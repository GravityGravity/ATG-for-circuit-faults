# FILE: log.py

# Description:
#   Contains ENUM type for 5 binary logic 1, 0, X, D, !D
#   Contains truth tables for all gates
#   Contains function calls for all binary logic

from enum import Enum, auto

class L(Enum):
    ZERO = 0
    ONE = 1
    D = (0, 1)  # D (good: 0, faulty: 1)
    D_ = (1, 0)  # Not D (good: 1, fault: 0)
    X = 'X'

class g_types(Enum):  # (controlling value, inversion signal)
    AND = (0, 0)
    OR = (1, 0)
    NOT = (L.X, 1)
    NAND = (0, 1)
    NOR = (1, 1)
    XOR = 'idk'  # fix this


#   Contains all truth table logic for circuit gates excluding NAND and NOR because those gates are just a NOT gate + AND/OR gate
OR_TABLE = {
    (0,0):0, (0,1):1, (0,(0, 1)):(0, 1), (0,(1, 0)):(1, 0), (0,'X'):'X',
    (1,0):1, (1,1):1, (1,(0, 1)):1, (1,(1, 0)):1, (1,'X'):1,
    ((0, 1),0):(0, 1), ((0, 1),1):1, ((0, 1),(0, 1)):(0, 1), ((0, 1),(1, 0)):1, ((0, 1),'X'):'X',
    ((1, 0),0):(1, 0), ((1, 0),1):1, ((1, 0),(0, 1)):1, ((1, 0),(1, 0)):(1, 0), ((1, 0),'X'):'X',
    ('X',0):'X', ('X',1):1, ('X',(0, 1)):'X', ('X',(1, 0)):'X', ('X','X'):'X'
}

AND_TABLE = {
    (0,0):0, (0,1):0, (0,(0, 1)):0, (0,(1, 0)):0, (0,'X'):0,
    (1,0):0, (1,1):1, (1,(0, 1)):(0, 1), (1,(1, 0)):(1, 0), (1,'X'):'X',
    ((0, 1),0):0, ((0, 1),1):(0, 1), ((0, 1),(0, 1)):(0, 1), ((0, 1),(1, 0)):0, ((0, 1),'X'):'X',
    ((1, 0),0):0, ((1, 0),1):(1, 0), ((1, 0),(0, 1)):0, ((1, 0),(1, 0)):(1, 0), ((1, 0),'X'):'X',
    ('X',0):0, ('X',1):'X', ('X',(0, 1)):'X', ('X',(1, 0)):'X', ('X','X'):'X'
}

NOT_TABLE = {
    0:L.ONE,
    1:L.ZERO,
    (0, 1):L.D_,
    (1, 0):L.D,
    'X':L.X
}

XOR_TABLE = {
    (0,0):0, (0,1):1, (0,(0, 1)):(0, 1), (0,(1, 0)):(1, 0), (0,'X'):'X',
    (1,0):1, (1,1):0, (1,(0, 1)):(1, 0), (1,(1, 0)):(0, 1), (1,'X'):'X',
    ((0, 1),0):(0, 1), ((0, 1),1):(1, 0), ((0, 1),(0, 1)):0, ((0, 1),(1, 0)):1, ((0, 1),'X'):'X',
    ((1, 0),0):(1, 0), ((1, 0),1):(0, 1), ((1, 0),(0, 1)):1, ((1, 0),(1, 0)):0, ((1, 0),'X'):'X',
    ('X',0):'X', ('X',1):'X', ('X',(0, 1)):'X', ('X',(1, 0)):'X', ('X','X'):'X'
}


# Gate Operations
def op_or(rand1: L, rand2: L):
    return L(OR_TABLE[(rand1.value, rand2.value)])
    
def op_nor(rand1: L, rand2: L):
   return (NOT_TABLE[OR_TABLE[(rand1.value, rand2.value)]])
    
def op_and(rand1: L, rand2: L):
    return L(AND_TABLE[(rand1.value, rand2.value)])
    
def op_nand(rand1: L, rand2: L):
    return (NOT_TABLE[AND_TABLE[(rand1.value, rand2.value)]])
    
def op_not(rand1: L):
    return L(NOT_TABLE[rand1.value])
