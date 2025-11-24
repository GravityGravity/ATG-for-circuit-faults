# FILE: ATG.py

# Description:
#   Automatic Test Generation file

# RUN THIS FILE FOR EVERYTHING

import sys
import os
import colorama as cl

from Sim import Simulation

from Circ import Circuit

from parser_runner import parse_circuit

# Auto reset colored console print
cl.init(autoreset=True)

selected_circuit: Circuit = None


def circuit_check():
    global selected_circuit
    if selected_circuit:
        return False
    else:
        print(
            f'{cl.Fore.RED}     ERROR: Circuit wasn\'t loaded, initialize circuit ->{cl.Fore.BLUE} option 0\n')
        return True


def gen_struct():
    """Option 0 - Generate data structure for circuit
    """

    print(cl.Fore.CYAN + 'DEBUG:   gen_struct()')  # debug

    ckt_name = input(
        f'    {cl.Back.WHITE} > Please input desired circuit file name < {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> File Name> {cl.Style.RESET_ALL}')

    # Create path to benchmarks folder that contains .ckt circuit file
    ckt_path = os.path.join(os.path.join(
        os.path.dirname(__file__), 'benchmarks'), (ckt_name))

    print(cl.Fore.CYAN + 'DEBUG:    ' + ckt_path)  # debug

    try:
        with open(ckt_path, 'r') as ckt_txt:
            print('    OPENED CKT FILE: ' + cl.Fore.GREEN + ckt_name)  # DEBUG
    except FileNotFoundError:
        print(cl.Fore.RED + '    ERROR: "' + ckt_name +
              '" file not found\n        '
              '-Ensure your circuit is within the benchmarks folder\n        '
              '-Ensure the benchmarks folder is in the same directory as this python file\n        '
              '-Ensure you add [filename].ckt to when prompted for name\n')
        comms()
        return 0

    # PARSE HERE
    global selected_circuit
    selected_circuit = parse_circuit(ckt_path, ckt_name)
    selected_circuit.fanout_split()
    selected_circuit.print_circ()
    print(f'{cl.Fore.GREEN} ✓ SUCESSFULLY!{cl.Fore.WHITE} CREATED DATA STRUCT FOR CIRCUIT: {cl.Fore.YELLOW}{selected_circuit.circuit_name}')
    comms()
    return 0


def fault_coll():
    """Option 1 - Perform fault collapsing and fault universe creation
    """
    print(cl.Fore.CYAN + 'DEBUG:   fault_coll()')  # debug
    if circuit_check():
        return None
    global selected_circuit
    selected_circuit.create_fault_universe()
    selected_circuit.fault_collapse()
    print(f'{cl.Fore.GREEN} ✓ SUCESSFULLY!{cl.Fore.WHITE} CREATED FAULT UNIVERSE FOR CIRCUIT: {selected_circuit.circuit_name}')
    return 1


def fc_display():
    """Option 2: - Display Fault Classes
    """
    print(cl.Fore.CYAN + 'DEBUG:   fc_display()')  # debug
    if circuit_check():
        return None
    if not selected_circuit.faults:
        print(
            f'{cl.Fore.RED}     ERROR: Fault classes empty , Create fault classes with ->{cl.Fore.BLUE} option 1\n')
        return None

    selected_circuit.faults.print_universe()

    return 1


def sim():
    """Option 3: - Simulate Circuit
    """
    print(cl.Fore.CYAN + 'DEBUG:   sim()')  # debug
    if circuit_check():
        return None
    global selected_circuit
    circSim = Simulation("000", selected_circuit)
    circSim.promptForParameters()
    circSim.Run()

    return 1


def Dalgo():
    print(cl.Fore.CYAN + 'DEBUG:   Dalgo()')  # debug
    if circuit_check():
        return None
    if not selected_circuit.fault_classes:
        print(
            f'{cl.Fore.RED}     ERROR: Circuit cannot perform D-ALGO without fault collapse.\n               Please collapse faults with ->{cl.Fore.BLUE} option 1\n')
    # ================================================================================================================
    # ================================================================================================================
    # ================================================================================================================
    # ================================================================================================================
    # STARMAN IMPLEMENT YOUR D-ALGO INTO THE D-ALGO.py FILE AND CALL IT HERE <------------------------------------------------------------------------------------
    # ================================================================================================================
    # ================================================================================================================
    # ================================================================================================================
    # ===============================================================================================================================
    return 1


def not_imp(option_num):
    print(cl.Fore.CYAN + 'DEBUG:   not_imp()')  # debug
    """Option 5 and 6: Test generation algorithms not implemented
    """
    print(
        f'{cl.Fore.RED}     ERROR: Selected {cl.Fore.BLUE} \'option {option_num}\' {cl.Fore.RED} not available.\n')
    return 1


def comms():
    """ Option 'help' - Prints console commands
    """
    print('\n' + cl.Fore.BLUE + 'Enter an option:\n'
          ' 0: generate data structures\n'
          ' 1: perform fault collapsing and create fault classes\n'
          ' 2: Display found fault classes\n'
          ' 3: Simulate the circuit\n'
          ' 4: Generate test (D-Algorithm)\n'
          + cl.Fore.WHITE + cl.Style.DIM +
          ' \033[9m5: Generate test (PODEM) --not implemented\n'
          ' 6: Generate test (Boolean Satifaibility) --not implemented\033[0m\n' + cl.Style.NORMAL + cl.Fore.BLUE +
          ' 7: Exit\n'
          '\'help\': Display console options again')


# While loop continously scans user input
comms()
while (True):
    option = input(cl.Fore.YELLOW + 'ATG.py> ' + cl.Style.RESET_ALL)

    match option.lower():
        case '0' | 'generate' | 'generate data structures':
            gen_struct()
        case '1' | 'perform' | 'perform fault collapsing' | 'create fault classes' | 'faults':
            fault_coll()
        case '2' | 'display' | 'fault display':
            fc_display()
        case '3' | 'simulate':
            sim()
        case '4' | 'generate' | 'generate test' | 'generate test (d-algorithm)' | 'd algo' | 'd-algo':
            Dalgo()
        case '5':
            not_imp('5')
        case '6':
            not_imp('6')
        case '7' | 'exit':
            print(cl.Back.YELLOW + '    EXITING PROGRAM    ')
            exit(0)
        case 'help' | '8':
            comms()
        case _:
            print(cl.Fore.RED + '   UNKOWNN COMMAND: "' + option + '"')
