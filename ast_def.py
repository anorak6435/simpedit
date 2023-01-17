# define the ast for the language
from rply.token import BaseBox, Token

class Number(BaseBox):
    def __init__(self, value) -> None:
        self.value = value

    def eval(self) -> str:
        "returns the wat code for the code"
        return f"(i32.const {self.value})"

class LambdaMdl(BaseBox):
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

class Parameters(BaseBox):
    def __init__(self, param_lst):
        self.param_lst = param_lst

    def getastlist(self):
        return self.param_lst

    def __repr__(self):
        return "PARAMS: " + str(self.param_lst)

    def eval(self) -> str:
        "return the statements given as webassembly text"
        return "".join([param.eval() for param in self.param_lst])

class Param(BaseBox):
    def __init__(self, p_name, p_type):
        self.name = p_name
        self.type = p_type

    def eval(self) -> str:
        return f" (param ${self.name} {self.type})"

def add_quotes(val):
    return '\"' + val + '\"'

class ImportMdl(BaseBox):
    def __init__(self, outside_obj_ref : list[str], inner_ref : BaseBox) -> None:
        self.outside_obj_ref = outside_obj_ref
        self.inner_ref = inner_ref

    def eval(self, export="") -> str:
        assert export == "", "Please don't give import statements something to export"
        return "(import " + " ".join(list(map(add_quotes, self.outside_obj_ref))) + " " + self.inner_ref.eval() + ")"

class ExportMdl(BaseBox):
    def __init__(self, stmt, name) -> None:
        self.stmt_to_export = stmt
        self.export_name = name

    # make sure that it's eval calls the eval of the inner statement to export
    # and gives the export name string to be inserted
    def eval(self) -> str:
        export_tag = " (export " + add_quotes(self.export_name) + ")"
        return self.stmt_to_export.eval(export=export_tag)

class FuncMdl(BaseBox):
    def __init__(self, name, params, result, body) -> None:
        self.name = name
        self.params = params
        self.result = result
        self.body = body

    def result_tag(self):
        if self.result == "void":
            return ""
        else:
            return f" (result {self.result})"

    def bodystmts(self):
        return self.body.eval()

    def eval(self, export="") -> str:
        # print("params : ", self.params)
        func_tag = f"(func ${self.name}{export}" + self.params.eval() + self.result_tag() + "\n" + self.bodystmts() + ")"
        return func_tag

class MemoryMdl(BaseBox):
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size

    def eval(self, export="") -> str:
        return f"(memory ${self.name}{export} {self.size})"

class BinaryOp(BaseBox):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def value_tag(self, value : Token) -> str:
        match value.gettokentype():
            case "IDENTIFIER":
                return f"(local.get ${value.getstr()})"
            case _:
                raise Exception(f"No watcode found for binaryop value: {value.gettokentype()}")

    def eval(self) -> str:
        assert isinstance(self.left, Token), "The left is not a token"
        print(dir(self.left))
        return_str = ""

        match self.op.getstr():
            case "+":
                return_str += f"(i32.add {self.value_tag(self.left)} {self.value_tag(self.right)})"
            case _:
                raise Exception(f"No watcode found for operation: {self.op.getstr()}")

        return return_str