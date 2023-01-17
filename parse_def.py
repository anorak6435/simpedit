from rply import ParserGenerator
from ast_def import *

pg = ParserGenerator(["IMPORT", "EXPORT", "AS", "LAMBDA", "DEF", "RPAR", "LPAR", "LBRACE", "RBRACE", "MEMORY", "DOT", "COMMA", "PLUS", "INT", "IDENTIFIER", "COLON", "RIGHT_ARROW"])

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

@pg.production("body : LBRACE RBRACE")
def empty_func_body(p):
    return Block([])

@pg.production("body : LBRACE expression RBRACE")
def expression_block(p):
    return Block([p[1]])

# @pg.production("expression : INT PLUS INT")
@pg.production("expression : IDENTIFIER PLUS IDENTIFIER")
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