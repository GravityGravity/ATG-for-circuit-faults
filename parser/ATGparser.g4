/* FILE: ATGparser.g4

   Description:
       Parses .ckt file formats and creates a circuit data structure
       that is used by ATG.py (full-adder example, etc.)
*/

grammar ATGparser;

// ---------- PARSER RULES ----------

program
  : ( inputDecl
    | outputDecl
    | gateDecl
    | NEWLINE               // completely empty line
    )* 
    END? 
    EOF
  ;

// X                   $ ... primary input
inputDecl
  : ID PI NEWLINE
  ;

// S                   $ ... primary output
outputDecl
  : ID PO NEWLINE
  ;

// L    nand    X  Y
gateDecl
  : output=ID type=TYPE inputs+=ID+ NEWLINE
  ;

// ---------- LEXER RULES ----------

// Match things like: "$ ... primary input" (any junk before/after the phrase)
PI
  : '$' ~[\r\n]* [pP][rR][iI][mM][aA][rR][yY] [ \t]+ [iI][nN][pP][uU][tT] ~[\r\n]*
  ;

// Match things like: "$ ... primary output"
PO
  : '$' ~[\r\n]* [pP][rR][iI][mM][aA][rR][yY] [ \t]+ [oO][uU][tT][pP][uU][tT] ~[\r\n]*
  ;

// Optional end-of-circuit marker:
// $ end of circuit description
END
  : '$' [ \t]* [eE][nN][dD] [ \t]+ [oO][fF] [ \t]+ [cC][iI][rR][cC][uU][iI][tT] [ \t]+ [dD][eE][sS][cC][rR][iI][pP][tT][iI][oO][nN] ~[\r\n]* 
  ;

// Gate type keywords (case-insensitive)
TYPE
  : [aA][nN][dD]
  | [nN][aA][nN][dD]
  | [oO][rR]
  | [nN][oO][rR]
  | [nN][oO][tT]
  | [xX][oO][rR]
  ;

// Wire / line / gate identifiers
ID
  : [a-zA-Z_0-9]+
  ;

// Handle any platform’s newline: \r\n (Windows), \n (Unix), \r (old Mac)
NEWLINE
  : ('\r\n' | '\n' | '\r')+
  ;

// Spaces and tabs between tokens
WS
  : [ \t]+ -> skip
  ;

// Any other $-line that is NOT PI/PO/END is just a comment to skip
COMMENT
  : '$' ~[\r\n]* -> skip
  ;

// Last-resort catch-all (optional, but keeps the lexer from blowing up)
ERROR
  : . -> skip
  ;