# define the ast for the language
from rply.token import BaseBox, Token

# global variables_defining_scopes_/_context of functions
global_var = {"function_name" : "", "loop_index": 0 }

class Comment(BaseBox):
    def __init__(self, comment_string):
        self.comment_string = comment_string

    def eval(self):
        return ";;" + self.comment_string[1:] # removing the # from the comment

class LambdaMdl(BaseBox):
    def __init__(self, name, params : list[str], return_type : str = None):
        self.name = name
        self.params = params
        self.return_type = return_type

    def eval(self) -> str:
        param_str = "".join([param.eval() for param in self.params])
        if self.return_type is None:
            return "(func $" + self.name + param_str + ")"
        else:
            return "(func $" + self.name + param_str + self.return_stmt + ")"

class Block(BaseBox):
    def __init__(self, stmts):
        self.statements = stmts

    def getastlist(self):
        return self.statements

    def eval(self) -> str:
        "return the statements given as webassembly text"
        return "\n".join([stmt.eval() for stmt in self.statements])

class ForLoop(BaseBox):
    def __init__(self, loop_var, start_idx, end_idx, body) -> None:
        self.loop_var = loop_var
        self.init_loop_var = LetStmt(loop_var, start_idx)
        self.increment_loop_var = LetStmt(loop_var , BinaryOp(Value(loop_var), Token("PLUS", "+"), Value(Token("INT", 1))))
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.body = body
    
    def eval(self) -> str:
        global global_var
        break_tag = f"$break_{global_var['function_name'] + '_' + str(global_var['loop_index'])}"
        top_tag = f"$top_{global_var['function_name'] + '_' + str(global_var['loop_index'])}"
        condition = f"(i32.eq {Value(self.loop_var).eval()} {self.end_idx.eval()})"
        loop_var_wat = self.init_loop_var.eval()
        loop_var_inc_wat = self.increment_loop_var.eval()
        loop_head = f"(block {break_tag}\n(loop {top_tag}\n(br_if {break_tag} {condition})"
        loop_end = f"(br {top_tag})\n)\n)"

        # Important to increment the loop_index before we go into the loop body
        global_var["loop_index"] += 1

        ret_wat = f"{loop_var_wat}\n{loop_head}\n{self.body.eval()}\n{loop_var_inc_wat}\n{loop_end}"

        
        return ret_wat

class LambdaType(BaseBox):
    def __init__(self, typ) -> None:
        self.typ = typ

    def eval(self) -> str:
        return f" (param {self.typ})"

class IfStmt(BaseBox):
    def __init__(self, condition, true_block, false_block) -> None:
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def eval(self) -> str:
        return f"{self.condition.eval()}\n(if (then\n{self.true_block.eval()})\n(else\n{self.false_block.eval()}\n))"
        

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


def local_tag_from_letstatement(value):
    return f" (local ${value.name} i32)"

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
        global global_var
        global_var["function_name"] = self.name # sets the right context for generated names
        global_var["loop_index"] = 0
        
        locals_str = "" #default the value to nothing
        if len(self.body.statements) > 0:
            let_stmts = set(iter_body_stmts_for_let_stmts(self.body.statements[0].statements)) # use the set to remove the duplicate values
            
            locals_str = "".join(list(map(local_tag_from_letstatement, let_stmts)))
        # print(locals_str, type(locals_str))
        func_tag = f"(func ${self.name}{export}" + self.params.eval() + self.result_tag() + f"{locals_str}\n" + self.bodystmts() + "\n)"
        return func_tag

def iter_body_stmts_for_let_stmts(body_stmts):
    stmts = []
    for val in body_stmts:
        if isinstance(val, LetStmt):
            stmts.append(val)
        elif isinstance(val, ForLoop):
            stmts.append(val.init_loop_var) # get it's init value
            stmts.extend(iter_body_stmts_for_let_stmts(val.body.statements[0].statements)) # get possible let statements from the loop body
            # assert False, (dir(val.body.statements[0]), val.body.statements[0].statements)
        elif isinstance(val, IfStmt):
            print(dir(val))
            stmts.extend(iter_body_stmts_for_let_stmts(val.true_block.statements[0].statements)) # there is always a true statements
            if len(val.false_block.statements) > 0:
                stmts.extend(iter_body_stmts_for_let_stmts(val.false_block.statements[0].statements))
    return stmts

class LetStmt(BaseBox):
    def __init__(self, name : Token, val_expr) -> None:
        self.name = name.getstr()
        self.val_expr = val_expr

    def eval(self) -> str:
        return f"(local.set ${self.name}\n{self.val_expr.eval()}\n)"

    # use the hash and eq function for the set() function that is used to find unique values
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(('name', self.name))

class Memory_Store(BaseBox):
    def __init__(self, address, val_expr) -> None:
        self.address = address
        self.val_expr = val_expr

    def eval(self) -> str:
        return f"{self.address.eval()}\n{self.val_expr.eval()}\n(i32.store8)"

class Memory_Load(BaseBox):
    def __init__(self, address) -> None:
        self.address = address
    
    def eval(self) -> str:
        return f"{self.address.eval()}\n(i32.load8_u)"

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
                op = "div_u"
            case "%":
                op = "rem_u"
            case "==":
                op = "eq"
            case "!=":
                op = "ne"
            case "<=":
                op = "le_u"
            case ">=":
                op = "ge_u"
            case "<":
                op = "lt_u"
            case ">":
                op = "gt_u"
            case "&&":
                op = "and"
            case _:
                raise Exception(f"No watcode found for operation: {self.op.getstr()}")

        return f"(i32.{op} {self.left.eval()} {self.right.eval()})"