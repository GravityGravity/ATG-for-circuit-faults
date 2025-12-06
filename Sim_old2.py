# File: Sim.py
# Implemented by: St4rmanxz

import os
import sys
import colorama as cl

# Contains circuit structure
from Circ import Circuit, gate, line

# Contains logic tables for gates (Includes D and Not D values)
from B_logic import *

class Simulation:

    def __init__(self, testVector="", circuit: Circuit = None):
        self.testVector = testVector
        self.circuit = circuit
        # Dictionary to hold the current logic value (0 or 1) for each line ID
        # Initialize all lines to -1 (unknown)
        self.line_state = {}

    def promptForParameters(self):
        print("Simulation Parameters:")
        
        self.testVector = input(
            f'    {cl.Back.WHITE} > INPUT TEST VECTOR > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
        )
        self.testVector = self.testVector.strip()

    def Run(self):
        if not self.circuit:
            print(f"{cl.Fore.RED}Error: No circuit loaded.{cl.Style.RESET_ALL}")
            return

        # 1. Initialize State
        # Create a fresh state dictionary for this run
        self.line_state = {lid: -1 for lid in self.circuit.lines}

        # 2. Map Test Vector to Primary Inputs
        sorted_inputs = sorted(list(self.circuit.Primary_in))
        
        if len(self.testVector) != len(sorted_inputs):
            print(f"{cl.Fore.RED}Error: Test vector length ({len(self.testVector)}) does not match number of Primary Inputs ({len(sorted_inputs)}).")
            print(f"Expected inputs: {sorted_inputs}{cl.Style.RESET_ALL}")
            return

        print(f"{cl.Fore.CYAN}Applying Vector: {self.testVector}")
        for i, input_name in enumerate(sorted_inputs):
            try:
                val = int(self.testVector[i])
                if val not in [0, 1]: raise ValueError
                
                # USE HELPER FUNCTION to handle Fanout Propagation
                self.set_line_value(input_name, val)
                
            except ValueError:
                 print(f"{cl.Fore.RED}Error: Test vector must contain only 0s and 1s.{cl.Style.RESET_ALL}")
                 return

        # 3. Simulate
        self.simulate_circuit()

        # 4. Print Results
        finalOutput = ""
        sorted_outputs = sorted(list(self.circuit.Primary_out))
        
        print(f"{cl.Fore.GREEN}Simulation Complete:{cl.Style.RESET_ALL}")
        for out_line in sorted_outputs:
            val = self.line_state[out_line]
            display_val = str(val) if val != -1 else "X"
            print(f"  Output {out_line}: {display_val}")
            finalOutput += display_val
            
        print(f"  Full Output Vector: {finalOutput}")

    def set_line_value(self, line_id, value):
        """
        Sets the value of a line and propagates it if it's a fanout stem.
        This bridges the gap created by fanout_split().
        """
        self.line_state[line_id] = value
        
        # Check if this line is a fanout stem
        # In Circ.py, fanout stems have is_fanout=True and their 'nxt' set contains the branch line IDs
        line_obj = self.circuit.lines.get(line_id)
        if line_obj and line_obj.is_fanout:
            # Propagate value to all branches (e.g., '1gat' -> '1gat.1', '1gat.2')
            for branch_id in line_obj.nxt:
                # Recursively set branches (though branches typically aren't stems themselves)
                self.set_line_value(branch_id, value)

    def simulate_circuit(self):
        """
        Iteratively simulates gates until all signals settle or no progress is made.
        """
        gates_to_evaluate = set(self.circuit.gates.keys())
        progress = True

        while progress and gates_to_evaluate:
            progress = False
            evaluated_this_cycle = set()

            for gid in gates_to_evaluate:
                g = self.circuit.gates[gid]
                
                # Check if all inputs for this gate are ready (not -1)
                inputs_ready = True
                input_values = []
                
                for inp_line in g.gate_line_inputs:
                    val = self.line_state[inp_line]
                    if val == -1:
                        inputs_ready = False
                        break
                    input_values.append(val)

                # If ready, calculate output
                if inputs_ready:
                    result = self.evaluate_gate(g.type, input_values)
                    
                    # USE HELPER FUNCTION to update output (handles fanouts automatically)
                    self.set_line_value(g.gate_line_output, result)
                    
                    evaluated_this_cycle.add(gid)
                    progress = True

            gates_to_evaluate -= evaluated_this_cycle

    def evaluate_gate(self, gate_type, inputs):
        """
        Helper function to calculate logic output based on gate type.
        """
        if gate_type == g_types.AND:
            return 1 if all(inputs) else 0
        
        elif gate_type == g_types.OR:
            return 1 if any(inputs) else 0
        
        elif gate_type == g_types.NOT:
            return 1 if not inputs[0] else 0
        
        elif gate_type == g_types.NAND:
            return 0 if all(inputs) else 1
        
        elif gate_type == g_types.NOR:
            return 0 if any(inputs) else 1
        
        elif gate_type == g_types.XOR:
            return sum(inputs) % 2
            
        return 0