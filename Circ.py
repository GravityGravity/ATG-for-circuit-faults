# FILE: Circ.py (Circuit structure)

from enum import Enum, auto
from B_logic import *


class Circuit():

    def __init__(self):
        self.Primary_in = []
        self.Primary_out = []

        self.gates = {}  # 'key' : 'value'
        self.lines = {}
        self.fanouts = {}

        fault_universe = []
        fault_list = []
        coll_faults = []

    def add_gate(self, gid: str, gtype: g_types, g_inputs: list, g_output):
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
    def __init__(self, gid: str, gtype: g_types, g_inputs: list, g_output: line):
        self.gate_id = gid
        self.type = gtype
        self.gate_line_inputs = g_inputs
        self.gate_line_output = g_output
