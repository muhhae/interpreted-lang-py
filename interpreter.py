from InfixToPostfix import infixToPostfix, calculatePostfix, isOp, logicPostfix, calculateLogic


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

        # print(tmpVar)
        for e in tmpVar:
            if e == "None":
                return
            if e == " " or isOp(e):
                continue
            if type(e) == str and e.isalnum():
                print(f"var {e} not found")
                return
            if e == None:
                return
        res = calculatePostfix(tmpVar)
        return res

    def checkTruthValue(self, input: str):
        cprOp = ["and", "or", "not", "!=", "==", "<=", ">=",
                 "<", ">", "+", "/", "*", "-", "^", "%", "(", ")"]

        tmp = input.replace(" ", "")
        tmp_2 = input.replace(" ", "")
        logic = False

        for e in cprOp:
            while tmp.count(e):
                logic = True
                tmp = tmp.replace(e, " ")
        for e in tmp.split(" "):
            if e == "" or type(e) != str:
                continue
            tmp_2 = tmp_2.replace(e, str(self.checkOperator(e)))
        if not logic:
            return self.checkOperator(tmp_2)

        for i, e in enumerate(cprOp):
            while tmp_2.count(e):
                tmp_2 = tmp_2.replace(e, f" op{i} ")

        tmp_ls = tmp_2.split(" ")
        for i, e in enumerate(tmp_ls):
            if e[:2] == "op":
                op_in = int(e[2:])
                tmp_ls[i] = cprOp[op_in]
        # print("tmp_ls", tmp_ls)
        # print("ps", logicPostfix(tmp_ls))
        # print("res", calculateLogic(logicPostfix(tmp_ls)))
        ls = 0
        try:
            ls = calculateLogic(logicPostfix(tmp_ls))
        except:
            return 0
        return ls

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
            tmpVar_val = self.checkTruthValue(tmpVar_val)
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

                if e == None or e == 'None':
                    print("NULL", end="")
                    continue
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

        if self.checkTruthValue(condition):
            str = ""
            for e in input[1:]:
                str += e + "\n"
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
#     print(e.name, e.value)
