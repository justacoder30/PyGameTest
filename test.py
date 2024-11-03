from enum import Enum

class State(Enum):
    Idle = "Idle"
    Run = "Run"
    Fall = "Fall"
    Jump = "Jump"
    Attack = "Attack"
    Die = "Die"

state = State.Idle

match state:
    case State.Idle:
        print("Idle")