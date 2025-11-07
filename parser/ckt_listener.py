# FILE: ckt_listener.py

from ATGparserListener import ATGparserListener
from ATGparserParser import ATGparserParser
from Circ import Circuit, g_types


class cktlistener(ATGparserListener):

    def __init__(self):
        self.l_circuit = Circuit()

    # Exit a parse tree produced by ATGparserParser#  inputDecl Rule.

    def exitInputDecl(self, ctx: ATGparserParser.InputDeclContext):
        line_label = 'line_' + ctx.ID().getText()
        self.l_circuit.add_line(line_label)
        self.l_circuit.Primary_in.append(line_label)

    # Exit a parse tree produced by ATGparserParser#  outputDecl Rule.

    def exitOutputDecl(self, ctx: ATGparserParser.OutputDeclContext):
        line_label = 'line_' + ctx.ID().getText()
        self.l_circuit.add_line(line_label)
        self.l_circuit.Primary_out.append(line_label)

    # Exit a parse tree produced by ATGparserParser  gateDecl Rule.

    def exitGateDecl(self, ctx: ATGparserParser.GateDeclContext):
        self.l_circuit.add_gate('gate_' + str(len(self.l_circuit.gates) + 1),
                                g_types[ctx.TYPE().getText().upper()], ['line_' + t.getText() for t in ctx.inputs], ('line_' + ctx.output.getText()))
