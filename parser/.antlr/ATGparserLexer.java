// Generated from c:/Users/Work/_repos/VLSI/ATG-for-circuit-faults/parser/ATGparser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class ATGparserLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PI=1, PO=2, END=3, TYPE=4, ID=5, NEWLINE=6, WS=7, COMMENT=8, ERROR=9;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"PI", "PO", "END", "TYPE", "ID", "NEWLINE", "WS", "COMMENT", "ERROR"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'$... primary input'", "'$... primary output'"
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


	public ATGparserLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "ATGparser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\t\u008c\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0003"+
		"\u0002Y\b\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0003\u0003m\b\u0003\u0001\u0004\u0004\u0004p\b\u0004"+
		"\u000b\u0004\f\u0004q\u0001\u0005\u0004\u0005u\b\u0005\u000b\u0005\f\u0005"+
		"v\u0001\u0006\u0004\u0006z\b\u0006\u000b\u0006\f\u0006{\u0001\u0006\u0001"+
		"\u0006\u0001\u0007\u0001\u0007\u0005\u0007\u0082\b\u0007\n\u0007\f\u0007"+
		"\u0085\t\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b"+
		"\u0000\u0000\t\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005"+
		"\u000b\u0006\r\u0007\u000f\b\u0011\t\u0001\u0000\u0003\u0004\u000009A"+
		"Z__az\u0002\u0000\n\n\r\r\u0002\u0000\t\t  \u0095\u0000\u0001\u0001\u0000"+
		"\u0000\u0000\u0000\u0003\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000"+
		"\u0000\u0000\u0000\u0007\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000"+
		"\u0000\u0000\u000b\u0001\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000"+
		"\u0000\u000f\u0001\u0000\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000"+
		"\u0001\u0013\u0001\u0000\u0000\u0000\u0003&\u0001\u0000\u0000\u0000\u0005"+
		":\u0001\u0000\u0000\u0000\u0007l\u0001\u0000\u0000\u0000\to\u0001\u0000"+
		"\u0000\u0000\u000bt\u0001\u0000\u0000\u0000\ry\u0001\u0000\u0000\u0000"+
		"\u000f\u007f\u0001\u0000\u0000\u0000\u0011\u0088\u0001\u0000\u0000\u0000"+
		"\u0013\u0014\u0005$\u0000\u0000\u0014\u0015\u0005.\u0000\u0000\u0015\u0016"+
		"\u0005.\u0000\u0000\u0016\u0017\u0005.\u0000\u0000\u0017\u0018\u0005 "+
		"\u0000\u0000\u0018\u0019\u0005p\u0000\u0000\u0019\u001a\u0005r\u0000\u0000"+
		"\u001a\u001b\u0005i\u0000\u0000\u001b\u001c\u0005m\u0000\u0000\u001c\u001d"+
		"\u0005a\u0000\u0000\u001d\u001e\u0005r\u0000\u0000\u001e\u001f\u0005y"+
		"\u0000\u0000\u001f \u0005 \u0000\u0000 !\u0005i\u0000\u0000!\"\u0005n"+
		"\u0000\u0000\"#\u0005p\u0000\u0000#$\u0005u\u0000\u0000$%\u0005t\u0000"+
		"\u0000%\u0002\u0001\u0000\u0000\u0000&\'\u0005$\u0000\u0000\'(\u0005."+
		"\u0000\u0000()\u0005.\u0000\u0000)*\u0005.\u0000\u0000*+\u0005 \u0000"+
		"\u0000+,\u0005p\u0000\u0000,-\u0005r\u0000\u0000-.\u0005i\u0000\u0000"+
		"./\u0005m\u0000\u0000/0\u0005a\u0000\u000001\u0005r\u0000\u000012\u0005"+
		"y\u0000\u000023\u0005 \u0000\u000034\u0005o\u0000\u000045\u0005u\u0000"+
		"\u000056\u0005t\u0000\u000067\u0005p\u0000\u000078\u0005u\u0000\u0000"+
		"89\u0005t\u0000\u00009\u0004\u0001\u0000\u0000\u0000:;\u0005$\u0000\u0000"+
		";<\u0005 \u0000\u0000<=\u0005e\u0000\u0000=>\u0005n\u0000\u0000>?\u0005"+
		"d\u0000\u0000?@\u0005 \u0000\u0000@A\u0005o\u0000\u0000AB\u0005f\u0000"+
		"\u0000BC\u0005 \u0000\u0000CD\u0005c\u0000\u0000DE\u0005i\u0000\u0000"+
		"EF\u0005r\u0000\u0000FG\u0005c\u0000\u0000GH\u0005u\u0000\u0000HI\u0005"+
		"i\u0000\u0000IJ\u0005t\u0000\u0000JK\u0005 \u0000\u0000KL\u0005d\u0000"+
		"\u0000LM\u0005e\u0000\u0000MN\u0005s\u0000\u0000NO\u0005c\u0000\u0000"+
		"OP\u0005r\u0000\u0000PQ\u0005i\u0000\u0000QR\u0005p\u0000\u0000RS\u0005"+
		"t\u0000\u0000ST\u0005i\u0000\u0000TU\u0005o\u0000\u0000UV\u0005n\u0000"+
		"\u0000VX\u0001\u0000\u0000\u0000WY\u0003\u000b\u0005\u0000XW\u0001\u0000"+
		"\u0000\u0000XY\u0001\u0000\u0000\u0000Y\u0006\u0001\u0000\u0000\u0000"+
		"Z[\u0005a\u0000\u0000[\\\u0005n\u0000\u0000\\m\u0005d\u0000\u0000]^\u0005"+
		"n\u0000\u0000^_\u0005a\u0000\u0000_`\u0005n\u0000\u0000`m\u0005d\u0000"+
		"\u0000ab\u0005o\u0000\u0000bm\u0005r\u0000\u0000cd\u0005n\u0000\u0000"+
		"de\u0005o\u0000\u0000em\u0005r\u0000\u0000fg\u0005n\u0000\u0000gh\u0005"+
		"o\u0000\u0000hm\u0005t\u0000\u0000ij\u0005x\u0000\u0000jk\u0005o\u0000"+
		"\u0000km\u0005r\u0000\u0000lZ\u0001\u0000\u0000\u0000l]\u0001\u0000\u0000"+
		"\u0000la\u0001\u0000\u0000\u0000lc\u0001\u0000\u0000\u0000lf\u0001\u0000"+
		"\u0000\u0000li\u0001\u0000\u0000\u0000m\b\u0001\u0000\u0000\u0000np\u0007"+
		"\u0000\u0000\u0000on\u0001\u0000\u0000\u0000pq\u0001\u0000\u0000\u0000"+
		"qo\u0001\u0000\u0000\u0000qr\u0001\u0000\u0000\u0000r\n\u0001\u0000\u0000"+
		"\u0000su\u0007\u0001\u0000\u0000ts\u0001\u0000\u0000\u0000uv\u0001\u0000"+
		"\u0000\u0000vt\u0001\u0000\u0000\u0000vw\u0001\u0000\u0000\u0000w\f\u0001"+
		"\u0000\u0000\u0000xz\u0007\u0002\u0000\u0000yx\u0001\u0000\u0000\u0000"+
		"z{\u0001\u0000\u0000\u0000{y\u0001\u0000\u0000\u0000{|\u0001\u0000\u0000"+
		"\u0000|}\u0001\u0000\u0000\u0000}~\u0006\u0006\u0000\u0000~\u000e\u0001"+
		"\u0000\u0000\u0000\u007f\u0083\u0005$\u0000\u0000\u0080\u0082\b\u0001"+
		"\u0000\u0000\u0081\u0080\u0001\u0000\u0000\u0000\u0082\u0085\u0001\u0000"+
		"\u0000\u0000\u0083\u0081\u0001\u0000\u0000\u0000\u0083\u0084\u0001\u0000"+
		"\u0000\u0000\u0084\u0086\u0001\u0000\u0000\u0000\u0085\u0083\u0001\u0000"+
		"\u0000\u0000\u0086\u0087\u0006\u0007\u0000\u0000\u0087\u0010\u0001\u0000"+
		"\u0000\u0000\u0088\u0089\t\u0000\u0000\u0000\u0089\u008a\u0001\u0000\u0000"+
		"\u0000\u008a\u008b\u0006\b\u0000\u0000\u008b\u0012\u0001\u0000\u0000\u0000"+
		"\u0007\u0000Xlqv{\u0083\u0001\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}