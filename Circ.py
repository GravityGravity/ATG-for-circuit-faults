# FILE: Circ.py (Circuit structure)

# Description:
#   Contains circuit structure used for ATG algorithms

from enum import Enum, auto
from B_logic import *
import colorama as cl

cl.init(autoreset=True)


class Circuit():

    def __init__(self, name: str):
        self.circuit_name: str = name
        self.Primary_in: set[str] = set()
        self.Primary_out: set[str] = set()

        self.gates: dict[str, gate] = {}  # 'key' : 'value'
        self.lines: dict[str, line] = {}
        self.fanouts: set[str] = set()

        self.fault_universe: dict = {}
        # self.fault_list = [] # Place Holders
        # self.coll_faults = []

    def add_gate(self, gid: str, gtype: g_types, g_inputs: list, g_output: str):
        for inp in g_inputs:

            inp_line = self.lines.get(inp)
            if not inp_line:
                msg = f'        ERROR(Circ.py): add_gate() input line DNE \\{inp} Creating new line...'
                print(cl.Fore.RED + '    ' + msg)
                inp_line = self.add_line(inp)

            inp_line.nxt.add(gid)

            if len(inp_line.nxt) > 1:
                if not inp_line.is_fanout:
                    inp_line.fan_out_change(True)
                if not inp_line.line_id in self.fanouts:
                    self.fanouts.add(inp_line.line_id)

        if not self.lines.get(g_output):
            temp_line = line(g_output)
            self.lines[g_output] = temp_line

        g = gate(gid, gtype, g_inputs, g_output)
        print(
            f'     {cl.Fore.GREEN}__Created New Gate {cl.Fore.WHITE}{g.gate_id} ')
        self.gates[gid] = g

    def add_line(self, lid: str):
        # Check if line already exists
        if self.lines.get(lid):
            msg = f'ERROR(Circ.py): add_line() line already exists \\{lid} dict EXITING>>>...'
            print(cl.Fore.RED + '    ' + msg)
            raise KeyError(msg)

        l = line(lid)
        print(
            f'     {cl.Fore.BLUE}_Created New Line {cl.Fore.WHITE}{l.line_id} ')
        self.lines[lid] = l

        return self.lines[lid]

    def fanout_split(self):

        for fanout in self.fanouts:
            print(fanout)
            fanout_line = self.lines.get(fanout)
            src_line_nxt = set()
            for i, nxt_gate in enumerate(fanout_line.nxt):
                print(i)

                # New split line nxt set to gate
                newline = self.add_line(fanout + f'.{i+1}')
                newline.add_nxt(nxt_gate)
                # Change nxt of src fanout line
                src_line_nxt.add(fanout + f'.{i+1}')
                # Change gate input to split line
                self.get_gate(nxt_gate).g_change_input(
                    fanout, fanout + f'.{i+1}')

            fanout_line.nxt = src_line_nxt

    def get_line(self, s_lid: str):
        return self.lines.get(s_lid)

    def get_gate(self, s_gid: str):
        return self.gates.get(s_gid)

    # Fault Handling

    def create_fault_universe(self):
        for inp in self.Primary_in:
            self.fault_universe[inp] = {'SA0', 'SA1'}

        for fanout in self.fanouts:
            fanout_line = self.get_line(fanout)
            if not fanout in self.fault_universe:
                self.fault_universe[fanout] = {'SA0', 'SA1'}
            for nxt_line in fanout_line.nxt:
                self.fault_universe[nxt_line] = {'SA0', 'SA1'}

        pass

    def print_fault_U(self):
        # print Gates
        print(
            f'    {cl.Back.RED} FAULT UNIVERSE {cl.Back.RESET}{cl.Fore.RED} (total: {len(self.fault_universe) * 2})')
        for key, value in self.fault_universe.items():
            print(f' {cl.Fore.RED}  {key}', end="")
            for fault in self.fault_universe[key]:
                print(f' {fault} ', end="")
            print('\n')
        print('==========FINISHED=========')
        pass

        # Circuit Printing

    def print_circ(self):
        # Print Circuit Name
        print(f'========================================')
        print(f'        {self.circuit_name.upper()}         \n')

        # Print Primary Inputs
        print(f'    {cl.Back.YELLOW} PRIMARY INPUTS ')
        for PI in self.Primary_in:
            print(f' {PI} ', end="")
        print('\n')

        # Print Primary Outputs
        print(f'    {cl.Back.YELLOW} PRIMARY OUTPUTS ')
        for PO in self.Primary_out:
            print(f' {PO} ', end="")
        print('\n')

        # Print Lines
        print(
            f'    {cl.Back.BLUE} LINES {cl.Back.RESET}{cl.Fore.BLUE} (total: {len(self.lines)})')
        for key, value in self.lines.items():
            print(f' {cl.Fore.CYAN}{key} ->', end="")
            for connected in value.nxt:
                print(f'  {connected} ', end="")
            if value.line_id in self.fanouts:
                print(f'   {cl.Fore.BLACK}{cl.Back.WHITE} FANOUT ', end="")
            if value.line_id in self.Primary_in:
                print(f'   {cl.Fore.BLUE}{cl.Back.WHITE} P INPUT ', end="")
            if value.line_id in self.Primary_out:
                print(f'   {cl.Fore.YELLOW}{cl.Back.WHITE} P OUTPUT ', end="")
            print('\n')

        # print Gates
        print(
            f'    {cl.Back.GREEN} GATES {cl.Back.RESET}{cl.Fore.GREEN} (total: {len(self.gates)})')
        for key, value in self.gates.items():
            print(f' {key}({value.type.name})')

            print(f' {cl.Fore.GREEN}G_Input: ', end="")
            for Inp in value.gate_line_inputs:
                print(f' {Inp} ', end="")

            print(f' {cl.Fore.MAGENTA}G_Output: ', end="")
            print(f' {value.gate_line_output} ', end="")
            print('\n')
        print('\n')

        print('==========FINISHED=========')


class line:

    def __init__(self, lid: str):
        self.line_id = lid
        self.values = []
        self.nxt: set[str] = set()
        self.is_fanout = False

    def fan_out_change(self, fan_out: bool):
        self.is_fanout = fan_out

    def add_nxt(self, item_id: str):
        self.nxt.add(item_id)


class gate:

    # Class Attributes
    def __init__(self, gid: str, gtype: g_types, g_inputs: list, g_output: str):
        self.gate_id = gid
        self.type = gtype
        self.gate_line_inputs = g_inputs
        self.gate_line_output = g_output

    def g_change_input(self, old_line_id, new_line_id):
        indx = self.gate_line_inputs.index(old_line_id)
        self.gate_line_inputs[indx] = new_line_id
