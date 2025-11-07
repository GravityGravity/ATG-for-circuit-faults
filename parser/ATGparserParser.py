# Generated from parser/ATGparser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,9,37,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,0,1,0,5,0,13,
        8,0,10,0,12,0,16,9,0,1,0,3,0,19,8,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,
        1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,0,0,4,0,2,4,6,0,0,37,0,14,
        1,0,0,0,2,22,1,0,0,0,4,26,1,0,0,0,6,30,1,0,0,0,8,13,3,2,1,0,9,13,
        3,4,2,0,10,13,3,6,3,0,11,13,5,6,0,0,12,8,1,0,0,0,12,9,1,0,0,0,12,
        10,1,0,0,0,12,11,1,0,0,0,13,16,1,0,0,0,14,12,1,0,0,0,14,15,1,0,0,
        0,15,18,1,0,0,0,16,14,1,0,0,0,17,19,5,3,0,0,18,17,1,0,0,0,18,19,
        1,0,0,0,19,20,1,0,0,0,20,21,5,0,0,1,21,1,1,0,0,0,22,23,5,5,0,0,23,
        24,5,1,0,0,24,25,5,6,0,0,25,3,1,0,0,0,26,27,5,5,0,0,27,28,5,2,0,
        0,28,29,5,6,0,0,29,5,1,0,0,0,30,31,5,5,0,0,31,32,5,4,0,0,32,33,5,
        5,0,0,33,34,5,5,0,0,34,35,5,6,0,0,35,7,1,0,0,0,3,12,14,18
    ]

class ATGparserParser ( Parser ):

    grammarFileName = "ATGparser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'$... primary input'", "'$... primary output'" ]

    symbolicNames = [ "<INVALID>", "PI", "PO", "END", "TYPE", "ID", "NEWLINE", 
                      "WS", "COMMENT", "ERROR" ]

    RULE_program = 0
    RULE_inputDecl = 1
    RULE_outputDecl = 2
    RULE_gateDecl = 3

    ruleNames =  [ "program", "inputDecl", "outputDecl", "gateDecl" ]

    EOF = Token.EOF
    PI=1
    PO=2
    END=3
    TYPE=4
    ID=5
    NEWLINE=6
    WS=7
    COMMENT=8
    ERROR=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ATGparserParser.EOF, 0)

        def inputDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ATGparserParser.InputDeclContext)
            else:
                return self.getTypedRuleContext(ATGparserParser.InputDeclContext,i)


        def outputDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ATGparserParser.OutputDeclContext)
            else:
                return self.getTypedRuleContext(ATGparserParser.OutputDeclContext,i)


        def gateDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ATGparserParser.GateDeclContext)
            else:
                return self.getTypedRuleContext(ATGparserParser.GateDeclContext,i)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(ATGparserParser.NEWLINE)
            else:
                return self.getToken(ATGparserParser.NEWLINE, i)

        def END(self):
            return self.getToken(ATGparserParser.END, 0)

        def getRuleIndex(self):
            return ATGparserParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = ATGparserParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5 or _la==6:
                self.state = 12
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 8
                    self.inputDecl()
                    pass

                elif la_ == 2:
                    self.state = 9
                    self.outputDecl()
                    pass

                elif la_ == 3:
                    self.state = 10
                    self.gateDecl()
                    pass

                elif la_ == 4:
                    self.state = 11
                    self.match(ATGparserParser.NEWLINE)
                    pass


                self.state = 16
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 18
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 17
                self.match(ATGparserParser.END)


            self.state = 20
            self.match(ATGparserParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InputDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ATGparserParser.ID, 0)

        def PI(self):
            return self.getToken(ATGparserParser.PI, 0)

        def NEWLINE(self):
            return self.getToken(ATGparserParser.NEWLINE, 0)

        def getRuleIndex(self):
            return ATGparserParser.RULE_inputDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInputDecl" ):
                listener.enterInputDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInputDecl" ):
                listener.exitInputDecl(self)




    def inputDecl(self):

        localctx = ATGparserParser.InputDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_inputDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(ATGparserParser.ID)
            self.state = 23
            self.match(ATGparserParser.PI)
            self.state = 24
            self.match(ATGparserParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ATGparserParser.ID, 0)

        def PO(self):
            return self.getToken(ATGparserParser.PO, 0)

        def NEWLINE(self):
            return self.getToken(ATGparserParser.NEWLINE, 0)

        def getRuleIndex(self):
            return ATGparserParser.RULE_outputDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOutputDecl" ):
                listener.enterOutputDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOutputDecl" ):
                listener.exitOutputDecl(self)




    def outputDecl(self):

        localctx = ATGparserParser.OutputDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_outputDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self.match(ATGparserParser.ID)
            self.state = 27
            self.match(ATGparserParser.PO)
            self.state = 28
            self.match(ATGparserParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GateDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(ATGparserParser.ID)
            else:
                return self.getToken(ATGparserParser.ID, i)

        def TYPE(self):
            return self.getToken(ATGparserParser.TYPE, 0)

        def NEWLINE(self):
            return self.getToken(ATGparserParser.NEWLINE, 0)

        def getRuleIndex(self):
            return ATGparserParser.RULE_gateDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGateDecl" ):
                listener.enterGateDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGateDecl" ):
                listener.exitGateDecl(self)




    def gateDecl(self):

        localctx = ATGparserParser.GateDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_gateDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(ATGparserParser.ID)
            self.state = 31
            self.match(ATGparserParser.TYPE)
            self.state = 32
            self.match(ATGparserParser.ID)
            self.state = 33
            self.match(ATGparserParser.ID)
            self.state = 34
            self.match(ATGparserParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





