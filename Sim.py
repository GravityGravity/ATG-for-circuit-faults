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

    def __init__(self, testVector="000", circuit: Circuit = None):
        self.testVector = testVector
        self.circuit = circuit
        self.eval_gates: list = []

    def promptForParameters(self):
        print("Simulation Parameters:")

        testVector = input(
            f'    {cl.Back.WHITE} > INPUT TEST VECTOR > {cl.Back.RESET}\n{cl.Fore.YELLOW} ATG.py>> SIM> {cl.Style.RESET_ALL}')

        return testVector

    def Run(self):
        self.simulate_circuit()
        finalOutput = ""
        for i in self.circuit.Primary_out:
            finalOutput = finalOutput + str(self.circuit.ioList[str(i)])
        print("Output : " + finalOutput)

    def simulate_circuit(self):
        self.eval_gates: list = []
        while self.circuit.gates:
            # <--- added type hints
            self.find_ready_gates()
            self.evaluate_ready_gates()

    def find_ready_gates(self):
        for g_name, g in self.circuit.gates.items():
            ready = True
            for inp in g.gate_line_inputs:
                if self.circuit.ioList[inp] == -1:
                    ready = False
                    break
            if ready:
                # <------ Cant use exact name 'gate' as gate is a class type
                self.eval_gates.append(g)
                # <------ Cant use exact name 'gate' as gate is a class type
                self.circuit.gates.remove(g)

    def evaluate_ready_gates(self):
        for gate in self.eval_gates:
            if gate.gate_type == "INV":
                self.circuit.ioList[gate.output] = int(
                    not self.circuit.ioList[gate.inputs[0]])
            elif gate.gate_type == "BUF":
                self.circuit.ioList[gate.output] = int(
                    self.circuit.ioList[gate.inputs[0]])
            elif gate.gate_type == "AND":
                self.circuit.ioList[gate.output] = int(
                    self.circuit.ioList[gate.inputs[0]] & self.circuit.ioList[gate.inputs[1]])
            elif gate.gate_type == "NAND":
                self.circuit.ioList[gate.output] = int(
                    not (self.circuit.ioList[gate.inputs[0]] and self.circuit.ioList[gate.inputs[1]]))
            elif gate.gate_type == "NOR":
                self.circuit.ioList[gate.output] = int(
                    not (self.circuit.ioList[gate.inputs[0]] or self.circuit.ioList[gate.inputs[1]]))
            elif gate.gate_type == "OR":
                self.circuit.ioList[gate.output] = int(
                    self.circuit.ioList[gate.inputs[0]] or self.circuit.ioList[gate.inputs[1]])
