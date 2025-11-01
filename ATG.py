# FILE: ATG.py

import sys
import os
import colorama as cl

# Auto reset colored console print
cl.init(autoreset=True)

# Option 0: Generate data struct


def gen_struct():
    """Option 0 - Generate data structure for circuit
    """

    print(cl.Fore.CYAN + 'DEBUG:   gen_struct()')  # debug

    ckt_name = input(
        '    Please input desired circuit file name\n' + cl.Fore.YELLOW + 'ATG.py>>File Name> ' + cl.Style.RESET_ALL)

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

    print(cl.Fore.GREEN +
          '✓ SUCESSFULLY CREATE DATA STRUCT FOR CIRCUIT:' + ckt_name)
    return 0

# Option 1: Generate fault collapse


def fault_coll():
    """Option 1 - Perform fault collapsing
    """
    print(cl.Fore.CYAN + 'DEBUG:   fault_coll()')  # debug
    return 0

# Prints console commands

# Simulate cir


def sim():
    """Option 3: - Simulate Circuit
    """
    print(cl.Fore.CYAN + 'DEBUG:   sim()')  # debug
    return 0


def Dalgo():
    return 0


def not_imp(option_num):
    """Option 6 and 7: Test generation algorithms not implemented
    """
    print(cl.Fore.CYAN + 'DEBUG:   not_imp()')  # debug
    return 0


def comms():
    """ Option 'help' - Prints console commands
    """
    print(cl.Fore.BLUE + 'Enter an option:\n'
          ' 0: generate data structures\n'
          ' 1: perform fault collapsing and create fault classes\n'
          ' 2: Display found fault classes\n'
          ' 3: Simulate the circuit\n'
          ' 4: Generate test (D-Algorithm)\n'
          + cl.Fore.WHITE + cl.Style.DIM +
          ' 5: Generate test (PODEM) --not implemented\n'
          ' 6: Generate tests (Boolean Satifaibility) --not implemented\n' + cl.Style.NORMAL + cl.Fore.BLUE +
          ' 7: Exit\n'
          '\'help\': Display console options again')


# While loop continously scans user input
comms()
while (True):
    option = input(cl.Fore.YELLOW + 'ATG.py> ' + cl.Style.RESET_ALL)

    match option:
        case '0':
            gen_struct()
        case '1':
            fault_coll()
        case '2':
            gen_struct()
        case '3':
            sim()
        case '4':
            gen_struct()
        case '5':
            not_imp('5')
        case '6':
            not_imp('6')
        case '7':
            print(cl.Back.YELLOW + '    EXITING PROGRAM    ')
            exit(0)
        case 'help':
            comms()
        case _:
            print(cl.Fore.RED + '   UNKOWNN COMMAND: "' + option + '"')
