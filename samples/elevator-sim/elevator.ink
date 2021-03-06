inkling "2.0"

type ButtonState number<NotPressed = 0, Pressed = 1>
experiment {
    backend_type: "pdp2"
}

# Position is current location of elevator.
type FloorState {
    Position: number<0, 1, 2>,
    Floor1: ButtonState,
    Floor2: ButtonState,
    Floor3: ButtonState
}

# command options: up, open, down
type Action {
    command: number<Up = 0, Open = 1, Down = 2>
}

# Connect to SimPy simulator for training
# Simulator source code:
# https://github.com/BonsaiAI/bonsai-sdk/blob/master/samples/elevator-sim/elevator.py
simulator ElevatorSimulator(action: Action): FloorState {
}

graph (input: FloorState): Action {
    concept ElevatorPlan(input): Action {
        curriculum {
            source ElevatorSimulator
        }
    }
    output ElevatorPlan
}
