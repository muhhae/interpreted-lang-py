from InfixToPostfix import infixToPostfix, calculatePostfix, isOp


class var:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class label:
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line


class funct:
    def __init__(self, name: str, content: str):
        pass

    def call(self, param: str):
        pass


class interpreter:
    def __init__(self):
        self.var_list = []
        self.label_list = []
        self.funct_list = []
        pass

    def findVar(self, var_name):
        for e in self.var_list:
            if e.name == var_name:
                return e
        return -1

    def checkAssignment(self, input: str):
        if input.count('=') > 1:
            print("Syntax Error")
            return
        asgnIndex = input.find('=')
        if asgnIndex == -1:
            return
        tmpVar_name = input[0:asgnIndex].strip()
        tmpVar_val = input[asgnIndex+1:].strip()
        if tmpVar_val.isdigit():
            tmpVar_val = float(tmpVar_val)
        elif tmpVar_val[0] != "\"" and tmpVar_val[-1] != "\"":
            other_var = self.findVar(tmpVar_val)
            if other_var != -1:
                tmpVar_val = other_var.value

        old_var = self.findVar(tmpVar_name)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            old_var.value = tmpVar_val

    def checkOperator(self):
        for i, v in enumerate(self.var_list):
            tmpVar = infixToPostfix(str(v.value))
            for j, el in enumerate(tmpVar):
                if isOp(el):
                    continue
                other_var = self.findVar(el)
                if other_var != -1:
                    tmpVar[j] = other_var.value
            self.var_list[i].value = calculatePostfix(tmpVar)

    def execline(self, input: str):
        self.checkAssignment(input)
        self.checkOperator()
        return

    def runstring(self, input):
        pass

    def runfile(self, path):
        pass


in_str = [
    "A = 45",
    "B = 100",
    "C = A + B"
]
it = interpreter()

for e in in_str:
    it.execline(e)

for e in it.var_list:
    print(e.name, e.value)
