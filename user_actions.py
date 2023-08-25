from enum import IntEnum


class UserActionsHand(IntEnum):
    DRAW = 1
    STAND = 2
    SPLIT = 3


class UserActionsRoundEnd(IntEnum):
    CONTINUE = 1
    EXIT = 2