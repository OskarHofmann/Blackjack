from enum import IntEnum


class UserActionsHand(IntEnum):
    DRAW = 1
    STAND = 2
    DOUBLE_DOWN = 3
    SPLIT = 4


class UserActionsRoundEnd(IntEnum):
    CONTINUE = 1
    EXIT = 2