from rply import ParserGenerator
from ast_def import *

pg = ParserGenerator(["IMPORT", "EXPORT", "AS", "LAMBDA", "DEF", "LET", "RPAR", "LPAR", "LBRACE", "RBRACE", "LSQRBRACE", "RSQRBRACE", "MEMORY", "DOT", "COMMA", "EQUALS", "PLUS", "MINUS", "MUL", "DIV", "INT", "IDENTIFIER", "COLON", "SEMICOLON", "RIGHT_ARROW"],
    # the lower in list. The higher precedence
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

@pg.production("modules : modules module")
def statements(p):
    return Block(p[0].getastlist() + [p[1]])

@pg.production("modules : module")
def statements(p):
    return Block([p[0]])

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
def expression_block(p):
    return Block([p[1]])

@pg.production("innerfunc : innerfunc stmt")
def statements(p):
    return Block(p[0].getastlist() + [p[1]])

@pg.production("innerfunc : stmt")
def single_statement_inner_func(p):
    return Block([p[0]])

@pg.production("stmt : vardeclar")
@pg.production("stmt : memstore")
@pg.production("stmt : expression")
def innerfunc_values(p):
    return p[0]

@pg.production("vardeclar : LET IDENTIFIER EQUALS expression SEMICOLON")
def let_expression_block(p):
    return LetStmt(p[1].getstr(), p[3])

@pg.production("memstore : IDENTIFIER LSQRBRACE expression RSQRBRACE EQUALS expression SEMICOLON")
def mem_expression_block(p):
    # TODO change how values like IDENTIFIER AND INT are handled in BINOPS. Give them their own Value class and bin op will call that value
    return Memory_Store((p[0].getstr()), p[2], p[5])

@pg.production("expression : IDENTIFIER")
@pg.production("expression : INT")
def expression_value(p):
    return Value(p[0])

@pg.production("expression : IDENTIFIER LPAR arguments RPAR SEMICOLON")
def function_call(p):
    return FunctionCall(p[0].getstr(), p[2])

@pg.production("expression : IDENTIFIER LPAR RPAR SEMICOLON")
def function_call_no_arguments(p):
    return FunctionCall(p[0].getstr(), Arguments([]))

@pg.production("arguments : arguments COMMA arg")
def arguments(p):
    return Arguments(p[0].getastlist() + [Arg(p[2])])

@pg.production("arguments : arg")
def arguments_one(p):
    return Arguments([Arg(p[0])])

@pg.production("arg : expression")
def arg(p):
    return p[0]

@pg.production("expression : LPAR expression RPAR")
def parentesised_expr(p):
    return p[1]

@pg.production("expression : expression PLUS expression")
@pg.production("expression : expression MINUS expression")
@pg.production("expression : expression MUL expression")
@pg.production("expression : expression DIV expression")
def plus_expression(p):
    return BinaryOp(p[0], p[1], p[2])

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
    return p[0] + [p[1].getstr()]

@pg.production("nameplus : IDENTIFIER")
def nameplus(p):
    # print("nameplus IDENTIFIER")
    # print(p)
    return [p[0].getstr()]

# importname : IDENTIFIER ( DOT IDENTIFIER ) *
@pg.production("importname : importname DOT IDENTIFIER")
def import_name_dot_name(p):
    # print("name dot name")
    # print(p)
    return p[0] + [p[2].getstr()]

@pg.production("importname : IDENTIFIER")
def import_name(p):
    return [p[0].getstr()]

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())
parser = pg.build()