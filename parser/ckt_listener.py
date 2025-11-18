# FILE: ckt_listener.py

from parser.ATGparserListener import ATGparserListener
from parser.ATGparserParser import ATGparserParser
from Circ import Circuit, g_types


class cktlistener(ATGparserListener):

    def __init__(self, circuitName):
        super().__init__()
        self.l_circuit = Circuit(circuitName)
        # debug print
        print(
            f' ---PARSING--- (ckt_listener.py created circuit {circuitName})\n')

    # Exit a parse tree produced by ATGparserParser#  inputDecl Rule.

    def exitInputDecl(self, ctx: ATGparserParser.InputDeclContext):
        line_label = 'line_' + ctx.ID().getText()  # .upper()
        self.l_circuit.add_line(line_label)
        self.l_circuit.Primary_in.add(line_label)

    # Exit a parse tree produced by ATGparserParser#  outputDecl Rule.

    def exitOutputDecl(self, ctx: ATGparserParser.OutputDeclContext):
        line_label = 'line_' + ctx.ID().getText()
        self.l_circuit.add_line(line_label)
        self.l_circuit.Primary_out.add(line_label)

    # Exit a parse tree produced by ATGparserParser  gateDecl Rule.

    def exitGateDecl(self, ctx: ATGparserParser.GateDeclContext):

        self.l_circuit.add_gate(('gate_' + len(self.l_circuit.gates) + 1),
                                # <-------- POSSIBLE ERROR
                                g_types[ctx.type_.text.upper()].name,
                                ['line_' + t.getText() for t in ctx.inputs],
                                ('line_' + ctx.output.getText()))
