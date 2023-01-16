# define the ast for the language
from rply.token import BaseBox

class Number(BaseBox):
    def __init__(self, value) -> None:
        self.value = value

    def eval(self) -> str:
        "returns the wat code for the code"
        return f"(i32.const {self.value})"

class LambdaStmt(BaseBox):
    def __init__(self, name, params : list[str], return_type : str = None):
        self.name = name
        self.params = params
        if len(self.params) > 0:
            self.params[0] = " " + self.params[0]
        self.return_type = return_type

    def eval(self) -> str:
        if self.return_type is None:
            return "(func $" + self.name + " ".join(self.params) + ")"
        else:
            return "(func $" + self.name + " ".join(self.params) + self.return_stmt + ")"

class Block(BaseBox):
    def __init__(self, stmts):
        self.statements = stmts

    def getastlist(self):
        return self.statements

    def eval(self) -> str:
        "return the statements given as webassembly text"
        return "\n".join([stmt.eval() for stmt in self.statements])


def add_quotes(val):
    return '\"' + val + '\"'

class ImportStmt(BaseBox):
    def __init__(self, outside_obj_ref : list[str], inner_ref : BaseBox) -> None:
        self.outside_obj_ref = outside_obj_ref
        self.inner_ref = inner_ref

    def eval(self, export="") -> str:
        assert export == "", "Please don't give import statements something to export"
        return "(import " + " ".join(list(map(add_quotes, self.outside_obj_ref))) + " " + self.inner_ref.eval() + ")"

class ExportStmt(BaseBox):
    def __init__(self, stmt, name) -> None:
        self.stmt_to_export = stmt
        self.export_name = name

    # make sure that it's eval calls the eval of the inner statement to export
    # and gives the export name string to be inserted
    def eval(self) -> str:
        export_tag = " (export " + add_quotes(self.export_name) + ")"
        return self.stmt_to_export.eval(export=export_tag)

class MemoryStmt(BaseBox):
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size

    def eval(self, export="") -> str:
        return f"(memory ${self.name}{export} {self.size})"

class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right