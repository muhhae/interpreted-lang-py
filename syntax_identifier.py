class syntax_identifier:
    def __init__(self):
        self.var_list = []
        self.funct_list = ['out', 'in', 'sizeof', 'funct_list', 'var_list']
        self.class_list = ['this']
        self.label_list = []

    def identify_string(self, str):
        lines = str.split('\n')
        for line in lines:
            self.identify_line(line)
        # print(self.var_list)
        # print(self.funct_list)
        # print(self.class_list)
        # print(self.label_list)

    def identify_line(self, line: str):
        line = line.strip()
        if line == '':
            return
        if line[-1] == ':':
            self.label_list.append(line[:-1])
            return
        line = line.replace('(', ' ( ')
        line = line.replace(')', ' ) ')
        line = line.replace('=', ' = ')
        line = line.replace('.', ' . ')
        line = line.replace(',', ' , ')
        line = line.replace('[', ' [ ')
        line = line.replace(']', ' ] ')

        tokens = line.split(' ')
        tokens = list(filter(lambda x: x != '', tokens))
        tokens = list(filter(lambda x: x != ',', tokens))
        # tokens = list(filter(lambda x: x != '(', tokens))
        # tokens = list(filter(lambda x: x != ')', tokens))
        for i in range(len(tokens)):
            tokens[i] = tokens[i].strip()
        key = tokens[0]
        match key:
            case 'fn':
                self.funct_list.append(
                    tokens[1]) if tokens[1] not in self.funct_list else None
                # print(tokens[3:tokens.index(')')])
                # print(tokens[4:tokens.index(')')])
                for e in tokens[3:tokens.index(')')]:
                    self.var_list.append(
                        e) if e not in self.var_list else None
            case 'class':
                self.class_list.append(
                    tokens[1]) if tokens[1] not in self.class_list else None
        if len(tokens) < 2:
            return
        if tokens[1] == '=' or tokens[1] == '.' or tokens[1] == '[':
            self.var_list.append(
                tokens[0]) if tokens[0] not in self.var_list else None
            if tokens[1] == '.' and tokens[3] != '(':
                self.var_list.append(
                    tokens[2]) if tokens[2] not in self.var_list else None


if __name__ == '__main__':
    file = open('Script/input.pyhk', 'r')
    identifier = syntax_identifier()
    identifier.identify_string(file.read())
    print('var', identifier.var_list)
    print('fn', identifier.funct_list)
    print('class', identifier.class_list)
    print('label', identifier.label_list)

    file.close()
