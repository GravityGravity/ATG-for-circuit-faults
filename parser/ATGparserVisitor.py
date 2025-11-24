# Generated from ./parser/ATGparser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ATGparserParser import ATGparserParser
else:
    from ATGparserParser import ATGparserParser

# This class defines a complete generic visitor for a parse tree produced by ATGparserParser.

class ATGparserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ATGparserParser#program.
    def visitProgram(self, ctx:ATGparserParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ATGparserParser#inputDecl.
    def visitInputDecl(self, ctx:ATGparserParser.InputDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ATGparserParser#outputDecl.
    def visitOutputDecl(self, ctx:ATGparserParser.OutputDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ATGparserParser#gateDecl.
    def visitGateDecl(self, ctx:ATGparserParser.GateDeclContext):
        return self.visitChildren(ctx)



del ATGparserParser