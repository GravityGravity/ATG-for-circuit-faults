# FILE: ATG.py

import os
import colorama as cl

# Auto reset colored console print
cl.init(autoreset=True)

# Option 0: Generate data struct


def gen_struct():

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
        return 0

    # PARSE HERE

    return 0

# Option 1: Generate fault collapse


def fault_coll():
    return 0

# Prints console commands


def comms():
    print(cl.Fore.BLUE + 'Enter an option:\n'
          '0: generate data structures\n'
          '1: perform fault collapsing and create fault classes\n'
          '2:Display found fault classes\n'
          '3:Simulate the circuit\n'
          '4:PODEM algo\n'
          '5:D-Algorithm\n'
          '6:Placeholder algo\n'
          '7: Reset ATG\n'
          '\'help\': Display console options again')


# While loop continously scans user input
comms()
while (True):
    option = input(cl.Fore.YELLOW + 'ATG.py> ' + cl.Style.RESET_ALL)

    match option:
        case '0':
            gen_struct()
            comms()
        case '1':
            gen_struct()
        case '2':
            gen_struct()
        case '3':
            gen_struct()
        case '4':
            gen_struct()
        case '5':
            gen_struct()
        case '6':
            gen_struct()
        case '7':
            gen_struct()
        case 'help':
            comms()
        case _:
            print(cl.Fore.RED + '   UNKOWNN COMMAND: "' + option + '"')
