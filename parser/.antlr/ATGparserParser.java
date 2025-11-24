// Generated from c:/Users/Work/_repos/VLSI/ATG-for-circuit-faults/parser/ATGparser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ATGparserParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PI=1, PO=2, END=3, TYPE=4, ID=5, NEWLINE=6, WS=7, COMMENT=8, ERROR=9;
	public static final int
		RULE_program = 0, RULE_inputDecl = 1, RULE_outputDecl = 2, RULE_gateDecl = 3;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "inputDecl", "outputDecl", "gateDecl"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "PI", "PO", "END", "TYPE", "ID", "NEWLINE", "WS", "COMMENT", "ERROR"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "ATGparser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ATGparserParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(ATGparserParser.EOF, 0); }
		public List<InputDeclContext> inputDecl() {
			return getRuleContexts(InputDeclContext.class);
		}
		public InputDeclContext inputDecl(int i) {
			return getRuleContext(InputDeclContext.class,i);
		}
		public List<OutputDeclContext> outputDecl() {
			return getRuleContexts(OutputDeclContext.class);
		}
		public OutputDeclContext outputDecl(int i) {
			return getRuleContext(OutputDeclContext.class,i);
		}
		public List<GateDeclContext> gateDecl() {
			return getRuleContexts(GateDeclContext.class);
		}
		public GateDeclContext gateDecl(int i) {
			return getRuleContext(GateDeclContext.class,i);
		}
		public List<TerminalNode> NEWLINE() { return getTokens(ATGparserParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(ATGparserParser.NEWLINE, i);
		}
		public TerminalNode END() { return getToken(ATGparserParser.END, 0); }
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(14);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ID || _la==NEWLINE) {
				{
				setState(12);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
				case 1:
					{
					setState(8);
					inputDecl();
					}
					break;
				case 2:
					{
					setState(9);
					outputDecl();
					}
					break;
				case 3:
					{
					setState(10);
					gateDecl();
					}
					break;
				case 4:
					{
					setState(11);
					match(NEWLINE);
					}
					break;
				}
				}
				setState(16);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(18);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==END) {
				{
				setState(17);
				match(END);
				}
			}

			setState(20);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InputDeclContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ATGparserParser.ID, 0); }
		public TerminalNode PI() { return getToken(ATGparserParser.PI, 0); }
		public TerminalNode NEWLINE() { return getToken(ATGparserParser.NEWLINE, 0); }
		public InputDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_inputDecl; }
	}

	public final InputDeclContext inputDecl() throws RecognitionException {
		InputDeclContext _localctx = new InputDeclContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_inputDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(22);
			match(ID);
			setState(23);
			match(PI);
			setState(24);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class OutputDeclContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ATGparserParser.ID, 0); }
		public TerminalNode PO() { return getToken(ATGparserParser.PO, 0); }
		public TerminalNode NEWLINE() { return getToken(ATGparserParser.NEWLINE, 0); }
		public OutputDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_outputDecl; }
	}

	public final OutputDeclContext outputDecl() throws RecognitionException {
		OutputDeclContext _localctx = new OutputDeclContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_outputDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(26);
			match(ID);
			setState(27);
			match(PO);
			setState(28);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class GateDeclContext extends ParserRuleContext {
		public Token output;
		public Token type;
		public Token ID;
		public List<Token> inputs = new ArrayList<Token>();
		public TerminalNode NEWLINE() { return getToken(ATGparserParser.NEWLINE, 0); }
		public List<TerminalNode> ID() { return getTokens(ATGparserParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ATGparserParser.ID, i);
		}
		public TerminalNode TYPE() { return getToken(ATGparserParser.TYPE, 0); }
		public GateDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_gateDecl; }
	}

	public final GateDeclContext gateDecl() throws RecognitionException {
		GateDeclContext _localctx = new GateDeclContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_gateDecl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(30);
			((GateDeclContext)_localctx).output = match(ID);
			setState(31);
			((GateDeclContext)_localctx).type = match(TYPE);
			setState(33); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(32);
				((GateDeclContext)_localctx).ID = match(ID);
				((GateDeclContext)_localctx).inputs.add(((GateDeclContext)_localctx).ID);
				}
				}
				setState(35); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			setState(37);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\t(\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0005\u0000\r\b\u0000\n\u0000\f\u0000\u0010\t\u0000"+
		"\u0001\u0000\u0003\u0000\u0013\b\u0000\u0001\u0000\u0001\u0000\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0004\u0003\"\b\u0003"+
		"\u000b\u0003\f\u0003#\u0001\u0003\u0001\u0003\u0001\u0003\u0000\u0000"+
		"\u0004\u0000\u0002\u0004\u0006\u0000\u0000)\u0000\u000e\u0001\u0000\u0000"+
		"\u0000\u0002\u0016\u0001\u0000\u0000\u0000\u0004\u001a\u0001\u0000\u0000"+
		"\u0000\u0006\u001e\u0001\u0000\u0000\u0000\b\r\u0003\u0002\u0001\u0000"+
		"\t\r\u0003\u0004\u0002\u0000\n\r\u0003\u0006\u0003\u0000\u000b\r\u0005"+
		"\u0006\u0000\u0000\f\b\u0001\u0000\u0000\u0000\f\t\u0001\u0000\u0000\u0000"+
		"\f\n\u0001\u0000\u0000\u0000\f\u000b\u0001\u0000\u0000\u0000\r\u0010\u0001"+
		"\u0000\u0000\u0000\u000e\f\u0001\u0000\u0000\u0000\u000e\u000f\u0001\u0000"+
		"\u0000\u0000\u000f\u0012\u0001\u0000\u0000\u0000\u0010\u000e\u0001\u0000"+
		"\u0000\u0000\u0011\u0013\u0005\u0003\u0000\u0000\u0012\u0011\u0001\u0000"+
		"\u0000\u0000\u0012\u0013\u0001\u0000\u0000\u0000\u0013\u0014\u0001\u0000"+
		"\u0000\u0000\u0014\u0015\u0005\u0000\u0000\u0001\u0015\u0001\u0001\u0000"+
		"\u0000\u0000\u0016\u0017\u0005\u0005\u0000\u0000\u0017\u0018\u0005\u0001"+
		"\u0000\u0000\u0018\u0019\u0005\u0006\u0000\u0000\u0019\u0003\u0001\u0000"+
		"\u0000\u0000\u001a\u001b\u0005\u0005\u0000\u0000\u001b\u001c\u0005\u0002"+
		"\u0000\u0000\u001c\u001d\u0005\u0006\u0000\u0000\u001d\u0005\u0001\u0000"+
		"\u0000\u0000\u001e\u001f\u0005\u0005\u0000\u0000\u001f!\u0005\u0004\u0000"+
		"\u0000 \"\u0005\u0005\u0000\u0000! \u0001\u0000\u0000\u0000\"#\u0001\u0000"+
		"\u0000\u0000#!\u0001\u0000\u0000\u0000#$\u0001\u0000\u0000\u0000$%\u0001"+
		"\u0000\u0000\u0000%&\u0005\u0006\u0000\u0000&\u0007\u0001\u0000\u0000"+
		"\u0000\u0004\f\u000e\u0012#";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}