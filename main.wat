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
(func $print_char_scanline (param $bitmap i32) (param $line i32)
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 128)) (i32.const 0))
(if (then
(call $setpixel (i32.const 0) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 64)) (i32.const 0))
(if (then
(call $setpixel (i32.const 1) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 32)) (i32.const 0))
(if (then
(call $setpixel (i32.const 2) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 16)) (i32.const 0))
(if (then
(call $setpixel (i32.const 3) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 8)) (i32.const 0))
(if (then
(call $setpixel (i32.const 4) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 4)) (i32.const 0))
(if (then
(call $setpixel (i32.const 5) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 2)) (i32.const 0))
(if (then
(call $setpixel (i32.const 6) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
(i32.gt_u (i32.and (local.get $bitmap) (i32.const 1)) (i32.const 0))
(if (then
(call $setpixel (i32.const 7) (local.get $line) (i32.const 0) (i32.const 0) (i32.const 0) (i32.const 255)))
(else

))
)
(func $char_cli (param $char i32) (local $screen_end i32) (local $char_start i32) (local $scanline i32) (local $char_line i32)
;; writes a character to the screen
(i32.eq (local.get $char) (i32.const 65))
(if (then
;; found the A character.
(local.set $screen_end
(i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4))
)
(local.set $char_start
(i32.add (local.get $screen_end) (i32.mul (i32.sub (local.get $char) (i32.const 32)) (i32.mul (i32.const 8) (i32.const 11))))
)
(local.set $scanline
(i32.const 0)
)
(block $break_char_cli_0
(loop $top_char_cli_0
(br_if $break_char_cli_0 (i32.eq (local.get $scanline) (i32.const 11)))
(local.set $char_line
(i32.add (local.get $char_start) (local.get $scanline))
)
(call $log (local.get $char_line))
(call $print_char_scanline (local.get $char_line)
(i32.load8_u) (local.get $scanline))
(local.set $scanline
(i32.add (local.get $scanline) (i32.const 1))
)
(br $top_char_cli_0)
)
)
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
)
(func $load_font (local $screen_end i32) (local $a_start i32)
;; store the bitmap of the font
;; 'A' CHARACTER 65 ascii code
(local.set $screen_end
(i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4))
)
(local.set $a_start
(i32.add (local.get $screen_end) (i32.mul (i32.sub (i32.const 65) (i32.const 32)) (i32.mul (i32.const 8) (i32.const 11))))
)
(call $log (i32.const 437))
(call $log (local.get $a_start))
(local.get $a_start)
(i32.const 48)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 1))
(i32.const 120)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 2))
(i32.const 220)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 3))
(i32.const 204)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 4))
(i32.const 252)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 5))
(i32.const 252)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 6))
(i32.const 204)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 7))
(i32.const 204)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 8))
(i32.const 204)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 9))
(i32.const 0)
(i32.store8)
(i32.add (local.get $a_start) (i32.const 10))
(i32.const 0)
(i32.store8)
;; END of 'A' Character
)
(func $font_program
(call $load_font)
(call $char_cli (i32.const 65))
)
(func $condition_check (local $test i32)
(local.set $test
(i32.const 1)
)
(i32.eq (local.get $test) (i32.const 1))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.ne (local.get $test) (i32.const 0))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.ne (local.get $test) (i32.const 1))
(if (then
(call $log (i32.const 6666)))
(else
(call $log (i32.const 1111))
))
(i32.lt_u (local.get $test) (i32.const 2))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.lt_u (i32.const 2) (local.get $test))
(if (then
(call $log (i32.const 6666)))
(else
(call $log (i32.const 1111))
))
(i32.gt_u (i32.const 2) (local.get $test))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.gt_u (local.get $test) (i32.const 2))
(if (then
(call $log (i32.const 6666)))
(else
(call $log (i32.const 1111))
))
(i32.le_u (local.get $test) (i32.const 2))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.le_u (i32.const 2) (local.get $test))
(if (then
(call $log (i32.const 6666)))
(else
(call $log (i32.const 1111))
))
(i32.ge_u (i32.const 2) (local.get $test))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.ge_u (local.get $test) (i32.const 2))
(if (then
(call $log (i32.const 6666)))
(else
(call $log (i32.const 1111))
))
(i32.and (local.get $test) (i32.const 1))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
(i32.and (i32.const 1) (local.get $test))
(if (then
(call $log (i32.const 1111)))
(else
(call $log (i32.const 6666))
))
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
(call $condition_check)
;; total memory in the 18 pages
(call $log (i32.mul (i32.const 65536) (i32.const 18)))
;; total memory used by this screen
(call $log (i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4)))
;; memory left after screen.
(call $log (i32.sub (i32.mul (i32.const 65536) (i32.const 18)) (i32.mul (i32.mul (i32.const 680) (i32.const 420)) (i32.const 4))))
;; the font memory
(call $log (i32.mul (i32.mul (i32.const 94) (i32.const 8)) (i32.const 11)))
(call $font_program)
(call $refresh_screen)
;; set the return value 0 from the function
(i32.const 0)
)