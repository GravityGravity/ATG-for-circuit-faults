# File: D_algo

import os
import sys

# Contains circuit structure
from Circ import *

# Contains logic tables for gates (Includes D and Not D values)
from B_logic import *

D_circuit = None
D_lines: dict[str, tuple[line, L]] = {}
D_frontier = []
J_frontier = []


class decision:
    def __init__(self):
        pass


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
                D_lines[l_name] = (l_obj, L.D)
                continue
            if f_val == 0:
                D_lines[l_name] = (l_obj, L.D_)
                continue
        D_lines[l_name] = (l_obj, L.X)

    print(f'D_algorithm(): f_line {f_line} , SSA {f_val}')  # debug
    D_print_lines()

    # Perform D-frontier queue
    while (D_frontier):
        if not imply_and_check():
            return False  # Fix

    # Perform J Frontier Queue
    while (J_frontier):
        if not imply_and_check:
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
        print(f'     {l_name} {l_obj[1]}')


def justify():
    pass


def imply_and_check():
    pass
