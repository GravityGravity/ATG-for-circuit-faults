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
        self.faultVector = ""
        self.circuit = circuit
        # Dictionary to hold the current logic value (0 or 1) for each line ID
        # Initialize all lines to -1 (unknown)
        self.line_state = {}

    def promptForParameters(self):
        print("Simulation Parameters:")
        
        # 1. Get Test Vector
        self.testVector = input(
            f'    {cl.Back.WHITE} > INPUT TEST VECTOR > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
        ).strip()
        
        # 2. Get Fault Vector (Optional)
        print(f"    {cl.Style.DIM}(Optional) Enter Primary Input Faults (same length). Use '0'/'1' for faults, 'X' for none.{cl.Style.RESET_ALL}")
        self.faultVector = input(
            f'    {cl.Back.WHITE} > INPUT FAULT VECTOR > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
        ).strip()

    def Run(self):
        if not self.circuit:
            print(f"{cl.Fore.RED}Error: No circuit loaded.{cl.Style.RESET_ALL}")
            return

        sorted_inputs = sorted(list(self.circuit.Primary_in))
        
        # --- Validation ---
        if len(self.testVector) != len(sorted_inputs):
            print(f"{cl.Fore.RED}Error: Test vector length ({len(self.testVector)}) does not match #PIs ({len(sorted_inputs)}).{cl.Style.RESET_ALL}")
            return

        # ==========================================
        # 1. Run Good Circuit (Golden Run)
        # ==========================================
        print(f"\n{cl.Fore.CYAN}--- Running Good Simulation ---{cl.Style.RESET_ALL}")
        good_output = self.run_single_pass(sorted_inputs, self.testVector)
        
        print(f"{cl.Fore.GREEN}Good Output:{cl.Style.RESET_ALL} {good_output}")

        # If no faults provided, we are done
        if not self.faultVector:
            return

        # ==========================================
        # 2. Run Fault Simulations
        # ==========================================
        if len(self.faultVector) != len(sorted_inputs):
            print(f"{cl.Fore.RED}Error: Fault vector length ({len(self.faultVector)}) must match input vector length.{cl.Style.RESET_ALL}")
            return

        print(f"\n{cl.Fore.CYAN}--- Running Fault Simulations ---{cl.Style.RESET_ALL}")
        
        faults_detected = 0

        # Iterate through the fault vector characters
        for i, fault_char in enumerate(self.faultVector):
            # Only process if it is a valid binary fault ('0' or '1')
            if fault_char in ['0', '1']:
                target_line = sorted_inputs[i]
                stuck_at_val = int(fault_char)

                # Prepare a faulty input vector
                # We copy the original logic, but override the specific input to the stuck-at value
                # (A stuck-at fault on a PI essentially overrides the test vector value for that line)
                
                # Note: We don't change the testVector string itself, we just tell the 
                # run_single_pass method to inject this specific fault.
                
                bad_output = self.run_single_pass(
                    sorted_inputs, 
                    self.testVector, 
                    fault_line=target_line, 
                    fault_val=stuck_at_val
                )

                # Compare results
                if bad_output != good_output:
                    faults_detected += 1
                    print(f"  {cl.Fore.RED}[DETECTED]{cl.Style.RESET_ALL} Fault: {target_line} SA-{stuck_at_val} | Output: {bad_output} (Expected: {good_output})")
                else:
                    # Optional: Print undetected faults if you want verbosity
                    # print(f"  [Undetected] Fault: {target_line} SA-{stuck_at_val} | Output: {bad_output}")
                    pass

        if faults_detected == 0:
            print(f"{cl.Fore.YELLOW}No faults detected by this vector.{cl.Style.RESET_ALL}")
        else:
            print(f"{cl.Fore.GREEN}Total Faults Detected: {faults_detected}{cl.Style.RESET_ALL}")

    def run_single_pass(self, sorted_inputs, vector_str, fault_line=None, fault_val=None):
        """
        Runs a single simulation pass.
        Args:
            sorted_inputs: list of PI names
            vector_str: string of 0s and 1s
            fault_line: (Optional) Name of PI to force to a stuck-at value
            fault_val: (Optional) Value (0 or 1) to force the fault_line to
        Returns:
            String representing the output vector
        """
        # 1. Reset State
        self.line_state = {lid: -1 for lid in self.circuit.lines}

        # 2. Apply Inputs (with optional Fault Injection)
        for i, input_name in enumerate(sorted_inputs):
            try:
                # Default value from test vector
                val = int(vector_str[i])
                
                # INJECT FAULT: If this line is the one we are currently testing,
                # override its value with the stuck-at value.
                if input_name == fault_line:
                    val = fault_val

                self.set_line_value(input_name, val)
            except ValueError:
                print(f"{cl.Fore.RED}Error: Input contains non-integer.{cl.Style.RESET_ALL}")
                return ""

        # 3. Simulate
        self.simulate_circuit()

        # 4. Collect Output
        finalOutput = ""
        sorted_outputs = sorted(list(self.circuit.Primary_out))
        for out_line in sorted_outputs:
            val = self.line_state[out_line]
            display_val = str(val) if val != -1 else "X"
            finalOutput += display_val
        
        return finalOutput

    def set_line_value(self, line_id, value):
        """
        Sets the value of a line and propagates it if it's a fanout stem.
        """
        self.line_state[line_id] = value
        
        line_obj = self.circuit.lines.get(line_id)
        if line_obj and line_obj.is_fanout:
            for branch_id in line_obj.nxt:
                self.set_line_value(branch_id, value)

    def simulate_circuit(self):
        """
        Iteratively simulates gates until all signals settle.
        """
        gates_to_evaluate = set(self.circuit.gates.keys())
        progress = True

        while progress and gates_to_evaluate:
            progress = False
            evaluated_this_cycle = set()

            for gid in gates_to_evaluate:
                g = self.circuit.gates[gid]
                
                # Check inputs
                inputs_ready = True
                input_values = []
                for inp_line in g.gate_line_inputs:
                    val = self.line_state[inp_line]
                    if val == -1:
                        inputs_ready = False
                        break
                    input_values.append(val)

                if inputs_ready:
                    result = self.evaluate_gate(g.type, input_values)
                    self.set_line_value(g.gate_line_output, result)
                    evaluated_this_cycle.add(gid)
                    progress = True

            gates_to_evaluate -= evaluated_this_cycle

    def evaluate_gate(self, gate_type, inputs):
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