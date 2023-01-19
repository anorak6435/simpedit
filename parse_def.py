from rply import ParserGenerator
from ast_def import *

pg = ParserGenerator(["IMPORT", "EXPORT", "AS", "LAMBDA", "DEF", "LET", "MEM", "FOR", "IN", "RANGE", "IF", "ELSE", "RPAR", "LPAR", "LBRACE", "RBRACE", "LSQRBRACE", "RSQRBRACE", "MEMORY", "DOT", "COMMA", "BINEQUAL", "BINNOTEQUAL", "BINLSS", "BINGTR", "BINLSSEQUAL", "BINGTREQUAL", "EQUALS", "PLUS", "MINUS", "MUL", "DIV", "INT", "IDENTIFIER", "COLON", "SEMICOLON", "RIGHT_ARROW", "COMMENT"])


@pg.production("modules : modules module")
def statements(p):
    return Block(p[0].getastlist() + [p[1]])

@pg.production("modules : module")
def statements(p):
    return Block([p[0]])

@pg.production("module : comment")
def comment_mdl(p):
    return p[0]

@pg.production("module : IMPORT importname AS lambda")
def mdl_import_and_return(p):
    # print("What the parser returned")
    # print(p)
    return ImportMdl(p[1], p[3])

@pg.production("module : EXPORT module AS IDENTIFIER")
def mdl_export_stmt(p):
    return ExportMdl(p[1], p[3].getstr())

@pg.production("module : MEMORY IDENTIFIER INT")
def mdl_memory(p):
    return MemoryMdl(p[1].getstr(), p[2].getstr())

@pg.production("module : DEF IDENTIFIER LPAR parameters RPAR RIGHT_ARROW IDENTIFIER body")
def mdl_func_def(p):
    return FuncMdl(p[1].getstr(), p[3], p[6].getstr(), p[7])

@pg.production("module : DEF IDENTIFIER LPAR RPAR RIGHT_ARROW IDENTIFIER body")
def mdl_func_def_no_params(p):
    return FuncMdl(p[1].getstr(), Arguments([]), p[5].getstr(), p[6])

@pg.production("body : LBRACE RBRACE")
def empty_func_body(p):
    return Block([])

@pg.production("body : LBRACE innerfunc RBRACE")
def body_block(p):
    return Block([p[1]])

@pg.production("innerfunc : innerfunc stmt")
def statements(p):
    return Block(p[0].getastlist() + [p[1]])

@pg.production("innerfunc : stmt")
def single_statement_inner_func(p):
    return Block([p[0]])

@pg.production("stmt : vardeclar")
@pg.production("stmt : memstore")
@pg.production("stmt : sum")
@pg.production("stmt : comment")
@pg.production("stmt : forloop")
@pg.production("stmt : if")
def innerfunc_values(p):
    return p[0]

@pg.production("forloop : FOR IDENTIFIER IN RANGE LPAR sum COMMA sum RPAR body")
def forloop(p):
    return ForLoop(p[1], p[5], p[7], p[9])

@pg.production("if : IF sum body")
def if_stmt(p):
    return IfStmt(p[1], p[2], Block([]))

@pg.production("if : IF sum body ELSE body")
def if_stmt(p):
    return IfStmt(p[1], p[2], p[4])

@pg.production("comment : COMMENT")
def commentary(p):
    return Comment(p[0].getstr())

@pg.production("vardeclar : LET IDENTIFIER EQUALS sum SEMICOLON")
def let_expr_block(p):
    return LetStmt(p[1], p[3])

@pg.production("memstore : MEM LSQRBRACE sum RSQRBRACE EQUALS sum SEMICOLON")
def mem_expr_block(p):
    return Memory_Store(p[2], p[5])


# atom
@pg.production("atom : IDENTIFIER")
@pg.production("atom : INT")
def atom_value(p):
    return Value(p[0])

# atom
@pg.production("atom : IDENTIFIER LPAR arguments RPAR SEMICOLON")
def function_call(p):
    return FunctionCall(p[0].getstr(), p[2])

# atom
@pg.production("atom : IDENTIFIER LPAR RPAR SEMICOLON")
def function_call_no_arguments(p):
    return FunctionCall(p[0].getstr(), Arguments([]))

@pg.production("arguments : arguments COMMA arg")
def arguments(p):
    return Arguments(p[0].getastlist() + [Arg(p[2])])

@pg.production("arguments : arg")
def arguments_one(p):
    return Arguments([Arg(p[0])])

@pg.production("arg : sum")
def arg(p):
    return p[0]

# atom
@pg.production("atom : LPAR sum RPAR")
def parentesised_expr(p):
    return p[1]

# sum
@pg.production("sum : sum PLUS product")
@pg.production("sum : sum MINUS product")
def bin_sum(p):
    return BinaryOp(p[0], p[1], p[2])
@pg.production("sum : product")
def sum_product(p):
    return p[0]
# product
@pg.production("product : product MUL condition")
@pg.production("product : product DIV condition")
def bin_prod(p):
    return BinaryOp(p[0], p[1], p[2])
@pg.production("product : condition")
def product_condition(p):
    return p[0]


# condition
@pg.production("condition : condition BINEQUAL atom")
@pg.production("condition : condition BINNOTEQUAL atom")
@pg.production("condition : condition BINLSS atom")
@pg.production("condition : condition BINGTR atom")
@pg.production("condition : condition BINLSSEQUAL atom")
@pg.production("condition : condition BINGTREQUAL atom")
def bin_condition(p):
    return BinaryOp(p[0], p[1], p[2])

@pg.production("condition : atom")
def condition_atom(p):
    return p[0]

@pg.production("parameters : parameters COMMA param")
def mdl_func_param(p):
    return Parameters(p[0].getastlist() + [p[2]])

@pg.production("parameters : param")
def mdl_func_single_param(p):
    return Parameters([p[0]])

@pg.production("param : IDENTIFIER COLON IDENTIFIER")
def param_name_type(p):
    return Param(p[0].getstr(), p[2].getstr())

@pg.production("lambda : LAMBDA IDENTIFIER typelist RIGHT_ARROW IDENTIFIER")
def mdl_lambda_with_return(p):
    # print("The lambda with return")
    return LambdaMdl(p[1].getstr(), p[2], p[4].getstr())

@pg.production("lambda : LAMBDA IDENTIFIER typelist")
def mdl_lambda(p):
    # print("The lambda")
    return LambdaMdl(p[1].getstr(), p[2])

@pg.production("typelist : LPAR nameplus RPAR")
def oneplus_typelist(p):
    return p[1]


@pg.production("typelist : LPAR RPAR")
def no_typelist(_):
    return []


# IDENTIFIER +
@pg.production("nameplus : nameplus IDENTIFIER")
def nameplus(p):
    # print("nameplus")
    # print(p)
    return p[0] + [LambdaType(p[1].getstr())]

@pg.production("nameplus : IDENTIFIER")
def nameplus(p):
    # print("nameplus IDENTIFIER")
    # print(p)
    return [LambdaType(p[0].getstr())]

# importname : IDENTIFIER ( DOT IDENTIFIER ) *
@pg.production("importname : importname DOT IDENTIFIER")
def import_name_dot_name(p):
    # print("name dot name")
    # print(p)
    return p[0] + [p[2].getstr()]

@pg.production("importname : IDENTIFIER")
def import_name(p):
    return [p[0].getstr()]

# @pg.error
# def error_handler(token):
#     raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())
parser = pg.build()