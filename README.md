# Interpreted Languange Run in Python
## 1. Introduction
This is a simple interpreted language run in Python. This project also includes Simple Text Editor and Interactive Terminal. It supports the following features:
1.  Variable declaration and assignment
```
Example:
a = 1
b = 2
```
2.  Arithmetic operations
```
Example:
a = 1 + 2
b = 3 - 4
c = 5 * 6
d = 7 / 8
e = a + b * c - d
```
3.  List declaration and assignment
```
Example:
a = [1, 2, 3]
```
4.  Conditional statements
```
Example:
if a > b
    out(a)
else
    out(b)
end
```
5.  Loop statements
```
i = 0
while i < 10
    out(i)
    i = i + 1
end
```
6.  Function declaration and call
```
fn add(a, b)
    return a + b
end
```
7.  class declaration and instantiation
```
class A
    fn init(a, b)
        this.a = a
        this.b = b
    end
end

C = A(1,2)
```
8.  Comments
```
# This is a comment
```
7. Built-in functions
```
out(a) # print a
in(a) # read input and store in a
sizeof(a) # return the size of list a
class.funct_list() # return the function list of class
class.var_list() # return the variable list of class
```
Text editor supports the following features:
1.  Open folder and file
2.  Save file
3.  Run file
4.  Syntax highlighting
5.  Auto Save
## 2. How to use
### 2.1. Run the program
To run the interpreter, you can use the following command:
```
py interpreter.py [file_name] # doesn't care about extension
py interpreter.py to run interactive terminal

```
To run the text editor, you can use the following command:
```
py App.py
```