from wasmer import wat2wasm
from rply import LexerGenerator
from parse_def import parser


lg = LexerGenerator()

lg.add("IMPORT", r"import(?!\w)")
lg.add("EXPORT", r"export(?!\w)")
lg.add("AS", r"as(?!\w)")
lg.add("LAMBDA", r"lambda(?!\w)")
lg.add("MEMORY", r"memory(?!\w)")
lg.add("RETURN", r"return(?!\w)")
lg.add("DEF", r"def(?!\w)")
lg.add("LET", r"let(?!\w)")
lg.add("STORE8", r"store8(?!\w)")
lg.add("LOAD8", r"load8(?!\w)")
lg.add("FOR", r"for(?!\w)")
lg.add("IN", r"in(?!\w)")
lg.add("RANGE", r"range(?!\w)")
lg.add("IF", r"if(?!\w)")
lg.add("ELSE", r"else(?!\w)")
lg.add("LPAR", r"\(")
lg.add("RPAR", r"\)")
lg.add("LBRACE", r"\{")
lg.add("RBRACE", r"\}")
lg.add("LSQRBRACE", r"\[")
lg.add("RSQRBRACE", r"\]")
lg.add("COLON", r"\:")
lg.add("SEMICOLON", r"\;")
lg.add("DOT", r"\.")
lg.add("RIGHT_ARROW", "->")
lg.add("COMMA", r"\,")
lg.add("AND", "&&")
lg.add("BINEQUAL", "==")
lg.add("BINNOTEQUAL", "!=")
lg.add("BINLSS", r"<(?!=)")
lg.add("BINGTR", r">(?!=)")
lg.add("BINLSSEQUAL", "<=")
lg.add("BINGTREQUAL", ">=")
lg.add("EQUALS", "=")
lg.add("PLUS", r"\+")
lg.add("MINUS", r"\-")
lg.add("MOD", r"\%")
lg.add("MUL", r"\*")
lg.add("DIV", r"/")
lg.add("INT", r"\d+")
lg.add("IDENTIFIER", r"[a-z-A-Z0-9_]\w*")
lg.add("COMMENT", r"#.*")
lg.ignore(r"\s+")


# load the contents of the source file
with open("./lang/purple.ptr", "r") as f:
    src = f.read()

lexer = lg.build()
# for tok in lexer.lex(src):
#     print(tok)

wat_text = parser.parse(lexer.lex(src)).eval()
# print("The wat output text")
# print(wat_text)

with open("main.wat", "w") as f:
    f.write(wat_text)

data = wat2wasm(wat_text)
print(data)

with open("main.wasm", "wb") as f:
    f.write(data)