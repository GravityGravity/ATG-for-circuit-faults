# Generated from ./parser/ATGparser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ATGparserParser import ATGparserParser
else:
    from ATGparserParser import ATGparserParser

# This class defines a complete listener for a parse tree produced by ATGparserParser.
class ATGparserListener(ParseTreeListener):

    # Enter a parse tree produced by ATGparserParser#program.
    def enterProgram(self, ctx:ATGparserParser.ProgramContext):
        pass

    # Exit a parse tree produced by ATGparserParser#program.
    def exitProgram(self, ctx:ATGparserParser.ProgramContext):
        pass


    # Enter a parse tree produced by ATGparserParser#inputDecl.
    def enterInputDecl(self, ctx:ATGparserParser.InputDeclContext):
        pass

    # Exit a parse tree produced by ATGparserParser#inputDecl.
    def exitInputDecl(self, ctx:ATGparserParser.InputDeclContext):
        pass


    # Enter a parse tree produced by ATGparserParser#outputDecl.
    def enterOutputDecl(self, ctx:ATGparserParser.OutputDeclContext):
        pass

    # Exit a parse tree produced by ATGparserParser#outputDecl.
    def exitOutputDecl(self, ctx:ATGparserParser.OutputDeclContext):
        pass


    # Enter a parse tree produced by ATGparserParser#gateDecl.
    def enterGateDecl(self, ctx:ATGparserParser.GateDeclContext):
        pass

    # Exit a parse tree produced by ATGparserParser#gateDecl.
    def exitGateDecl(self, ctx:ATGparserParser.GateDeclContext):
        pass



del ATGparserParser