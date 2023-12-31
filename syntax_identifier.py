import os


class syntax_identifier:
    def __init__(self, work_dir: str = None):
        if work_dir is not None and os.path.exists(work_dir):
            self.work_dir = work_dir
        self.var_list = []
        self.funct_list = ['out', 'in', 'sizeof', 'funct_list', 'var_list']
        self.class_list = ['this']
        self.label_list = []

    def identify_string(self, str):
        lines = str.split('\n')
        for line in lines:
            self.identify_line(line)

    def identify_file(self, file):
        self.identify_string(file.read())

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
            case 'import':
                if len(tokens) < 2:
                    return
                path = ''
                for i in tokens[1:]:
                    path += i
                # print('import', path)
                try:
                    # print('current working directory:', os.getcwd())
                    # print('import', path)
                    file = open(os.path.join(self.work_dir, path), 'r')
                    self.identify_file(file)
                    file.close()
                except:
                    pass
            case 'fn':
                if len(tokens) < 2:
                    return
                self.funct_list.append(
                    tokens[1]) if tokens[1] not in self.funct_list else None
                for e in tokens[3:tokens.index(')') if ')' in tokens else None]:
                    self.var_list.append(
                        e) if e not in self.var_list else None
            case 'class':
                if len(tokens) < 2:
                    return
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
