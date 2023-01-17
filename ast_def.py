# define the ast for the language
from rply.token import BaseBox, Token

# class Number(BaseBox):
#     def __init__(self, value) -> None:
#         self.value = value

#     def eval(self) -> str:
#         "returns the wat code for the code"
#         return f"(i32.const {self.value})"

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

class Arguments(BaseBox):
    def __init__(self, argument_lst) -> None:
        self.arg_lst = argument_lst

    def getastlist(self):
        return self.arg_lst

    def eval(self) -> str:
        # print(self.arg_lst)
        return "".join([arg.eval() for arg in self.arg_lst])

class Arg(BaseBox):
    def __init__(self, expr_val) -> None:
        self.expr_val = expr_val

    def eval(self) -> str:
        # print(self.expr_val)
        return " " + self.expr_val.eval()



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

class MemoryMdl(BaseBox):
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size

    def eval(self, export="") -> str:
        return f"(memory ${self.name}{export} {self.size})"

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
        locals_str = "" #default the value to nothing
        if len(self.body.statements) > 0:
            let_stmts = list(filter(is_let_stmt, self.body.statements[0].statements))
            locals_str = "".join(list(map(lambda val: f" (local ${val.name} i32)", let_stmts)))
        print(locals_str, type(locals_str))
        func_tag = f"(func ${self.name}{export}" + self.params.eval() + self.result_tag() + f"{locals_str}\n" + self.bodystmts() + ")"
        return func_tag

class LetStmt(BaseBox):
    def __init__(self, name, val_expr) -> None:
        self.name = name
        self.val_expr = val_expr

    def eval(self) -> str:
        return f"(local.set ${self.name}\n{self.val_expr.eval()}\n)"

class Memory_Store(BaseBox):
    def __init__(self, memref, address, val_expr) -> None:
        self.memref = memref
        self.address = address
        self.val_expr = val_expr

    def eval(self) -> str:
        return f"{self.address.eval()}\n{self.val_expr.eval()}\n(i32.store8)"

class FunctionCall(BaseBox):
    def __init__(self, func_name, arguments) -> None:
        self.func_name = func_name
        self.args = arguments

    def eval(self) -> str:
        return f"(call ${self.func_name}{self.args.eval()})"

class Value(BaseBox):
    def __init__(self, val):
        self.value = val

    def eval(self) -> str:
        match self.value.gettokentype():
            case "IDENTIFIER":
                return f"(local.get ${self.value.getstr()})"
            case "INT":
                return f"(i32.const {self.value.getstr()})"
            case _:
                raise Exception(f"No watcode found for value: {self.value.gettokentype()}")

class BinaryOp(BaseBox):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self) -> str:
        match self.op.getstr():
            case "+":
                op = "add"
            case "-":
                op = "sub"
            case "*":
                op = "mul"
            case "/":
                op = "div"
            case _:
                raise Exception(f"No watcode found for operation: {self.op.getstr()}")

        return f"(i32.{op} {self.left.eval()} {self.right.eval()})"

def is_let_stmt(val):
    return isinstance(val, LetStmt)