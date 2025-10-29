grammar parse;

// Parser
program : ;
input : ID TYPE ;
output : ID PO ;

// Lexer of ANTLR 4
PI : '$ ... primary input' ;
PO : '$ ... primary output' ;
COMMENT : '$'[.]* ;
TYPE : 'and' | 'nand' | 'or' | 'nor' | 'not' | 'xor' ;
WS : [ \t\r\n]+ -> skip;
ID : [a-zA-Z_][a-zA-Z_0-9]* ;
ERROR : . -> skip;