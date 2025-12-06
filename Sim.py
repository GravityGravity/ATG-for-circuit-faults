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
        self.faultVectorInput = ""
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

        # 2. Get Fault Vector List
        print(f"    {cl.Style.DIM}(Optional) Enter list of Fault Vectors (e.g., {{0000, 0011}} or just 0000).{cl.Style.RESET_ALL}")
        print(
            f"    {cl.Style.DIM}Use '0'/'1' for faults, 'X' for none.{cl.Style.RESET_ALL}")
        self.faultVectorInput = input(
            f'    {cl.Back.WHITE} > INPUT FAULT LIST > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}'
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
        if not self.faultVectorInput:
            return

        # ==========================================
        # 2. Parse Fault List
        # ==========================================
        # Clean the input: remove braces and split by comma
        cleaned_input = self.faultVectorInput.replace('{', '').replace('}', '')

        # Handle empty case after strip
        if not cleaned_input:
            return

        raw_list = cleaned_input.split(',')
        fault_vectors = [v.strip() for v in raw_list if v.strip()]

        print(f"\n{cl.Fore.CYAN}--- Running Fault Simulations ({len(fault_vectors)} vectors) ---{cl.Style.RESET_ALL}")

        faults_detected = 0

        # ==========================================
        # 3. Iterate Through Each Fault Vector
        # ==========================================
        for f_vec in fault_vectors:
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
                # Optional: Verbose output for undetected
                # print(f"  [Undetected] Fault Vector: {f_vec} | Output: {bad_output}")
                pass

        if faults_detected == 0:
            print(
                f"{cl.Fore.YELLOW}No faults detected by any provided vector.{cl.Style.RESET_ALL}")
        else:
            print(
                f"{cl.Fore.GREEN}Total Fault Vectors Detected: {faults_detected}{cl.Style.RESET_ALL}")

    def run_single_pass(self, sorted_inputs, vector_str, fault_mask=None):
        """
        Runs a single simulation pass.
        Args:
            sorted_inputs: list of PI names
            vector_str: string of 0s and 1s (Good Values)
            fault_mask: (Optional) string of 0s, 1s, and Xs. 
                        '0'/'1' overrides the input to that value.
                        'X' (or anything else) leaves the original vector_str value.
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

                # INJECT FAULT MASK
                # If a fault mask is provided, check the character at this index
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
