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
        if f_line == l_obj:
            if f_val == 1:
                D_lines[l_name] = LineState(l_obj=l_obj, val=L.D_)
                continue
            if f_val == 0:
                D_lines[l_name] = LineState(l_obj=l_obj, val=L.D)
                continue
        D_lines[l_name] = LineState(l_obj=l_obj, val=L.X)

    D_print_lines()

    # D ALGO IMPLEMENTATION
# ----------------------------------------

    imply_and_check(f_line)
    D_print_lines()

    if not PO_has_D():

        # Perform D-frontier queue
        print('    ---- ENTERED D-FRONTIER... ----')
        print(f'    D-front -> {D_frontier}')
        while (D_frontier):
            Dfront_process(D_circuit.get_gate(D_frontier[0]))
            D_frontier.pop(0)
            # --------------------------------------
    D_print_lines()  # Debug
    if not PO_has_D():
        # ----------------PERFORM FAULT VECTOR UPDATE HERE !!!!
        return False

    # ============= J FRONTIER =======================

    for g_str in D_circuit.gates:
        g = D_circuit.get_gate(g_str)
        if D_lines[g.gate_line_output].l_obj == f_line:
            J_frontier.append(g.gate_id)
            print(f'         DALGO 1 J APPENDED gate {g.gate_id}')
            continue

        for inp in g.gate_line_inputs:
            if D_lines[inp].val == L.X and D_lines[g.gate_line_output].val != L.X:
                J_frontier.append(g.gate_id)
                print(f'        DALGO 2 J APPENDED gate {g.gate_id}')
                break

    print('    ---- ENTERED J-FRONTIER... ----')
    while (J_frontier):
        Jfront_process(D_circuit.get_gate(J_frontier[0]))
        J_frontier.pop(0)

    D_print_lines()  # Debug

    # Check Primary Inputs

    return True


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
    while (True):
        choice_str = input("   Enter choice number: ")
        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue
        if 1 <= choice <= len(options_list):
            selected_f_line, selected_f_val = options_list[choice - 1]
            print(f"You chose: {selected_f_line} -> {selected_f_val}")
            break
        else:
            print("Invalid choice. Try Again!")  # Debug / Fix
            continue

    return selected_f_line, selected_f_val


def D_print_lines():
    print("   D_algo line print:")
    for l_name, l_obj in D_lines.items():
        print(f'     {l_name} {l_obj.val}')


def Jfront_process(g: gate):

    print(f'Jfront({g.gate_id})')

    C = g.type.value[0]  # Controlling Value
    I = g.type.value[1]  # Inversion Value
    is_C_activated = False

    output_l = D_lines[g.gate_line_output]
    inputs = [D_lines[i] for i in g.gate_line_inputs]

    if output_l.val == L.X:
        print(
            f'     J_process(): ERROR gate {g.gate_id} has unknown output within J frontier')
        if output_l.l_obj.is_fanout:
            for n in output_l.l_obj.nxt:
                if not D_lines[n] == L.X:
                    fanout_val = D_lines[n].val

            output_l.val = fanout_val
            for n in output_l.l_obj.nxt:
                if D_lines[n] == L.X:
                    D_lines[n] = fanout_val
                elif D_lines[n] == fanout_val:
                    continue
                else:
                    print('     J_process(): ERROR J-frontier fanout conflict')
        return False

    if g.type == g_types.XOR:
        A = inputs[0]
        B = inputs[1]
        pair = (A.val, B.val)
        if output_l.val == 0:
            match pair:
                case (0, L.X):
                    B.val = 0
                case (1, L.X):
                    B.val = 1
                case (L.X, 0):
                    A.val = 0
                case (L.X, 1):
                    A.val = 0
        elif output_l.val == 1:
            match pair:
                case (0, L.X):
                    B.val = 1
                case (1, L.X):
                    B.val = 0
                case (L.X, 1):
                    A.val = 0
                case (L.X, 0):
                    A.val = 1
        if not Jfront_check(g):
            return False

        return True

    if I:
        if int_inverse(C) == output_l.val:
            is_C_activated: True
    elif C == output_l.val:
        is_C_activated: True

    if is_C_activated:
        for inp in inputs:
            if inp.val == L.X:
                inp.val = C
                print(
                    f'    C_act TRUE input_line: {inp.l_obj.line_id} set to {inp.val}')

    if not is_C_activated:
        for inp in inputs:
            if inp.val == L.X:
                inp.val = int_inverse(C)
                print(
                    f'    C_act FALSE input_line: {inp.l_obj.line_id} set to {inp.val}')

    print(f'     output_line {output_l.l_obj.line_id} was {output_l.val}')

    if not Jfront_check(g):
        return False

    return True


