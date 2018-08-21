# The Elevator Control System
## Description:
This project has the implementation of an Elevator Control System.
The main entities in this are:-
1. **Lifts**: Every lift takes care of it's own functionalities, eg. `Move Up/Down`, `Stop`, `Open/Close the Door` etc and manages its states- `Door Close Status`, `Current Floor`, `Direction` etc. This Project supports Multiple Lifts, functioning in parallel, in order to fulfil the `call`. 

2. **Floor Panels**: Every floor has a panel that has 2 buttons which are used to give a signal weather the user wants to go up or down from that floor.  

3. **The Lift Controller**: Acts as a central control system that takes IO from the **Floor Panels** and signals the Lifts about the floor towards which they should go. The Lift Controller also contains references to all the lifts, thereby, access their states, in order to instruct a specific Lift.

## Build and Run Instructions:
### Requirements:-
- Python (3+ version)

### Steps:-
- Execute command: `python elevator.py`
The above command starts the program.

