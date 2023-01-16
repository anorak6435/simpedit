from rply import ParserGenerator
from ast_def import *

pg = ParserGenerator(["IMPORT", "AS", "LAMBDA", "RPAR", "LPAR", "COLON", "DOT", "IDENTIFIER", "RIGHT_ARROW"])

@pg.production("statements : statements stmt")
def statements(p):
    return Block(p[0].getastlist() + [p[1]])

@pg.production("statements : stmt")
def statements(p):
    return Block([p[0]])

@pg.production("stmt : IMPORT importname AS lambda")
def stmt_import_and_return(p):
    # print("What the parser returned")
    # print(p)
    return ImportStmt(p[1], p[3])


@pg.production("lambda : LAMBDA IDENTIFIER parameters RIGHT_ARROW IDENTIFIER")
def stmt_lambda_with_return(p):
    # print("The lambda with return")
    return LambdaStmt(p[1].getstr(), p[2], p[4].getstr())

@pg.production("lambda : LAMBDA IDENTIFIER parameters")
def stmt_lambda(p):
    # print("The lambda")
    return LambdaStmt(p[1].getstr(), p[2])

@pg.production("parameters : LPAR nameplus RPAR")
def oneplus_parameters(p):
    return p[1]


@pg.production("parameters : LPAR RPAR")
def no_parameters(_):
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