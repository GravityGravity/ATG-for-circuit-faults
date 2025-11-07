# FILE: ckt_listener.py

from ATGparserListener import ATGparserListener
from ATGparserParser import ATGparserParser
from Circ import Circuit


class cktlistener(ATGparserListener):

    def __init__(self):
        self.l_circuit = Circuit()

    # Exit a parse tree produced by ATGparserParser#inputDecl.

    def exitInputDecl(self, ctx: ATGparserParser.InputDeclContext):
        pass

    # Exit a parse tree produced by ATGparserParser#outputDecl.

    def exitOutputDecl(self, ctx: ATGparserParser.OutputDeclContext):
        pass

    # Exit a parse tree produced by ATGparserParser#gateDecl.

    def exitGateDecl(self, ctx: ATGparserParser.GateDeclContext):
        pass
