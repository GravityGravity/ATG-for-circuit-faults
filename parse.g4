/* FILE: parse.g4

    Description:
        Parses .ckt file formats and creates a circuit data structure that is used by ATG.py
 */
grammar parse;

// Parser Rules
program : ;
input : ID PI NEWLINE;
output : ID PO NEWLINE;
gate : ID TYPE ID ID NEWLINE | ID TYPE ID ID END;


// Lexer Rules
PI : '$... primary input' ;
PO : '$... primary output' ;
END : '$ end of circuit description' ;
COMMENT : '$'[.]+ ;
TYPE : 'and' | 'nand' | 'or' | 'nor' | 'not' | 'xor' ;
WS : [ \t\r]+ -> skip;
ID : [a-zA-Z_][a-zA-Z_0-9]* ;
NEWLINE : [\n]+;
ERROR : [.] -> skip;