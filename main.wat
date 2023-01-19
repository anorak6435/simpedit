(import "env" "log" (func $log (param i32)))
(import "env" "refresh_screen" (func $refresh_screen))
(memory $wasmem (export "wasmem") 18)
(func $add (export "add") (param $x i32) (param $y i32) (result i32)
(i32.add (local.get $x) (local.get $y))
)
;; made a formula to check if math precedence was handled
(func $formula (param $x i32) (param $y i32) (param $z i32) (result i32)
(i32.sub (i32.add (local.get $x) (i32.mul (local.get $y) (local.get $z))) (i32.div_u (i32.const 4) (i32.const 2)))
)
(func $setpixel (param $x i32) (param $y i32) (param $r i32) (param $g i32) (param $b i32) (param $a i32) (local $pxl_start i32)
(local.set $pxl_start
(i32.mul (i32.add (i32.mul (local.get $y) (i32.const 680)) (local.get $x)) (i32.const 4))
)
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
(func $main (export "main") (result i32) (local $yi i32) (local $xi i32)
(call $add (i32.const 410) (i32.const 10))
(call $log)
(local.set $yi
(i32.const 0)
)
(block $break_main_0
(loop $top_main_0
(br_if $break_main_0 (i32.eq (local.get $yi) (i32.const 420)))
(local.set $xi
(i32.const 0)
)
(block $break_main_1
(loop $top_main_1
(br_if $break_main_1 (i32.eq (local.get $xi) (i32.const 680)))
;; red is alert on changes in the code
;; log(xi);
;; log(yi);
;; setpixel(xi, yi, 255, 0, 0, 255);
(call $setpixel (local.get $xi) (local.get $yi) (i32.const 165) (i32.const 55) (i32.const 253) (i32.const 255))
;; purple pixels
(local.set $xi
(i32.add (local.get $xi) (i32.const 1))
)
(br $top_main_1)
)
)
(local.set $yi
(i32.add (local.get $yi) (i32.const 1))
)
(br $top_main_0)
)
)
(call $refresh_screen)
;; total memory in the 18 pages
(call $log (i32.mul (i32.const 65536) (i32.const 18)))
;; total memory used by this screen
(call $log (i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4)))
;; memory left after screen.
(call $log (i32.sub (i32.mul (i32.const 65536) (i32.const 18)) (i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4))))
;; set the return value 0 from the function
(i32.const 0)
)