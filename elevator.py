import copy
import time
import json
import random
from threading import Thread

class LiftController():
    def __init__(self, max_floors):
        self.floors_calls_up    = set([])
        self.floors_calls_down  = set([])
        self.max_floor          = max_floors
        self.registered_lifts   = []

    def register_lift(self, lift):
        self.registered_lifts.append(lift)

    def check_periodically(self):
        while(True):
            print(str(time.time())+" . Starting checkss..")
            for floor in copy.copy(self.floors_calls_up):
                for lift in self.registered_lifts:
                    if lift.floor_no<floor and lift.dir=="up":
                        continue
                if floor in self.floors_calls_up:
                    for lift in self.registered_lifts:
                        if lift.dir=="stopped":
                            t = Thread(target=lift.move_up)
                            t.daemon=True
                            t.start()

            for floor in copy.copy(self.floors_calls_down):
                for lift in self.registered_lifts:
                    if lift.floor_no>floor and lift.dir=="down":
                        break
                if floor in self.floors_calls_down:
                    allotted = False
                    for lift in self.registered_lifts:
                        if lift.floor_no>floor and lift.dir=="stopped":
                            t = Thread(target=lift.move_down)
                            t.daemon=True
                            t.start()
                            allotted=True
                            break
                    if (not allotted):
                        for lift in self.registered_lifts:
                            if lift.floor_no < floor and lift.dir == "stopped":
                                self.floors_calls_up.add(floor)
                                t = Thread(target=lift.move_up)
                                t.daemon = True
                                t.start()
                                allotted = True
                                break

            print("Controller Sleeping for 5 secs")
            time.sleep(5)


class Lift():
    def __init__(self, lift_controller, lift_id):
        self.lift_id = lift_id
        self.no_of_people=0
        self.floor_no=0
        self.dir="stopped"
        self.lift_door_state="closed"
        self.floors_to_be_stopped=set([])
        self.lift_controller = lift_controller
        self.max_floor = lift_controller.max_floor

    def select_floor(self, dest_floor):
        self.floors_to_be_stopped.add(dest_floor)

    def stop(self):
        self.display_status("Stopping ")
        self.lift_door_state="open"
        self.display_status("waiting for 1 minute")
        time.sleep(60)
        self.lift_door_state = "closed"
        self.display_status()

    def move_up(self):
        self.dir = "up"
        self.lift_door_state = "closed"
        self.display_status("Moving up..")
        while self.floor_no <= self.max_floor:
            self.floor_no +=1
            self.display_status("Up Floor")
            if (self.floor_no in self.lift_controller.floors_calls_up) or (self.floor_no in self.floors_to_be_stopped):
                self.remove_cur_floor()
                self.stop()
        self.dir = "stopped"
        self.display_status("Lift Stopped")
        self.remove_cur_floor()

    def remove_cur_floor(self):
        try:
            self.lift_controller.floors_calls_up.remove(self.floor_no)
        except:
            pass
        try:
            self.floors_to_be_stopped.remove(self.floor_no)
        except:
            pass

    def move_down(self):
        self.dir = "down"
        self.lift_door_state = "closed"
        self.display_status("Moving down ")
        while self.floor_no >= 1:
            self.floor_no -=1
            self.display_status("Down Floor")
            if (self.floor_no in self.lift_controller.floors_calls_down) or (self.floor_no in self.floors_to_be_stopped):
                self.remove_cur_floor()
                self.stop()
        self.dir="stopped"
        self.display_status("Lift Stopped")
        self.remove_cur_floor()

    def display_status(self, msg = None):
        cur_status = {"lift_id":self.lift_id, "door_state": self.lift_door_state, "direction": self.dir, "floor_no": self.floor_no}
        if (msg):
            cur_status['msg']=msg
        print( json.dumps(cur_status) )

class FloorPanel():
    def __init__(self,floor_no, lift_controller):
        self.floor_no = floor_no
        self.lift_controller = lift_controller

    def press_up(self):
        self.lift_controller.floors_calls_up.add(self.floor_no)

    def press_down(self):
        self.lift_controller.floors_calls_down.add(self.floor_no)


def take_int_value_input(msg):
    while True:
        try:
            intval = int(input(msg))
            return intval
        except:
            print("Invalid entry. Please enter an integer...\nRetrying...")



max_floors = take_int_value_input("Enter the maximum number of Floors : ")

# Initialising the Lift Controller
lift_controller = LiftController(max_floors)
# Initialising Floor Panels
floor_panels = []
for fl in range(1, max_floors+1):
    fp = FloorPanel(fl, lift_controller)
    floor_panels.append(fp)

no_of_lifts = take_int_value_input("Enter Number of Lifts : ")

# Initilialsing {{no_of_lifts}} lifts
for i in range(0, no_of_lifts):
    lift_i = Lift(lift_controller, 1)
    lift_controller.register_lift(lift_i)

# Starting the scheduler in LiftController that should keep checking if any Lift needs to be sent to any floor.
lift_controller_thread = Thread(target=lift_controller.check_periodically)
lift_controller_thread.daemon = True
lift_controller_thread.start()

# Sample Inputs to get the code started.
'''
floor_panels[0].press_up()
floor_panels[9].press_down()
floor_panels[5].press_up()
floor_panels[7].press_down()
'''

while True:
    floorN = input("Enter Floor Number: ")
    try:
        floorN=int(floorN)
    except:
        print("Invalid floor number")
        continue
    dir = input("Choose Direction (U or D)")
    if dir=="D":
        floor_panels[floorN-1].press_down()
    else:
        floor_panels[floorN - 1].press_up()


