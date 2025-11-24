<p align="center">
  <img src="images/banner.jpg" 
       alt="ATPG Banner" 
       width="1600">

 # 🔌📐 Automatic Test Pattern Generator (ATPG) for Single Stuck-At Faults
  Final Project — Digital Circuits / VLSI Testing


---

## Overview

This repository contains my Python implementation of an **Automatic Test Pattern Generator (ATPG)** designed to analyze **single stuck-at faults** in combinational circuits.  
The tool reads a gate-level netlist, simulates logic behavior with and without faults, and generates valid test vectors using multiple classical ATPG strategies.

The project was developed as the final assignment for my university **VLSI Testing / Digital Circuits** course.

---

## Features

- **Interactive command-line interface** with options to load circuits, collapse faults, simulate, and generate tests  
- **Single stuck-at fault model** supporting both s-a-0 and s-a-1  
- **ATPG method**:
  - D-Algorithm  
- **Fault collapsing** to reduce redundant faults  
- **Logic and fault simulation** to verify propagation to primary outputs  
- Clear text-based outputs and error handling for invalid inputs or malformed netlists

---

## Getting Started

### Prerequisites


