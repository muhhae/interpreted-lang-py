from InfixToPostfix import opVal


def cprVal(n):
    if n in ["not"]:
        return 2
    if n in ["and", "or"]:
        return 1
    if n in ["!=", "==", "<=", ">=", "<", ">"]:
        return 3
    return opVal(n)


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


def isOpLgc(c):
    cprOp = ["and", "or", "not", "!=", "==", "<=", ">=",
             "<", ">", "+", "/", "*", "-", "^", "%", "(", ")"]
    return c in cprOp


def logicPostfix(ls: list):
    # print("ls", ls)
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
    # print("post:", n)
    result = []
    for c in n:
        if not isOpLgc(c):
            result.append(float(c))
            continue

        b = result.pop()
        if c != "not":
            if len(result) == 0 or isOpLgc(result[-1]):
                a = 0
            else:
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
