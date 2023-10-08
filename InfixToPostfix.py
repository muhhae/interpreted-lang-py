from rich import print
from rich.table import Table


def isOp(c):
    op = ["+", "/", "*", "-", "^", "%", "(", ")"]
    return c in op


def opVal(op: str):
    match op:
        case "+" | "-": return 4
        case "*" | "/": return 5
        case "^": return 6


def cprVal(n):
    if n in ["not"]:
        return 3
    if n in ["and", "or"]:
        return 2
    if n in ["!=", "==", "<=", ">=", "<", ">"]:
        return 1
    return opVal(n)


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


def checkBracketLs(n: list):
    openBracket = n.count("(")
    closeBracket = n.count(")")
    if openBracket > closeBracket:
        for i in range(openBracket - closeBracket):
            n.append(")")
    else:
        for i in range(closeBracket - openBracket):
            n.insert(0, "(")
    return n


def infixToPostfix(n: str):
    n = checkBracket(n)
    result = []
    aux = []

    fullNum = False
    cTemp = ""

    for i, c in enumerate(n):
        if c == " ":
            continue
        if c == "-" and (isOp(n[i-1]) or i == 0):
            cTemp += c
            if i == len(n) - 1:
                result.append(cTemp)
                result.append(" ")
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
        if not isOp(c):
            cTemp += c
            if i == len(n) - 1:
                result.append(cTemp)
                result.append(" ")
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

    while len(aux) > 0:
        result.append(aux.pop())
        result.append(" ")

    # print(table)
    strResult = listToStr(result)
    # print("postfix\t:", strResult)
    return result


def isOpLgc(c):
    cprOp = ["and", "or", "not", "!=", "==", "<=", ">=",
             "<", ">", "+", "/", "*", "-", "^", "%", "(", ")"]
    return c in cprOp


def logicPostfix(ls: list):
    n = checkBracketLs(ls)
    result = []
    aux = []

    for i, c in enumerate(n):
        if c in [" ", ""]:
            continue
        if not isOpLgc(c):
            result.append(c)
        elif c == '(':
            aux.append(c)
        elif c == ')':
            while len(aux) > 0 and aux[-1] != '(':
                result.append(aux.pop())
            aux.pop()
        else:
            while len(aux) > 0 and aux[-1] != "(" and cprVal(aux[-1]) >= cprVal(c):
                result.append(aux.pop())
            aux.append(c)

    while len(aux) > 0:
        result.append(aux.pop())
    return result


def calculateLogic(n: list):
    result = []
    for c in n:
        if not isOpLgc(c):
            result.append(float(c))
            continue

        b = result.pop()
        if c != "not":
            a = result.pop()

        match c:
            case "*":
                result.append(a*b)
            case "+":
                result.append(a+b)
            case "-":
                result.append(a-b)
            case "/":
                result.append(a/b)
            case "^":
                result.append(a**b)
            case "%":
                result.append(a % b)
            case "and":
                result.append(int(a and b))
            case "or":
                result.append(int(a or b))
            case "not":
                result.append(int(not b))
            case "==":
                result.append(int(a == b))
            case "!=":
                result.append(int(a != b))
            case "<=":
                result.append(int(a <= b))
            case ">=":
                result.append(int(a >= b))
            case "<":
                result.append(int(a < b))
            case ">":
                result.append(int(a > b))
    res = result.pop()
    return res


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
            case "%":
                result.append(a % b)
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
        "ab + ac * ad",
        # "1 * 2 * (3 + 4 * (5 + 6))",
        "a > 1 and a < 2"
    ]
    # print("-- Infix To Postfix -- \n")
    for e in Str:
        initTugas(e)
