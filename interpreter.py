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
        tmpVar_name = input[0:asgnIndex].replace(" ", "")
        tmpVar_val = input[asgnIndex+1:].replace(" ", "")

        if tmpVar_val[0] != "\"" and tmpVar_val[-1] != "\"":
            other_var = self.findVar(tmpVar_val)
            if other_var != -1:
                tmpVar_val = other_var.value

        old_var = self.findVar(tmpVar_name)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            old_var.value = tmpVar_val

    def checkOperator(self, input: str):
        pass

    def execline(self, input: str):
        self.checkAssignment(input)
        return

    def runstring(self, input):
        pass

    def runfile(self, path):
        pass


in_str = [
    "A = 10",
    "B = A",
    "A = 99"
]
it = interpreter()

for e in in_str:
    it.execline(e)

for e in it.var_list:
    print(e.name, e.value)
