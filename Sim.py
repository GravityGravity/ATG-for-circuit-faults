# File: Sim.py
# Implemented by: Nik

import os
import sys
import colorama as cl

# Circuit Structures
from Circ import Circuit, gate, line

# B_logic structures
from B_logic import *


class Simulation:

    def __init__(self, testVector="", circuit: Circuit = None):                                         #Initialization and default values. testVector is input test streing, fault vector is optional fault injection string.
        self.testVector = testVector                                                                    #Circuit is a pass in from the circuit class, line_state is dictionary to hold current line values.                           
        self.faultVectorInput = ""
        self.circuit = circuit
        self.line_state = {}

    def promptForParameters(self):                                                                          #Function to prompt user for simulation parameters (test vector and optional fault vectors). Uses sime nice coloring and formatting from colorama.                          
        print("Simulation Parameters:")

        self.testVector = input(
            f'    {cl.Back.WHITE} > INPUT TEST VECTOR > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
        ).strip()

        print(f"    {cl.Style.DIM}(Optional) Enter list of Fault Vectors (e.g., {{0000, 0011}} or just 0000).{cl.Style.RESET_ALL}")
        print(
            f"    {cl.Style.DIM}Use '0'/'1' for faults, '<empty string>' for none.{cl.Style.RESET_ALL}")                                          
        self.faultVectorInput = input(
            f'    {cl.Back.WHITE} > INPUT FAULT LIST > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
        ).strip()

    def Run(self):
        if not self.circuit:
            print(f"{cl.Fore.RED}Error: No circuit loaded.{cl.Style.RESET_ALL}")
            return

        sorted_inputs = sorted(list(self.circuit.Primary_in))

        if len(self.testVector) != len(sorted_inputs):
            print(f"{cl.Fore.RED}Error: Test vector length ({len(self.testVector)}) does not match #PIs ({len(sorted_inputs)}).{cl.Style.RESET_ALL}")
            return


        print(f"\n{cl.Fore.CYAN}--- Running Good Simulation ---{cl.Style.RESET_ALL}")
        good_output = self.run_single_pass(sorted_inputs, self.testVector)                       #Run a single good simulation pass to get the expected output. (this will be compared against the runs w/ fault sims)                           

        print(f"{cl.Fore.GREEN}Good Output:{cl.Style.RESET_ALL} {good_output}")

        if not self.faultVectorInput:
            return


        cleaned_input = self.faultVectorInput.replace('{', '').replace('}', '')                 #Code will look for {...} and split the cases by commas, and remove the brackets. (E.g. {0000,111,1010})

        if not cleaned_input:                                                                   #Empty string?                      
            return

        raw_list = cleaned_input.split(',')
        fault_vectors = [v.strip() for v in raw_list if v.strip()]

        print(f"\n{cl.Fore.CYAN}--- Running Fault Simulations ({len(fault_vectors)} vectors) ---{cl.Style.RESET_ALL}")

        faults_detected = 0

        for f_vec in fault_vectors:                                                                                                 #Big loop that will run the entire sim again for each fault vector. I think its the best way to do this?
            # Check length compatibility
            if len(f_vec) != len(sorted_inputs):
                print(
                    f"{cl.Fore.YELLOW}Warning: Skipping invalid length vector '{f_vec}'{cl.Style.RESET_ALL}")
                continue

            # Run simulation with this specific fault mask
            bad_output = self.run_single_pass(
                sorted_inputs,
                self.testVector,
                fault_mask=f_vec
            )

            # Compare results
            if bad_output != good_output:
                faults_detected += 1
                print(
                    f"  {cl.Fore.RED}[DETECTED]{cl.Style.RESET_ALL} Fault Vector: {f_vec} | Output: {bad_output} (Expected: {good_output})")
            else:
                pass

        if faults_detected == 0:
            print(
                f"{cl.Fore.YELLOW}No faults detected by any provided vector.{cl.Style.RESET_ALL}")
        else:
            print(
                f"{cl.Fore.GREEN}Total Fault Vectors Detected: {faults_detected}{cl.Style.RESET_ALL}")

    def run_single_pass(self, sorted_inputs, vector_str, fault_mask=None):                      # Helper function to run a single simulation pass with optional fault injection. Uses a mask to override input values.                       
        # 1. Reset State
        self.line_state = {lid: -1 for lid in self.circuit.lines}

        # 2. Apply Inputs (with optional Fault Injection)
        for i, input_name in enumerate(sorted_inputs):
            try:
                # Default value from test vector
                val = int(vector_str[i])

                if fault_mask:
                    mask_char = fault_mask[i]
                    if mask_char == '0':
                        val = 0
                    elif mask_char == '1':
                        val = 1
                    # If 'X' or other, keep original 'val'

                self.set_line_value(input_name, val)
            except ValueError:
                print(
                    f"{cl.Fore.RED}Error: Input contains non-integer.{cl.Style.RESET_ALL}")
                return ""

        # 3. Simulate
        self.simulate_circuit()

        # 4. Collect Output
        finalOutput = ""
        sorted_outputs = sorted(list(self.circuit.Primary_out))                     #Sorted list of primary output line IDs. Print in order.
        for out_line in sorted_outputs:
            val = self.line_state[out_line]
            display_val = str(val) if val != -1 else "X"
            finalOutput += display_val

        return finalOutput

    def set_line_value(self, line_id, value):                               # Helper function that sets the value of a line. Will also propagate the value if the line is a fanout stem.
        self.line_state[line_id] = value

        line_obj = self.circuit.lines.get(line_id)
        if line_obj and line_obj.is_fanout:
            for branch_id in line_obj.nxt:
                self.set_line_value(branch_id, value)                       

    def simulate_circuit(self):                                             #Function to simulate circuit.
        gates_to_evaluate = set(self.circuit.gates.keys())                  #Set of gate IDs that need to be evaluated.
        progress = True                                                     #Flag to track if any gates were evaluated in the current iteration.                       

        while progress and gates_to_evaluate:                               #Continue while there is progress and there are gates left to evaluate.                         
            progress = False                                                #Set progress to False (this will be used to track the gates that get evaluated in this run).               
            evaluated_this_cycle = set()                                    #Set to track gates evaluated in this iteration. (Starts empty)          

            for gid in gates_to_evaluate:                                   #For each gate in the set to evaluate, we will loop through them.      
                g = self.circuit.gates[gid]                                 #Get the gate object from the circuit using its ID.

                inputs_ready = True                                         #Assume all inputs are ready initially.                    
                input_values = []                                           #List to hold the input values for the gate.                  
                for inp_line in g.gate_line_inputs:                         #For each input line of the gate, we will check if its value is known.                     
                    val = self.line_state[inp_line]                         #Get the current value of the input line from the line_state dictionary.
                    if val == -1:                                           #If the value is -1, it means the input is not yet known (must perform the evaluation helper to calculate a value).                 
                        inputs_ready = False                                #Set inputs_ready to False and break out of the loop.                
                        break                               
                    input_values.append(val)                                #If the value is known, append it to the input_values list.                      

                if inputs_ready:                                            #If all inputs are ready, we can evaluate the gate.                        
                    result = self.evaluate_gate(g.type, input_values)       #Evaluate the gate using its type and the collected input values.
                    self.set_line_value(g.gate_line_output, result)         #Set the output line value using the result of the evaluation.    
                    evaluated_this_cycle.add(gid)                           #Add this gate ID to the set of evaluated gates for this cycle.                
                    progress = True                                         #Set progress to True since we evaluated at least one gate.                           

            gates_to_evaluate -= evaluated_this_cycle                       #Remove the evaluated gates from the set to evaluate for the next iteration.                  

    def evaluate_gate(self, gate_type, inputs):                   #Function to evaluate the gate in the circuit based on its type. Returns the output value based on the operation and inputs.
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
       # elif gate_type == g_types.XOR:                //Saw that modulo is a good way to do it. Probably don't need it for now though.
       #     return sum(inputs) % 2
        return 0
