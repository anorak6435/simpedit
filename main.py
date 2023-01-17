from wasmer import wat2wasm
from rply import LexerGenerator
from parse_def import parser


lg = LexerGenerator()

lg.add("IMPORT", "import")
lg.add("EXPORT", "export")
lg.add("AS", "as")
lg.add("LAMBDA", "lambda")
lg.add("MEMORY", "memory")
lg.add("DEF", "def")
lg.add("LET", "let")
lg.add("MEM", "mem")
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
lg.add("EQUALS", "=")
lg.add("PLUS", r"\+")
lg.add("MINUS", r"\-")
lg.add("MUL", r"\*")
lg.add("DIV", r"/")
lg.add("INT", r"\d+")
lg.add("IDENTIFIER", r"[a-z-A-Z0-9_]\w*")
lg.ignore(r"\s+")


# load the contents of the source file
with open("./lang/purple.ptr", "r") as f:
    src = f.read()

lexer = lg.build()
for tok in lexer.lex(src):
    print(tok)

wat_text = parser.parse(lexer.lex(src)).eval()
print("The wat output text")
print(wat_text)

module = """(module
    (import "env" "log" (func $log (param i32)))
    (import "env" "refresh_screen" (func $refresh_screen))
    (memory $mem (export "mem") 18)
    (func $add (export "add") (param i32) (param i32) (result i32)
        (local.get 0)
        (local.get 1)
        (i32.add)
    )
    (func $setpixel (param $x i32) (param $y i32) (param $r i32) (param $g i32) (param $b i32) (param $a i32) (local $pxl_start i32) ;; set the red green blue alpha values for the position maked by $x $y
        (local.set $pxl_start
            (i32.mul 
                (i32.add 
                    (i32.mul (local.get $y) (i32.const 680) ) 
                    (local.get $x)
                ) 
                (i32.const 4)
            )
        ) ;; the location of the r value starting this pixel
        ;; (call $log (local.get $pxl_start))
        (local.get $pxl_start)
        (local.get $r)
        (i32.store8)

        (i32.add (local.get $pxl_start) (i32.const 1))
        (local.get $g)
        (i32.store8)

        (i32.add (local.get $pxl_start) (i32.const 2))
        (local.get $b)
        (i32.store8)

        (i32.add (local.get $pxl_start) (i32.const 3))
        (local.get $a)
        (i32.store8)
    )
    (func $main (export "main") (result i32) (local $xi i32) (local $yi i32)
        (call $add (i32.const 410) (i32.const 10))
        (call $log)
        (local.set $xi (i32.const 0))
        
        ;; for xi in range (xi, 680)
        (block $break_x
            (loop $top_x
                (br_if $break_x
                    (i32.eq
                        (local.get $xi)
                        (i32.const 680)
                    )
                )
                (local.set $yi (i32.const 0))
                (block $break_y
                    (loop $top_y
                        (br_if $break_y
                            (i32.eq
                                (local.get $yi)
                                (i32.const 420)
                            )
                        )

                
                        (call $setpixel (local.get $xi) (local.get $yi) (i32.const 165) (i32.const 55) (i32.const 253) (i32.const 255))

                        (local.set $yi
                            (i32.add (local.get $yi) (i32.const 1))
                        )
                        (br $top_y)
                    )
                )

                (local.set $xi
                    (i32.add (local.get $xi) (i32.const 1))
                )
                (br $top_x)
            )
        )

        ;;(call $setpixel (i32.const 0) (i32.const 0) (i32.const 255) (i32.const 255) (i32.const 0) (i32.const 0))
        ;;(call $setpixel (i32.const 1) (i32.const 0) (i32.const 255) (i32.const 255) (i32.const 0) (i32.const 0))
        ;;(call $setpixel (i32.const 2) (i32.const 0) (i32.const 255) (i32.const 255) (i32.const 0) (i32.const 0))
        ;;(call $setpixel (i32.const 3) (i32.const 0) (i32.const 255) (i32.const 255) (i32.const 0) (i32.const 0))
        ;;(call $setpixel (i32.const 4) (i32.const 0) (i32.const 255) (i32.const 255) (i32.const 0) (i32.const 0))
        (call $refresh_screen)
        (i32.const 0)
    )
)
"""

data = wat2wasm(module)
print(data)

with open("main.wasm", "wb") as f:
    f.write(data)