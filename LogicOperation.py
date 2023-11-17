
def isString(n: str):
    return (n[0] == "\"" and n[-1] == "\"" and n.count('"') == 2)


def cprVal(n):
    if n in ["not"]:
        return 2
    if n in ["and", "or"]:
        return 1
    if n in ["!=", "==", "<=", ">=", "<", ">"]:
        return 3
    match n:
        case "+" | "-": return 4
        case "*" | "/": return 5
        case "^": return 6


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
    n = checkBracketLs(ls)
    result = []
    aux = []

    for c in n:
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
    # print("calculateLogic", n)
    OPERATION = {
        "and": lambda a, b: int(a and b),
        "or": lambda a, b: int(a or b),
        "not": lambda a: int(not a),
        "!=": lambda a, b: int(a != b),
        "==": lambda a, b: int(a == b),
        "<=": lambda a, b: int(a <= b),
        ">=": lambda a, b: int(a >= b),
        "<": lambda a, b: int(a < b),
        ">": lambda a, b: int(a > b),
        "+": lambda a, b: a + b,
        "/": lambda a, b: a / b,
        "*": lambda a, b: a * b,
        "-": lambda a, b: a - b,
        "^": lambda a, b: a ** b,
        "%": lambda a, b: a % b
    }
    result = []
    for c in n:
        # print("c", c)
        # print("result", result)
        try:
            result.append(float(c))
            continue
        except:
            pass

        if isString(c):
            result.append(c[1:-1])
            continue

        b = result.pop()
        if c != "not":
            if len(result) == 0 or isOpLgc(result[-1]):
                a = 0
            else:
                a = result.pop()
        # print("a", a)
        # print("b", b)
        a = int(a) if type(a) == float and a % 1 == 0 else a
        b = int(b) if type(b) == float and b % 1 == 0 else b
        # print("1 a", a)
        # print("1 b", b)
        try:
            if c == "not":
                tmp = OPERATION[c](b)
            else:
                tmp = OPERATION[c](a, b)
            result.append(tmp)
        except Exception as e:
            print("error:", e)
            return None

    # #print("result after op", result)
    res = result.pop()
    if type(res) == float:
        if res.is_integer():
            return int(res)
    if type(res) == str:
        return "\"" + res + "\""
    return res
