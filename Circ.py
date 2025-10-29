
from enum import Enum, auto


class gate_logic_types(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    NAND = auto()
    NOR = auto()
    XOR = auto()


class Circuit:

    Primary_in = []
    Primary_out = []


class gate:

    # Class Attributesd

    type: gate_logic_types

    def __init__(self, id, logic_gate):
        self.gate_id = id
        self.type = logic_gate
