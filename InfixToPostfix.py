from rich import print
from rich.table import Table


def isOp(c):
    op = ["+", "/", "*", "-", "^", "(", ")"]
    return c in op


def opVal(op: str):
    match op:
        case "+" | "-": return 0
        case "*" | "/": return 1
        case "^": return 2


def listprint(l: list):
    for e in l:
        pass
        # print(e, end="")


def listToStr(l: list):
    s = ""
    for e in l:
        s += str(e)
    return s


def checkBracket(n: str):
    openBracket = n.count("(")
    closeBracket = n.count(")")
    if openBracket > closeBracket:
        n += ")" * (openBracket - closeBracket)
    else:
        n = "(" * (closeBracket - openBracket) + n
    return n


def infixToPostfix(n: str):
    n = checkBracket(n)
    # print("infix:", n)
    result = []
    aux = []

    fullNum = False
    cTemp = ""

    table = Table("Step", "Input", "Operator", "Result",
                  title="Infix To Postfix",
                  title_justify="center",
                  caption_justify="center",)
    step = 0
    for i, c in enumerate(n):
        if c == " ":
            continue
        if c == "-" and (isOp(n[i-1]) or i == 0):
            cTemp += c
            if i == len(n) - 1:
                result.append(cTemp)
                result.append(" ")
                step += 1
                table.add_row(str(step), cTemp, listToStr(
                    aux), listToStr(result))
                table.add_section()
            continue
        if isOp(c):
            if cTemp != "":
                if cTemp != "-":
                    result.append(cTemp)
                    result.append(" ")
                    cTemp = ""
                else:
                    aux.append(cTemp)
                    cTemp = ""
                step += 1
                table.add_row(str(step), cTemp, listToStr(
                    aux), listToStr(result))
                table.add_section()
        if not isOp(c):
            cTemp += c
            if i == len(n) - 1:
                result.append(cTemp)
                result.append(" ")
                step += 1
                table.add_row(str(step), cTemp, listToStr(
                    aux), listToStr(result))
                table.add_section()
            continue
        elif c == '(':
            aux.append(c)
        elif c == ')':
            while len(aux) > 0 and aux[-1] != '(':
                result.append(aux.pop())
                result.append(" ")
            aux.pop()
        else:
            while len(aux) > 0 and aux[-1] != "(" and opVal(aux[-1]) >= opVal(c):
                result.append(aux.pop())
                result.append(" ")
            aux.append(c)
        step += 1
        table.add_row(str(step), c, listToStr(aux), listToStr(result))
        table.add_section()

    while len(aux) > 0:
        result.append(aux.pop())
        result.append(" ")

    step += 1
    table.add_row(str(step), "", listToStr(aux), listToStr(result))
    table.add_section()

    # print(table)
    strResult = listToStr(result)
    # print("postfix\t:", strResult)
    return result


def calculatePostfix(n: list):
    result = []
    # print("\nCalculating...\n")
    for c in n:
        if c == " ":
            continue
        if not isOp(c):
            result.append(float(c))
            continue

        b = result.pop()
        a = result.pop()

        match c:
            case "*":
                # print(a, "*", b, "=", a*b)
                result.append(a*b)
            case "+":
                # print(a, "+", b, "=", a+b)
                result.append(a+b)
            case "-":
                # print(a, "-", b, "=", a-b)
                result.append(a-b)
            case "/":
                # print(a, "/", b, "=", a/b)
                result.append(a/b)
            case "^":
                # print(a, "^", b, "=", a**b)
                result.append(a**b)
    # print()
    res = result.pop()
    # print("result\t:", res)
    return res


def bracketFunc(n: list):
    result = []
    for c in n:
        if c == " ":
            continue
        if not isOp(c):
            result.append(c)
            continue

        b = result.pop()
        a = result.pop()

        result.append('(' + a + c + b + ')')
    # print()
    res = result.pop()
    # print("result\t:", res)
    return res


def initTugas(s: str):
    # print("infix\t:", s)
    Str = infixToPostfix(s)
    for e in Str:
        if e.isdigit():
            calculatePostfix(Str)
            break
    # print()


if __name__ == "__main__":
    Str = [
        "ab + ac * ad"
        # "1 * 2 * (3 + 4 * (5 + 6))"
    ]
    # print("-- Infix To Postfix -- \n")
    for e in Str:
        initTugas(e)
