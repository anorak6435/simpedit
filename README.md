# A simple editor
Be another simple dev env in the browser.

let's add a cursor to the browser so the user knows where the code would be added.

# language to define the editor in.
used for myself to have one step above the wat strings

## import definitions
import env.log as lambda NAME ( [i32 | i64] * ) [ -> [i32 | i64] ]

## memory definitions
memory NAME INT
the int defines the number of pages the memory uses

## export definition
export stmt as NAME
adds an export tag to the stmt it wraps

## function definitions
def NAME ( param : [i32 | i64] * ) [ -> [i32 | i64] ]
    let x = 15; # set the local x value to 15