def Jfront_check(g: gate):

    gates_to_check: list[gate] = []
    output_l = D_lines[g.gate_line_output]
    inputs = [D_lines[i] for i in g.gate_line_inputs]
    inputs_vals = [L(D_lines[i].val) for i in g.gate_line_inputs]

    result = op_case(g.type, *inputs_vals)

    if result != L(output_l.val):
        print(
            f'    J_frontcheck(): ERROR: {g.gate_id} output {output_l.val} DNE input operation result {result}')
        return False

    for inp in inputs:

        for g_iter in D_circuit.gates:
            select_gate = D_circuit.get_gate(g_iter)

            if select_gate.gate_line_output == inp.l_obj.line_id:
                gates_to_check.append(select_gate)

    print(f' -> gates_to_check: {gates_to_check}')

    for g_obj in gates_to_check:
        for g_inps in g_obj.gate_line_inputs:
            if D_lines[g_inps].val == L.X and g_obj.gate_id not in J_frontier:
                J_frontier.append(g_obj.gate_id)
                print(f'         JCHECK2 APPENDED gate {g_obj.gate_id}')
                break

    return True


# I guess forward imply constantly until ti reachs output


def Dfront_process(g: gate):

    print(f'    Dfront_process(): processed gate {g.gate_id}')

    C = g.type.value[0]  # Controlling Value
    I = g.type.value[1]  # Inversion Value

    output_l = D_lines[g.gate_line_output]
    inputs = [D_lines[i] for i in g.gate_line_inputs]

    # Error Checks

    if not output_l.val == L.X:  # Need to Imply Forward Always
        # FIX / ERROR EXIT
        print(
            'D_process(): ERROR CANNOT PROPAGATE FAULT TO OUTPUT AS GATE OUTPUT ALREADY SET')
        return False

    # +=========================== MIGHT HAVE TO MOVE THIS
    for l in inputs[:]:
        if l.val in (L.D, L.D_):
            fault_input = D_lines[l.l_obj.line_id]
            inputs.remove(D_lines[l.l_obj.line_id])
            break

    if not fault_input:
        # FIX / ERROR EXIT
        print(
            f'D_process(): ERROR D or D_ s not in ANY OF THE INPUTS OF GATE {g.gate_id}')
        return False

    if g.type == g_types.XOR:
        for inp in inputs:
            inp.val = 0

        output_l.val = op_case(g.type, fault_input.val,
                               *(L(o.val) for o in inputs))

    else:
        for inp in inputs:
            inp.val = int_inverse(C)
            output_l.val = op_case(
                g.type, fault_input.val, *(L(o.val) for o in inputs))

    if not output_l.val in (L.D, L.D_):
        print(
            f'D_process(): FINAL OUTPUT OF D_FRONTIER GATE NOT FAULT VALUE: {g.gate_id}')
    imply_and_check(output_l.l_obj)


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
                print(f'    Added {g.gate_id} to D-Frontier Queue:')
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


def justify_XOR(g: gate, output_value):
    # gate.inputs = [A, B]
    A = D_lines[g.gate_line_inputs[0]]
    B = D_lines[g.gate_line_inputs[1]]

    if output_value == 1:
        # Inputs must differ
        patterns = [(0, 1), (1, 0)]
    elif output_value == 0:
        # Inputs must be the same
        patterns = [(0, 0), (1, 1)]
    else:
        raise ValueError("XOR output cannot be X during justification")

    valid_solutions = []

    for a_val, b_val in patterns:
        if (A.val not in (L.X, a_val)):
            continue
        if (B.val not in (L.X, b_val)):
            continue
        valid_solutions.append((a_val, b_val))

    return valid_solutions
