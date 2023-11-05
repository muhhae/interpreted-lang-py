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
    def __init__(self, name: str, content: str, arg: list[str]):
        self.name = name
        self.content = content
        self.arg = arg
        self.local_interpreter = interpreter()

    def exec(self, arg):
        for a, b in zip(self.arg, arg):
            self.local_interpreter.var_list.append(var(a, b))
        ret = self.local_interpreter.execstring(self.content)
        self.local_interpreter.var_list.clear()
        return ret


class interpreter:
    def __init__(self, parent=None):
        self.parent = parent
        self.var_list = []
        self.label_list = []
        self.funct_list = []
        self.line_done = []
        pass

    def findVar(self, var_name):
        for e in self.var_list:
            if e.name == var_name:
                return e
        return -1

    def checkOperation(self, input: str):
        ok, res = self.checkkeyword(input)
        if ok:
            return res

        if input[0] == "[" and input[-1] == "]":
            tmp = input[input.find("[") + 1:input.rfind("]")
                        ].strip().split(",")
            tmp = [self.checkOperation(e.strip()) for e in tmp]
            return tmp

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
        bracketIndex = input.find('(')
        asgnIndex = input.find('=')
        if asgnIndex == -1 or (bracketIndex != -1 and bracketIndex < asgnIndex):
            self.checkkeyword(input)
            return
        tmpVar_name = input[0:asgnIndex].replace(" ", "").replace("\t", "")
        tmpVar_val = input[asgnIndex+1:].strip()
        if tmpVar_val.isdigit():
            tmpVar_val = float(tmpVar_val)
        else:
            # print("not ok")
            tmpVar_val = self.checkOperation(tmpVar_val)

        arr_index = -1
        if tmpVar_name.find("[") != -1:
            arr_index = tmpVar_name[tmpVar_name.find(
                "[") + 1:tmpVar_name.rfind("]")].strip()
            arr_index = self.checkOperation(arr_index)
            tmpVar_name = tmpVar_name[:tmpVar_name.find("[")]

        old_var = self.findVar(tmpVar_name)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            if arr_index != -1:
                old_var.value[arr_index] = tmpVar_val
            old_var.value = tmpVar_val

    def checkkeyword(self, inp: str) -> tuple[bool, any]:
        # print("masuk checkKeyword", inp)
        if inp.find("(") == -1:
            return (False, None)
        key = inp[:inp.find("(")]
        arg = inp[inp.find("(") + 1:inp.rfind(")")].strip().split(",")
        # print("arg", arg)
        arg_tmp = []
        str_tmp = ""
        bracket_level = 0

        for e in arg:
            if len(e) == 0:
                continue
            if e.count("(") != e.count(")"):
                bracket_level += e.count("(") - e.count(")")
            if bracket_level == 0:
                arg_tmp.append(str_tmp + e)
                str_tmp = ""
            else:
                str_tmp += e + ","
        # print("arg_tmp", arg_tmp)
        arg = arg_tmp

        arg_tmp = []
        str_tmp = ""
        total_quote = 0

        for e in arg:
            if len(e) == 0:
                continue
            if e.count("\"") != 0:
                total_quote += e.count("\"")
            if total_quote % 2 == 0:
                arg_tmp.append(str_tmp + e)
                str_tmp = ""
            else:
                str_tmp += e + ","
        arg = arg_tmp

        str_to_print = ""
        if key == "out":
            break_line = True
            for e in arg:
                e = e.strip()
                if e == "no_break":
                    break_line = False
                    continue
                if len(e) == 0:
                    continue
                if not isString(e):
                    e = self.checkOperation(e)
                if type(e) == str and isString(e):
                    e = e[1:-1]

                if e == None or e == 'None':
                    print("NULL", end="")
                    continue
                str_to_print += str(e)
            print(str_to_print, end="")
            if break_line:
                print()
            return (True, None)
        if key == "in":
            if len(arg) == 0:
                input()
                return (True, None)
            val = input()
            if val.isdigit():
                val = float(val)
            else:
                val = "\"" + val + "\""
            for e in arg:
                e.strip()
                if len(e) == 0:
                    continue
                old_var = self.findVar(e)
                if old_var == -1:
                    self.var_list.append(var(e, val))
                else:
                    old_var.value = val
            return (True, None)
        for fun in self.funct_list:
            if fun.name == key:
                for i, e in enumerate(arg):
                    e = e.strip()
                    e = self.checkOperation(e)
                    arg[i] = e
                return (True, fun.exec(arg))
        return (False, None)

    def execline(self, input: str):
        input = input.strip()
        if len(input) == 0:
            return
        if input[0] == '#':
            return
        if input[:4] == "goto":
            self.exec_goto(input)
            return
        self.checkAssignment(input)
        return

    def exec_if(self, inp: list[str]):
        # print("exec_if", inp, "\n")
        block_k = ["if", "while", "fn"]

        ls_cond = []
        ls_task = []

        tmp = ""
        nested = 0

        for e in inp:
            es = e.strip()
            for k in block_k:
                if es[:len(k)] == k:
                    nested += 1
                    break
            if e == "end":
                nested -= 1
            if nested > 1:
                tmp += es + '\n'
                continue

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
        # print("cond", ls_cond)

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

    def exec_goto(self, inp):
        # input("masuk goto")
        label_name = inp[4:].strip()
        for e in self.label_list:
            if e.name == label_name:
                goto_line = e.line
                str_to_exec = ""
                # print("goto", goto_line)
                for lin in self.line_done[goto_line:]:
                    str_to_exec += lin + "\n"
                # print("str_to_exec", str_to_exec)
                self.execstring(str_to_exec)
                break

    def def_fn(self, inp):
        # print("def fn")
        name = inp[0][inp[0].find("fn") + len('fn'):inp[0].find("(")].strip()
        arg = inp[0][inp[0].find("(") + 1:inp[0].rfind(")")].strip().split(",")
        arg = [e.strip() for e in arg]
        content = ""
        for e in inp[1:]:
            content += e + "\n"
        # print('name', name)
        # print('arg', arg)
        # print('content', content)
        self.funct_list.append(funct(name, content, arg))

    def execstring(self, input, is_root=False):
        block_k = ["if", "while", "fn", "execPy"]
        input = input.split("\n")
        # print("input ", input, '\n')
        in_block = 0
        block_type = ""
        block_content = []
        # print("ib", in_block)
        for i, l in enumerate(input):
            l = l.strip()
            if is_root:
                self.line_done.append(l)
            if len(l) == 0:
                continue
            if l[-1] == ':':
                label_name = l[:-1].strip()
                self.label_list.append(label(label_name, i))
                continue
            for k in block_k:
                if l[:len(k)] == k:
                    if in_block == 0:
                        block_type = k
                    in_block += 1
            if in_block > 0 and l[:4] == "end":
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
                        case "execPy":
                            str_to_exec = ""
                            for lin in block_content[1:]:
                                str_to_exec += lin + "\n"
                            exec(str_to_exec)
                    block_content.clear()
                    continue
            if in_block:
                block_content.append(l)
            else:
                # print("ln", l)
                if l[:6] == "return":
                    return self.checkOperation(l[6:])
                self.execline(l)

    def execfile(self, path):
        file_in = open(path, "r")
        self.execstring(file_in.read(), True)
        file_in.close()


def main():
    it = interpreter()
    line_input = ""
    input_tmp = ""

    key_block = ["if", "while", "fn", "execPy"]
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
            if line_input == "lab":
                ls = [e.name for e in it.label_list]
                print(ls)
                continue
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
