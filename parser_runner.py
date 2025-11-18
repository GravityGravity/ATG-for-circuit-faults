
from antlr4 import *
from parser.ATGparserLexer import ATGparserLexer
from parser.ATGparserParser import ATGparserParser
from parser.ckt_listener import cktlistener


def parse_circuit(file_path: str, circuit_name: str = "circuit_default_name"):
    """
    Parse a .ckt file and return a fully built Circuit object.
    """

    # Load the file into ANTLR
    input_stream = FileStream(file_path, encoding="utf-8")

    # Create lexer → token stream
    lexer = ATGparserLexer(input_stream)
    tokens = CommonTokenStream(lexer)

    # Create parser
    parser = ATGparserParser(tokens)

    # Your starting rule (IMPORTANT)
    tree = parser.program()

    # Walk with listener
    listener = cktlistener(circuit_name)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Return the circuit model
    return listener.l_circuit
