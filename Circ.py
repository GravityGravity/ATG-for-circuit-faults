
from enum import Enum, auto


class logic(Enum):
    ZERO = 0
    ONE = 1
    D = (0, 1)  # D
    D_ = (1, 0)  # Not D
    X = (1, 0)


class gate_logic_types(Enum):  # (controlling value, inversion signal)
    AND = (0, 0)
    OR = (1, 0)
    NOT = (logic.X, 1)
    NAND = (0, 1)
    NOR = (1, 1)
    XOR = 'idk'  # fix this


class Circuit:

    def __init__(self):
        self.Primary_in = []
        self.Primary_out = []

        self.gates = {}  # 'key' : 'value'
        self.lines = {}

        fault_universe = []
        fault_list = []

    def add_gate(self, gid: str, gtype: gate_logic_types, g_inputs: list, g_output):
        g = gate(gid, gtype, g_inputs, g_output)
        self.gates[gid] = g

    def add_line(self, lid: str):
        l = line(lid)
        self.lines[lid] = l


class line:

    def __init__(self, lid: str):
        self.line_id = lid
        self.values = []


class gate:

    # Class Attributes
    def __init__(self, gid: str, gtype: gate_logic_types, g_inputs: list, g_output: line):
        self.gate_id = gid
        self.type = gtype
        self.gate_line_inputs = g_inputs
        self.gate_line_output = g_output
