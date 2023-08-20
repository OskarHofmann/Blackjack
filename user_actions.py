from enum import Enum


class UserActionsHand(Enum):
    DRAW = 1
    HOLD = 2
    SPLIT = 3


class UserActionsRoundEnd(Enum):
    CONTINUE = 1
    EXIT = 2