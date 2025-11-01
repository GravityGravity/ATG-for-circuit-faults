
from enum import Enum, auto


class gate_logic_types(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    NAND = auto()
    NOR = auto()
    XOR = auto()


class logic(Enum):
    ZERO = 0
    ONE = 1
    D = 2
    X = 3


class Circuit:

    Primary_in = []
    Primary_out = []

    gates = {}  # 'key' : 'value'
    lines = {}


class gate:

    # Class Attributes
    gate_id: str
    type: gate_logic_types
    gate_line_inputs = []
    gate_line_output = []


class line:

    values = []
    line_id: str
