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
def NAME ( param : [i32 | i64] * ) -> [i32 | i64] {
    let x = 15; # set the local x value to 15
}

## local variable definition
let NAME = expression;

## memory manipulation
### store8
store8\[address\] = expression;
set a memory value at address to expression value
store8 is the memory command keyword
address is an expression that results into an integer
expression results into the integer value to be stored at that memory location

### load8
load8\[address\]

load 8 bits from the memory ready to be used in expressions by the program.

## call function
NAME \( args * \);

## comment definition
Comments are defined like in python
\# following text is comemnted
until the newline Than code can continue

## for loop definition
for local_var in range(0, 155) {
    # instructions ...
}
A local variable will be set that tracks what index in the loop we are at.
increment this local variable at the end of the loop.

## If statements
if condition { block }
optional:
else { block }


# TODO
- [x] The nameplus to change it into typelist and make parameters free for the function statement
- [x] Build a wat version of the add function
- [x] add more binary operations (with precedence)
- [x] build a definition for a local variable
- [x] FIX can handle function definitions without arguments
- [x] build a function call definition
- [x] build comment definition
    - [x] inside functions comments
    - [x] outside function comments
    - [x] FIX made me realise that the function closing paren has te be on it's own line otherwise it will be commented out.
- [x] build a for loop definition
    - [x] build a nested for loop
- [x] setup walking through the statements and inner statements of loops to get let statements
- [x] make if conditions happen
    - [x] if condition statement
    - [x] if else condition statements
- condition checks
    - [x] ==
    - [x] !=
    - [x] <
    - [x] >
    - [x] <=
    - [x] >=
- [x] Memory
    - [x] store8\[address\] = value;
    - [x] load8\[address\]
- [ ] Generate the productions that are needed for the program
    - [ ] modules
        - [ ] comment
        - [ ] import
        - [ ] export
        - [ ] memory
        - [ ] function
    - [ ] statements
        - [ ] assert (for testing purposes)
        - [ ] comment
        - [ ] vardeclar
        - [ ] memstore
        - [ ] sum (expression)
        - [ ] forloop
        - [ ] if

# Pygraphviz installation
https://stackoverflow.com/questions/59707234/issues-installing-pygrahviz-fatal-error-c1083-cannot-open-include-file-graph
run the .exe after that  
pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz