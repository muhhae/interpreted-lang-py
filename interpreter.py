from LogicOperation import logicPostfix, calculateLogic, isString
import os
import sys

DEBUG = 0


def debug_log(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    print(*args, sep=sep, end=end, file=file, flush=flush) if DEBUG else None


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

    def exec(self, arg, parent=None, *args):
        local_interpreter = interpreter(parent)
        for a, b in zip(self.arg, arg):
            local_interpreter.var_list.append(var(a, b))
        for e in args:
            local_interpreter.var_list.append(e)
        ok, ret = local_interpreter.execstring(self.content)
        if ok:
            return ret
        return None


class class_def:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class class_var:
    def __init__(self, base: class_def, arg=[], parent=None):
        self.class_interpreter = interpreter(parent)
        self.class_interpreter.execstring(base.content)
        self.class_list = self.class_interpreter.class_list
        self.var_list = self.class_interpreter.var_list
        self.funct_list = self.class_interpreter.funct_list
        self.parent = parent
        self.exec_funct("init", arg)
        debug_log("Init Self = ", self)
        debug_log("Init Self.parent = ", self.parent)

    def exec_funct(self, name, arg):
        for e in self.funct_list:
            if e.name == name:
                return e.exec(arg, self.class_interpreter, var("this", self))
        return None

    def get_var(self, name):
        for e in self.var_list:
            if e.name == name:
                return e
        return None


class interpreter:
    def __init__(self, parent=None):
        self.parent = parent
        self.var_list = []
        self.label_list = []
        self.funct_list = []
        self.class_list = []
        self.line_done = []
        self.in_goto = False

    def find_var(self, var_name, recursive=False):
        for e in self.var_list:
            if e.name == var_name:
                return e
        if recursive and self.parent != None:
            return self.parent.find_var(var_name, True)
        return -1

    def find_class(self, class_name):
        debug_log("class_name \t\t-->", class_name)
        debug_log("self.class_list \t-->", [i.name for i in self.class_list])
        debug_log("self.parent \t\t-->", self.parent)
        for e in self.class_list:
            if e.name == class_name:
                debug_log("return e", e.name)
                return e
        if self.parent != None:
            return self.parent.find_class(class_name)
        return -1

    def find_funct(self, funct_name):
        debug_log("funct_name \t\t-->", funct_name)
        debug_log("self.funct_list \t-->", [i.name for i in self.funct_list])
        debug_log("self.parent \t\t-->", self.parent)
        for e in self.funct_list:
            if e.name == funct_name:
                return e
        if self.parent != None:
            return self.parent.find_funct(funct_name)
        return -1

    def check_operation(self, input: str):
        debug_log("input operation \t-->", input)
        if len(input) == 0:
            return None
        if input[0] == "[" and input[-1] == "]":
            tmp = input[input.find("[") + 1:input.rfind("]")
                        ].strip().split(",")
            if len(tmp) == 1 and tmp[0] == "":
                debug_log("Returning []")
                return []
            tmp = [self.check_operation(e.strip()) for e in tmp]
            return tmp

        cprOp = ["!=", "==", "<=", ">=",
                 "<", ">", "+", "/", "*", "-", "^", "%", "(", ")"]
        word_op = ["and", "or", "not"]

        tmp_2 = input.strip()

        str_tmp = ""
        list_str = []
        in_quote = False
        for c in tmp_2:
            if c == "\"":
                if in_quote:
                    list_str.append(str_tmp)
                    str_tmp = ""
                    in_quote = False
                else:
                    in_quote = True
                continue
            if in_quote:
                str_tmp += c
                continue

        debug_log("list_str \t\t-->", list_str)
        for i, e in enumerate(list_str):
            while tmp_2.count(f"\"{e}\""):
                tmp_2 = tmp_2.replace(f"\"{e}\"", f"$__str__{i}$")

        debug_log("tmp_2 \t\t\t-->", tmp_2)
        for i, e in enumerate(cprOp):
            while tmp_2.count(e):
                tmp_2 = tmp_2.replace(e, f"$__op__{i}$")

        for i, e in enumerate(word_op):
            prob_case = [f" {e} ",
                         f"){e}(",
                         f"){e} ",
                         f" {e}("]
            for a in prob_case:
                while tmp_2.count(a):
                    tmp_2 = tmp_2.replace(a, f"$__w_op__{i}$")

        if tmp_2.find("not ") == 0:
            tmp_2 = tmp_2.replace("not ", "$__w_op__2$")

        tmp_ls = tmp_2.split("$")

        # Check for list/array
        ls_tmp = []
        str_tmp = ""
        bracket_level = 0
        for e in tmp_ls:
            if len(e) == 0:
                continue
            if e[:7] == "__str__":
                str_in = int(e[7:])
                e = f"\"{list_str[str_in]}\""
            elif e[:8] == "__w_op__":
                w_op_in = int(e[8:])
                e = word_op[w_op_in]
            elif e[:6] == "__op__":
                op_in = int(e[6:])
                e = cprOp[op_in]
            if e.count("[") != e.count("]"):
                bracket_level += e.count("[") - e.count("]")
            if bracket_level == 0:
                ls_tmp.append(str_tmp + e)
                str_tmp = ""
            else:
                str_tmp += e
        tmp_ls = ls_tmp

        # Check for function
        ls_tmp = []
        in_funct = 0
        func_tmp = ""
        funct_index = False
        debug_log("tmp_ls operation \t-->", tmp_ls)
        for i, e in enumerate(tmp_ls):
            e = e.strip()
            if e in ["", " "]:
                continue
            if i == 0:
                ls_tmp.append(e)
                continue
            if e == "(":
                debug_log("ls_tmp[- 1] \t\t-->", ls_tmp[-1])
                if ls_tmp[-1][0].isalpha() and not ls_tmp[-1] in cprOp:
                    funct_index = True
                    in_funct += 1
                elif in_funct > 0:
                    in_funct += 1
            if e == ")" and in_funct:
                in_funct -= 1
            if in_funct > 0:
                func_tmp += e
            if in_funct == 0:
                if funct_index:
                    ls_tmp[-1] += func_tmp + e
                    funct_index = False
                else:
                    ls_tmp.append(e)
                func_tmp = ""
        tmp_ls = ls_tmp

        # Operation after formatting
        debug_log("tmp_ls after \t\t-->", tmp_ls)
        for i, e in enumerate(tmp_ls):
            e = e.strip()
            if e in ["", " "]:
                continue
            if e in cprOp or e in word_op:
                continue
            try:
                tmp_ls[i] = float(e)
                continue
            except:
                pass

            ok, res = self.checkkeyword(e)
            if ok:
                debug_log("res from keyword -->", res)
                tmp_ls[i] = res
            elif e == "NULL":
                tmp_ls[i] = None
            elif e.isdigit() or isString(e):
                tmp_ls[i] = e
            elif e.find(".") != -1:
                obj = e[:e.find(".")]
                e = e[e.find(".") + 1:]
                found_var = self.find_var(obj, True)
                if found_var != -1:
                    if type(found_var.value) != class_var:
                        print("error:", obj, "is not a class")
                        return None
                    var_val = found_var.value.get_var(e)
                    if var_val == None:
                        print("error:", e, "is not defined")
                        return None
                    tmp_ls[i] = var_val.value
                else:
                    print("error:", obj, "is not defined")
                    return
            elif e.find("[") != -1:
                arr_index = e[e.find("[") + 1:e.rfind("]")].strip()
                arr_index = self.check_operation(arr_index)
                e = e[:e.find("[")]
                found_var = self.find_var(e, True)
                if found_var != -1:
                    if type(found_var.value) != list:
                        print("error:", e, "is not an array")
                        return None
                    if arr_index + 1 > len(found_var.value):
                        print("error: index out of range")
                        return None
                    else:
                        tmp_ls[i] = found_var.value[arr_index]
                else:
                    print("error:", e, "is not defined")
                    return None
            else:
                found_var = self.find_var(e, True)
                if found_var != -1:
                    if type(found_var.value) == list:
                        val = found_var.value
                        return [e_arr for e_arr in val]
                    else:
                        tmp_ls[i] = found_var.value
                else:
                    print("error:", e, "is not defined")
                    return None
        debug_log("tmp_ls operation \t-->", tmp_ls)
        try:
            ls = calculateLogic(logicPostfix(tmp_ls))
            return ls
        except:
            debug_log("error in calculateLogic")
            return tmp_ls[0] if len(tmp_ls) == 1 else None

    def check_assigment(self, input: str):
        debug_log("input assign \t\t-->", input)
        bracketIndex = input.find('(')
        asgnIndex = input.find('=')
        if asgnIndex == -1 or (bracketIndex != -1 and bracketIndex < asgnIndex):
            return self.checkkeyword(input)
        tmpVar_name = input[0:asgnIndex].strip()
        tmpVar_val = input[asgnIndex+1:].strip()
        tmpVar_scope = "local"

        if tmpVar_name.find(" ") != -1:
            splt = tmpVar_name.split(" ")
            tmpVar_name = splt[-1]
            for e in splt[:-1]:
                if e == "global":
                    tmpVar_scope = "global"

        try:
            tmpVar_val = float(tmpVar_val)
        except:
            debug_log("Masuk check Operation")
            tmpVar_val = self.check_operation(tmpVar_val)
            debug_log("tmpVar_val \t\t-->", tmpVar_val)
        debug_log("val \t\t\t-->", tmpVar_val)
        arr_index = -1
        if tmpVar_name.find("[") != -1:
            arr_index = tmpVar_name[tmpVar_name.find(
                "[") + 1:tmpVar_name.rfind("]")].strip()
            arr_index = self.check_operation(arr_index)
            tmpVar_name = tmpVar_name[:tmpVar_name.find("[")]

        obj = None
        if "." in tmpVar_name:
            obj = tmpVar_name[tmpVar_name.find(".") + 1:]
            tmpVar_name = tmpVar_name[:tmpVar_name.find(".")]

        old_var = self.find_var(
            tmpVar_name, True if tmpVar_scope == "global" else False)
        if old_var == -1:
            self.var_list.append(var(tmpVar_name, tmpVar_val))
        else:
            if arr_index != -1:
                while len(old_var.value) < arr_index + 1:
                    old_var.value.append(None)
                old_var.value[arr_index] = tmpVar_val
            elif obj != None:
                if type(old_var.value) != class_var:
                    print("error:", tmpVar_name, "is not a class")
                    return
                var_val = old_var.value.get_var(obj)
                if var_val == None:
                    old_var.value.var_list.append(var(obj, tmpVar_val))
                else:
                    var_val.value = tmpVar_val
            else:
                old_var.value = tmpVar_val

    def checkkeyword(self, inp: str) -> tuple[bool, any]:
        debug_log("input keyword \t\t-->", inp)
        if inp.find("(") == -1:
            return (False, None)

        obj = None
        key = None
        arg = None

        def splitting(ch, str):
            bracket_level = 0
            # print("str", str)
            for i, c in enumerate(reversed(str)):
                # print("c", c)
                # print("bracket_level", bracket_level)
                if c == "(":
                    bracket_level += 1
                if c == ")":
                    bracket_level -= 1
                if bracket_level == 0 and c == ch:
                    return (str[:len(str) - i - 1], str[len(str) - i:])
            # print("return None")
            return None

        if "." in inp:
            if splitting(".", inp) != None:
                obj, key = splitting(".", inp)
                arg = key[key.find("(") + 1:key.rfind(")")].strip().split(",")
                key = key[:key.find("(")]

        key = inp[:inp.find("(")] if key == None else key
        arg = inp[inp.find("(") + 1:inp.rfind(")")
                  ].strip().split(",") if arg == None else arg

        debug_log("inp_key \t\t-->", key)
        debug_log("key \t\t\t-->", key)
        debug_log("obj \t\t\t-->", obj)
        if obj != None:
            old_var = None
            if obj.find("(") != -1:
                ok, obj = self.checkkeyword(obj)
                if not ok:
                    print("error:", obj, "is not defined")
                    return (False, None)
            else:
                old_var = self.find_var(obj, True)
                if old_var == -1:
                    print("error:", obj, "is not defined")
                    return (True, None)
                else:
                    obj = old_var.value
                if type(obj) != class_var:
                    print("error:", obj, "is not a class")
                    return (True, None)

            match key:
                case "var_list":
                    tmp = []
                    for e in obj.var_list:
                        tmp.append((e.name, e.value))
                    return (True, tmp)
                case "funct_list":
                    tmp = []
                    for e in obj.funct_list:
                        tmp.append((e.name, e.arg))
                    return (True, tmp)

            return (True, obj.exec_funct(key, arg))

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

        debug_log("key \t\t\t-->", key)
        debug_log("arg \t\t\t-->", arg)

        if key == "out":
            str_to_print = ""
            break_line = True
            for e in arg:
                e = e.strip()
                if e == "no_break":
                    break_line = False
                    continue
                if len(e) == 0:
                    continue
                if not isString(e):
                    e = self.check_operation(e)
                if type(e) == str and isString(e):
                    e = e[1:-1]
                str_to_print += str(e)
            str_to_print = str_to_print.replace("\\n", "\n")
            str_to_print = str_to_print.replace("\\t", "\t")
            str_to_print = str_to_print.replace("None", "NULL")
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
                old_var = self.find_var(e, True)
                if old_var == -1:
                    self.var_list.append(var(e, val))
                else:
                    old_var.value = val
            return (True, None)
        if key == "sizeof":
            if len(arg) == 0:
                return (True, None)
            old_var = self.find_var(arg[0], True)
            if old_var == -1:
                print("error:", arg[0], "is not defined")
                return (True, None)
            if type(old_var.value) == list:
                return (True, len(old_var.value))
            else:
                print("error:", arg[0], "is not an array")
                return (True, None)
        func = self.find_funct(key)
        if func != -1:
            for i, e in enumerate(arg):
                e = e.strip()
                e = self.check_operation(e)
                arg[i] = e
            return (True, func.exec(arg, self))
        cls = self.find_class(key)
        if cls != -1:
            for i, e in enumerate(arg):
                e = e.strip()
                e = self.check_operation(e)
                arg[i] = e
            # print("arg", arg)
            return (True, class_var(cls, arg, self))
        return (False, None)

    def execline(self, input: str):
        input = input.strip()
        if len(input) == 0:
            return
        cmt_index = input.find("#")
        if cmt_index != -1:
            input = input[:cmt_index]
        if input[:4] == "goto":
            self.exec_goto(input)
            return
        if input[:len('import')] == "import":
            mod = input[len('import'):].strip()
            if not os.path.exists(mod):
                print("error :", mod, "does not exist")
                return
            self.execfile(mod)
            return
        res = self.check_assigment(input)
        return res

    def exec_if(self, inp: list[str]):
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

            cond_key = es if es == "else" else es[:es.find(" ")]
            # debug_log("es \t\t\t-->", es)
            # debug_log("conditional key \t-->", cond_key)

            if cond_key == 'if':
                ls_cond.append(e[2:].strip())
            elif cond_key == 'else_if':
                ls_cond.append(e[7:].strip())
                ls_task.append(tmp)
                tmp = ""
            elif cond_key == 'else':
                ls_cond.append('1')
                ls_task.append(tmp)
                tmp = ""
            else:
                tmp += es + '\n'
        ls_task.append(tmp)
        debug_log("condition \t\t-->", ls_cond)

        for condition, task in zip(ls_cond, ls_task):
            if self.check_operation(condition):
                return self.execstring(task)
                # return interpreter(self).execstring(task)
        return (False, None)

    def exec_while(self, inp):
        condition = inp[0][inp[0].find("while") + len('while'):]
        condition.strip()
        str = ""
        for e in inp[1:]:
            str += e + "\n"
        while self.check_operation(condition):
            ok, ret = self.execstring(str)
            # ok, ret = interpreter(self).execstring(str)
            if ok:
                return (True, ret)
        return (False, None)

    def exec_goto(self, inp):
        label_name = inp[4:].strip()
        for e in self.label_list:
            if e.name == label_name:
                in_goto = True
                goto_line = e.line
                str_to_exec = ""
                for lin in self.line_done[goto_line:]:
                    str_to_exec += lin + "\n"
                ok, ret = self.execstring(str_to_exec)
                in_goto = False
                if ok:
                    return (True, ret)
                return (False, None)
        return (False, None)

    def def_fn(self, inp):
        name = inp[0][inp[0].find("fn") + len('fn'):inp[0].find("(")].strip()
        arg = inp[0][inp[0].find("(") + 1:inp[0].rfind(")")].strip().split(",")
        arg = [e.strip() for e in arg]
        content = ""
        for e in inp[1:]:
            content += e + "\n"
        fn_tmp = funct(name, content, arg)
        self.funct_list.append(fn_tmp)

    def def_class(self, inp):
        name = inp[0][inp[0].find("class") + len('class'):].strip()
        content = ""
        for e in inp[1:]:
            content += e + "\n"
        self.class_list.append(class_def(name, content))

    def execstring(self, input, is_root=False):
        block_k = ["if", "while", "fn", "execPy", "class"]
        input = input.split("\n")
        in_block = 0
        block_type = ""
        block_content = []
        for i, l in enumerate(input):
            l = l.strip()
            if is_root and not self.in_goto:
                self.line_done.append(l)
            if len(l) == 0:
                continue
            if l[-1] == ':':
                label_name = l[:-1].strip()
                self.label_list.append(label(label_name, i))
                continue

            key = l[:l.find(" ")] if l.find(" ") != -1 else l
            if key in block_k:
                if not in_block:
                    block_type = key
                in_block += 1
            if in_block > 0 and key == "end":
                in_block -= 1
                if in_block == 0:
                    match block_type:
                        case "if":
                            ok, ret = self.exec_if(block_content)
                            if ok:
                                return (True, ret)
                        case "while":
                            ok, ret = self.exec_while(block_content)
                            if ok:
                                return (True, ret)
                        case "fn":
                            self.def_fn(block_content)
                        case "execPy":
                            str_to_exec = ""
                            for lin in block_content[1:]:
                                str_to_exec += lin + "\n"
                            exec(str_to_exec)
                        case "class":
                            self.def_class(block_content)
                    block_content.clear()
                    continue
            if in_block:
                block_content.append(l)
            else:
                if key == "return":
                    ret = self.check_operation(l[6:].strip())
                    return (True, ret)
                self.execline(l)
        return (False, None)

    def execfile(self, path, chdir=False):
        os.chdir(os.path.dirname(path)) if chdir else None
        file_in = open(os.path.basename(path) if chdir else path, "r")
        self.execstring(file_in.read(), True)
        file_in.close()


def main():
    it = interpreter()
    line_input = ""
    input_tmp = ""

    key_block = ["if", "while", "fn", "execPy", "class"]
    in_block = 0

    if len(sys.argv) == 1 or sys.argv[1] == "-i":
        if len(sys.argv) == 3:
            print(">> import", sys.argv[2])
            it.execfile(sys.argv[2], True)
            print()
        no_print = False
        while not line_input in ["/q", "/quit", "/exit"]:
            if not no_print:
                if in_block:
                    line_input = input(".. ").strip()
                else:
                    line_input = input(">> ").strip()
            else:
                no_print = False
                line_input = input().strip()
            input_tmp += "\n" + line_input

            key = line_input[:line_input.find(" ")] if line_input.find(
                " ") != -1 else line_input
            arg = line_input[line_input.find(" "):]

            debug_log("key \t\t\t-->", key)
            if key in key_block:
                in_block += 1
            if key == "cd":
                arg = arg.strip()
                # print('cd', arg)
                no_print = True
                debug_log(f"is {arg} path ?",
                          "Yes" if os.path.isdir(arg) else "No")
                if os.path.isdir(arg):
                    os.chdir(arg)
                continue
            if line_input == "lab":
                ls = [e.name for e in it.label_list]
                print(ls)
                continue
            if line_input == "cls":
                os.system("cls")
                continue
            if line_input == "wd":
                print(os.getcwd())
                continue
            if line_input == "var":
                ls = [(e.name, e.value) for e in it.var_list]
                for e in ls:
                    print(e, sep="\n")
                continue
            if line_input == "funct":
                ls = [(e.name, e.arg) for e in it.funct_list]
                print(ls)
                continue
            if line_input == "it":
                print("interpreter", it)
                continue
            if line_input == "end":
                in_block -= 1
            if in_block == 0:
                ok, ret = it.execstring(input_tmp)
                print(ret) if ret != None else None
                input_tmp = ""

    else:
        it.execfile(sys.argv[1], True)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
