# File: D_algo

import os
import sys
from dataclasses import dataclass

# Contains circuit structure
from Circ import *

# Contains logic tables for gates (Includes D and Not D values)
from B_logic import *


@dataclass
class LineState:
    l_obj: line
    val: L


D_circuit = None
D_lines: dict[str, LineState] = {}
D_frontier = []
J_frontier = []


def d_algorithm(circuit: Circuit = None):

    # Check if circuit exists
    if not circuit:
        print(f"{cl.Fore.RED}Error: No circuit loaded.{cl.Style.RESET_ALL}")
        return 0

    global D_lines
    global D_circuit
    D_circuit = circuit

    f_line, f_val = promptForParameters()
    f_line = D_circuit.get_line(f_line)

    # Creating D_algo circuit structure
    for l_name, l_obj in D_circuit.lines.items():
        print(f'D_algorithm(): f_line {f_line} , circ_line {l_obj}')  # debug
        if f_line == l_obj:
            if f_val == 1:
                D_lines[l_name] = LineState(l_obj=l_obj, val=L.D_)
                continue
            if f_val == 0:
                D_lines[l_name] = LineState(l_obj=l_obj, val=L.D)
                continue
        D_lines[l_name] = LineState(l_obj=l_obj, val=L.X)

    print(f'D_algorithm(): f_line {f_line} , SSA {f_val}')  # debug
    D_print_lines()

    # D ALGO IMPLEMENTATION
# ----------------------------------------

    imply_and_check(f_line)
    D_print_lines()

    if not PO_has_D():

        # Perform D-frontier queue
        print('    ----ENTERED D-FRONTIER... ----')
        print(f'    D-front -> {D_frontier}')
        while (D_frontier):
            if not D_imply_and_check():
                return False  # Fix
# --------------------------------------
    # Perform J Frontier Queue

    print('    ----ENTERED J-FRONTIER... ----')
    while (J_frontier):
        if not J_imply_and_check:
            return False  # Fix

    return 0


def promptForParameters():  # Thank you St4armanz
    print("D_algo Parameters:")

    options_list: list[tuple[str, int]] = []

    for f_li, f_val in D_circuit.faults.state.universe_coll.items():
        for v in sorted(f_val):
            options_list.append((f_li, v))

    # Build a numbered menu
    print("    Select an option:")
    for idx, (l, SSAval) in enumerate(options_list, start=1):
        print(f"    {idx}) {l} -> SSA-{SSAval}")

    # Example selection logic
    choice_str = input("   Enter choice number: ")
    choice = int(choice_str)
    while (True):
        if 1 <= choice <= len(options_list):
            selected_f_line, selected_f_val = options_list[choice - 1]
            print(f"You chose: {selected_f_line} -> {selected_f_val}")
            break
        else:
            print("Invalid choice. Try Again!")  # Debug / Fix

    return selected_f_line, selected_f_val


def D_print_lines():
    print("   D_algo line print:")
    for l_name, l_obj in D_lines.items():
        print(f'     {l_name} {l_obj.val}')


def justify():
    pass


def J_imply_and_check(g: gate):

    C = g.type.value[0]  # Controlling Value
    I = g.type.value[1]  # Inversion Value

    output_l = D_lines[g.gate_line_output]
    inputs = [D_lines[i] for i in g.gate_line_inputs]

    # D frontier

    if output_l[1] == L.X:  # Need to Imply Forward
        pass


# I guess forward imply constantly until ti reachs output
def Dfront_process(g: gate):

    C = g.type.value[0]  # Controlling Value
    I = g.type.value[1]  # Inversion Value

    output_l = D_lines[g.gate_line_output]
    inputs = [D_lines[i] for i in g.gate_line_inputs]

    # Error Checks

    if not output_l[1] == L.X:  # Need to Imply Forward Always
        # FIX / ERROR EXIT
        print('D_imply_and_check(): ERROR CANNOT PROPAGATE FAULT TO OUTPUT AS GATE OUTPUT ALREADY SET')
        return False

    # +=========================== MIGHT HAVE TO MOVE THIS
    for l_obj, val in inputs:
        if val in (L.D, L.D_):
            fault_inputs = D_lines[l_obj.line_id]
            break
    else:
        return 'D_imply_and_check(): ERROR D or D_ s not in ANY OF THE INPUTS'  # FIX / ERROR EXIT


def imply_and_check(D_line: line):

    print(f'imply_check(): current line {D_line.line_id}')
    print(f'                            nxt: {D_line.nxt}')

    if not D_line.nxt:
        return True  # Fault has reached PO or Errord

    for nxt in D_line.nxt:
        if nxt in D_lines:
            D_lines[nxt].val = D_lines[D_line.line_id].val
            imply_and_check(D_lines[nxt].l_obj)
            continue
        if nxt in D_circuit.gates:
            g = D_circuit.get_gate(nxt)
            inputs = [D_lines[i].val for i in g.gate_line_inputs]

            if g.type == g_types.NOT:
                result = op_case(g.type, inputs[0])   # or vals[0]
                D_lines[g.gate_line_output].val = result
            else:
                # works for 2, 3, 4... inputs
                result = op_case(g.type, *inputs)
                D_lines[g.gate_line_output].val = result

            if result in (L.D, L.D_):
                return imply_and_check(D_lines[g.gate_line_output].l_obj)
            else:
                D_frontier.append(g.gate_id)

        else:
            print(f'ERROR: line{nxt} ELSE IN IMPLY AND CHECK()')

    return False  # FAIL


def PO_has_D():  # Primary Output contain fault value

    for out in D_circuit.Primary_out:
        out_val = D_lines[out]
        if out_val.val in (L.D, L.D_):
            return True  # Fault not found in primary output

    return False  # Fault not found in primary output
