/* FILE: ATGparser.g4

    Description:
        Parses .ckt file formats and creates a circuit data structure that is used by ATG.py
 */
 
grammar ATGparser;

// ---------- PARSER RULES ----------
program
  : (inputDecl | outputDecl | gateDecl | NEWLINE)* END? EOF
  ;

inputDecl   : ID PI NEWLINE ;
outputDecl  : ID PO NEWLINE ;
gateDecl    : output=ID type=TYPE inputs+=ID+ NEWLINE ;   // out type in1 in2

// ---------- LEXER RULES ----------
PI   : '$... primary input' ;
PO   : '$... primary output' ;
END  : '$ end of circuit description' NEWLINE? ;

TYPE : 'and' | 'nand' | 'or' | 'nor' | 'not' | 'xor' ;

ID       : [a-zA-Z_][a-zA-Z_0-9]* ;
NEWLINE  : [\r\n]+ ;
WS       : [ \t]+ -> skip ;

// Any other $-line is a comment: "$ blah blah"
COMMENT  : '$' ~[\r\n]* -> skip ;
ERROR    : . -> skip ;
