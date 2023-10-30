from LogicOperation import logicPostfix, calculateLogic, isString
import sys


class var:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value


class label:
    def __init__(self, name: str, line: int):
        self.name = name
        self.line = line


class funct:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content
        self.arg = []
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

    def checkOperation(self, input: str):
        # print("masuk chekOp", input)
        cprOp = ["and", "or", "not", "!=", "==", "<=", ">=",
                 "<", ">", "+", "/", "*", "-", "^", "%", "(", ")"]

        tmp_2 = input.replace(" ", "")

        for i, e in enumerate(cprOp):
            while tmp_2.count(e):
                tmp_2 = tmp_2.replace(e, f" op{i} ")

        tmp_ls = tmp_2.split(" ")
        for i, e in enumerate(tmp_ls):
            if e in ["", " "]:
                continue
            if e[:2] == "op":
                op_in = int(e[2:])
                tmp_ls[i] = cprOp[op_in]
            else:
                if type(e) == str:
                    if e.isdigit() or isString(e):
                        tmp_ls[i] = e
                    else:
                        find_var = self.findVar(e)
                        if find_var != -1:
                            # print("ketemu", find_var.name, find_var.value)
                            tmp_ls[i] = find_var.value
                        else:
                            print("error:", e, "is not defined")

        ls = 0
        # print("tmp_ls", tmp_ls)
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
        else:
            tmpVar_val = self.checkOperation(tmpVar_val)
        old_var = self.findVar(tmpVar_name)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            old_var.value = tmpVar_val

    def checkkeyword(self, input: str):
        b_out = input[:3] == "out"

        if b_out:
            tmp_val = input[3:].strip().split(";")
            # print("tmp_val", tmp_val)
            for e in tmp_val:
                e.strip()
                if len(e) == 0:
                    continue
                if not isString(e):
                    e = self.checkOperation(e)
                if type(e) == str and isString(e):
                    e = e[1:-1]

                if e == None or e == 'None':
                    print("NULL", end="")
                    continue
                print(e, end="")
            print()
            return True

    def execline(self, input: str):

        input = input.strip()

        if self.checkkeyword(input):
            return
        self.checkAssignment(input)
        return

    def exec_if(self, inp: list[str]):
        # print("exec if")

        ls_cond = []
        ls_task = []

        tmp = ""

        for e in inp:
            es = e.strip()
            if es[:2] == 'if':
                ls_cond.append(e[2:].strip())
            elif es[:7] == 'else_if':
                ls_cond.append(e[7:].strip())
                ls_task.append(tmp)
                tmp = ""
            elif es[:4] == 'else':
                ls_cond.append('1')
                ls_task.append(tmp)
                tmp = ""
            else:
                tmp += es + '\n'
        ls_task.append(tmp)

        for condition, task in zip(ls_cond, ls_task):
            # print("condition", condition)
            # print("task", task)
            if self.checkOperation(condition):
                self.execstring(task)
                break

    def exec_while(self, inp):
        condition = inp[0][inp[0].find("while") + len('while'):]
        condition.strip()
        str = ""
        for e in inp[1:]:
            str += e + "\n"
        while self.checkOperation(condition):
            self.execstring(str)

    def def_fn(self, inp):
        pass

    def execstring(self, input):
        # print("ip\n", input)
        block_k = ["if", "while", "fn"]
        input = input.split("\n")
        in_block = 0
        block_type = ""
        block_content = []
        # print("ib", in_block)
        for l in input:
            l = l.strip()
            if l[:1] == "#":
                continue
            for k in block_k:
                if l[:len(k)] == k:
                    if in_block == 0:
                        block_type = k
                    in_block += 1
            if l[:4] == "end":
                in_block -= 1
                # print("ib", in_block)
                if in_block == 0:
                    # print("bc", block_content)
                    match block_type:
                        case "if":
                            self.exec_if(block_content)
                        case "while":
                            self.exec_while(block_content)
                        case "fn":
                            self.def_fn(block_content)
                    block_content.clear()
                    continue
            if in_block:
                block_content.append(l)
            else:
                # print("ln", l)
                self.execline(l)

    def execfile(self, path):
        file_in = open(path, "r")
        self.execstring(file_in.read())
        file_in.close()


def main():
    it = interpreter()
    line_input = ""
    input_tmp = ""

    key_block = ["if", "while", "fn"]
    in_block = False

    if len(sys.argv) == 1:
        while not line_input in ["/q", "/quit", "/exit"]:
            if in_block:
                line_input = input(".. ").strip()
            else:
                line_input = input(">> ").strip()
            input_tmp += "\n" + line_input
            for e in key_block:
                if line_input[0:len(e)] == e:
                    in_block = True
                    break
            if line_input == "var":
                ls = [e.value for e in it.var_list]
                print(ls)
                continue
            if line_input == "end":
                in_block = False
            if not in_block:
                it.execstring(input_tmp)
                input_tmp = ""
    else:
        it.execfile(sys.argv[1])


if __name__ == "__main__":
    main()
