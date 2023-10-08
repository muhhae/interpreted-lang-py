from InfixToPostfix import checkBracket


def isCprOp(n):
    cpr = ["and", "or", "not", "!=", "==", "<=", ">=", "<", ">"]
    return n in cpr


def cprVal(n):
    if n in ["not"]:
        return 3
    if n in ["and", "or"]:
        return 2
    if n in ["!=", "==", "<=", ">=", "<", ">"]:
        return 1


def cprPostfix(n: list):
    aux = []
    res = []
    for e in n:
        pass


def compare(n):
    pass


if __name__ == "__main__":
    s = "12 <= 33 && 11 >= 24"
