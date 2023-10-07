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

    def checkOperator(self, input):
        tmpVar = infixToPostfix(str(input))
        for j, el in enumerate(tmpVar):
            if isOp(el) or el == " ":
                continue
            other_var = self.findVar(el)
            if other_var != -1:
                tmpVar[j] = other_var.value
            else:
                if el.isdigit():
                    el = float(el)
                tmpVar[j] = el

        for e in tmpVar:
            if e == " " or isOp(e):
                continue
            if type == str:
                print(f"var {e} not found")
                return
        res = calculatePostfix(tmpVar)
        return res

    def checkAssignment(self, input: str):
        if input.count('=') > 1:
            return
        asgnIndex = input.find('=')
        if asgnIndex == -1:
            return
        tmpVar_name = input[0:asgnIndex].replace(" ", "").replace("\t", "")
        tmpVar_val = input[asgnIndex+1:].strip()
        if tmpVar_val.isdigit():
            tmpVar_val = float(tmpVar_val)
        elif tmpVar_val[0] != "\"" and tmpVar_val[-1] != "\"":
            tmpVar_val = self.checkOperator(tmpVar_val)

        old_var = self.findVar(tmpVar_name)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            old_var.value = tmpVar_val

    def checkkeyword(self, input: str):
        b_out = input[:3] == "out"

        if b_out:
            tmp_val = input[3:].strip().split(";")
            for e in tmp_val:
                e.strip()
                if len(e) == 0:
                    continue
                if e[0] != "\"" and e[-1] != "\"":
                    e = self.checkOperator(e)
                else:
                    e = e.replace("\"", "")
                print(e, end="")
            print()
            return

    def execline(self, input: str):

        input = input.strip()

        if self.checkkeyword(input):
            return
        self.checkAssignment(input)
        return

    def exec_if(self, input):
        condition = input[0][input[0].find("if") + 2:]
        condition.strip()

        lg = ["and", "or", "<=", "<", ">=", ">", "==", "not", "!="]
        key_loc = -1
        lgc_type = ""

        cond = False
        for e in lg:
            tmp = condition.find(e)
            if tmp != -1:
                lgc_type = e
                key_loc = tmp
                break

        if key_loc == -1:
            return

        a = condition[:key_loc].strip()
        b = condition[key_loc + len(lgc_type):].strip()

        a = self.checkOperator(a)
        b = self.checkOperator(b)

        str = ""

        for e in input[1:]:
            str += e + "\n"

        match lgc_type:
            case ">":
                if a > b:
                    self.execstring(str)
            case ">=":
                if a >= b:
                    self.execstring(str)
            case "<=":
                if a <= b:
                    self.execstring(str)
            case "<":
                if a < b:
                    self.execstring(str)
            case "!=":
                if a != b:
                    self.execstring(str)
            case "==":
                if a == b:
                    self.execstring(str)

    def execstring(self, input):
        input = input.split("\n")
        in_block = False
        block_type = ""
        block_content = []
        for l in input:
            if l[:1] == "#":
                continue
            if l[:2] == "if":
                block_type = "if"
                in_block = True
            elif l[:4] == "END":
                match block_type:
                    case "if":
                        self.exec_if(block_content)
                in_block = False
                block_content.clear()
            if in_block:
                block_content.append(l)
            else:
                self.execline(l)

    def execfile(self, path):
        file_in = open(path, "r")
        self.execstring(file_in.read())
        file_in.close()


it = interpreter()
it.execfile("input.pyhk")

# for e in in_str:
#     it.execline(e)

# it.execstring(one_str)

# for e in it.var_list:
# print(e.name, e.value)
