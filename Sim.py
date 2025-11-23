# File: Sim.py
# Implemented by: St4rmanxz

import os
import sys
import ATG

# Contains circuit structure
import Circ

# Contains logic tables for gates (Includes D and Not D values)
from B_logic import *


class Sim:

    circuit = ATG.selected_circuit

    def __init__(self, testVector="000", circuit=None):
        self.testVector = testVector
        if circuit is None:
            circuit = ATG.selected_circuit

    def promptForParameters(self):
        print("Simulation Parameters:")
        print("PLEASE INPUT TEST VECTOR:")
        testVector = input()
        return testVector
    

    def Run(self):
        self.circuit = ATG.selected_circuit
        self.simulate_circuit()
        finalOutput = ""
        for i in self.circuit.outPut:
            finalOutput = finalOutput + str(self.circuit.ioList[str(i)])
        print("Output : " + finalOutput)


    def simulate_circuit(self):
        evaluate_gates = []
        while self.circuit.gates:
            self.find_ready_gates(evaluate_gates)
            self.evaluate_ready_gates(evaluate_gates)
    
    def find_ready_gates(self, evaluate_gates):
        for gate in self.circuit.gates:
            ready = True
            for inp in gate.inputs:
                if self.circuit.ioList[inp] == -1:
                    ready = False
                    break
            if ready:
                evaluate_gates.append(gate)
                self.circuit.gates.remove(gate)
    
    def evaluate_ready_gates(self, evaluate_gates):
        for gate in evaluate_gates:
            if gate.gate_type == "INV":
                self.circuit.ioList[gate.output] = int(not self.circuit.ioList[gate.inputs[0]])
            elif gate.gate_type == "BUF":
                self.circuit.ioList[gate.output] = int(self.circuit.ioList[gate.inputs[0]])
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

