# FILE: Circ.py (Circuit structure)

# Description:
#   Contains circuit structure used for ATG algorithms

from enum import Enum, auto
from B_logic import *
import colorama as cl


class Circuit():

    def __init__(self):
        self.Primary_in = []
        self.Primary_out = []

        self.gates = {}  # 'key' : 'value'
        self.lines = {}
        self.fanouts = {}

        fault_universe = []
        # fault_list = []
        # coll_faults = []

    def add_gate(self, gid: str, gtype: g_types, g_inputs: list, g_output: str):
        for inp in g_inputs:
            if not self.lines.get(inp):
                print(
                    cl.Fore.RED + '    ERROR(Circ.py): add_gate() input line does not exist in line\{} dict')

        if self.lines.get(g_output):
            temp_line = self.lines[g_output]
            temp_line.is_fanout = True

        g = gate(gid, gtype, g_inputs, g_output)
        self.gates[gid] = g

    def add_line(self, lid: str):
        l = line(lid)
        self.lines[lid] = l

    def get_line(self, s_lid: str):
        return self.lines[s_lid]

    def get_gate(self, s_gid: str):
        return self.gates[s_gid]

    def print_all():
        return 0


class line:

    is_fanout = False
    nxt = []  # The next gate or next fanout this line connects to

    def __init__(self, lid: str):
        self.line_id = lid
        self.values = []

    def add_nxt(self, item_id: str):
        self.nxt.append(item_id)


class gate:

    # Class Attributes
    def __init__(self, gid: str, gtype: g_types, g_inputs: list, g_output: list):
        self.gate_id = gid
        self.type = gtype
        self.gate_line_inputs = g_inputs
        self.gate_line_output = g_output
