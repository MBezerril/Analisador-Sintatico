class log:
    token = ""
    classif = ""
    linha = ""

    def __init__(self, tk, cl, n):
        self.token = tk
        self.classif = cl
        self.linha = n


class AnalisadorLexico:
    aditivos = ['+', '-']
    multiplicativos = ['/', '*']
    chaves = ["program", "var", "integer", "real", "boolean", "procedure", "begin",
              "end", "if", "then", "else", "while", "do", "not", "true", "false"]
    inteiros = []  # type: List(str)
    delimitadores = [",", ".", ";", ":", "(", ")", "[", "]"]
    relacionais = ["=", "<", ">", "<=", ">=", "<>"]
    palavra = ""
    linhaCont = 1
    logFinal = []  # type: List(log)
    ultimoLido = ''

    def __init__(self, nomeArquivo):
        for x in range(0, 10):
            self.inteiros.append(str(x))
        self.arquivo = open(nomeArquivo, "r")

    def limparPalavra(self):
        self.palavra = ""

    def SeparaClassifica(self):
        #print("PALAVRA:", self.palavra)
        if self.palavra is not "":
            self.palavra = self.palavra.lower()
            inicio = 0
            classificacao = ""
            substring = ""
        #--------------------------
            while inicio < len(self.palavra):
                if self.palavra[inicio].isalpha():
                    #comeca com letra, ou é identificador ou chave
                    for i in range(inicio, len(self.palavra)):
                        if self.palavra[i].isalpha() or self.palavra[i] in self.inteiros:
                            substring += self.palavra[i]
                        else:
                            inicio=i
                            if substring in self.chaves:
                                novo = log(substring, "Chave", self.linhaCont)
                                self.logFinal.append(novo)
                            else:
                                novo = log(substring, "Identificador", self.linhaCont)
                                self.logFinal.append(novo)
                            break
                        if i == len(self.palavra)-1:
                            if substring in self.chaves:
                                novo = log(substring, "Chave", self.linhaCont)
                                self.logFinal.append(novo)
                            else:
                                novo = log(substring, "Identificador", self.linhaCont)
                                self.logFinal.append(novo)
                            inicio=i+1
                            break
                elif self.palavra[inicio] in self.delimitadores:
                    substring += self.palavra[inicio]
                    if inicio < len(self.palavra) - 1:
                        if self.palavra[inicio] is ":" and self.palavra[inicio + 1] is "=":
                            substring += self.palavra[inicio + 1]
                            inicio += 2
                            novo = log(substring, "Atribuição", self.linhaCont)
                            self.logFinal.append(novo)
                        else:
                            inicio += 1
                            novo = log(substring, "Delimitador", self.linhaCont)
                            self.logFinal.append(novo)
                    else:
                        inicio += 1
                        novo = log(substring, "Delimitador", self.linhaCont)
                        self.logFinal.append(novo)
                elif self.palavra[inicio] in self.relacionais:
                    substring += self.palavra[inicio]
                    if inicio<len(self.palavra)-1 and self.palavra[inicio+1] in self.relacionais:
                        substring += self.palavra[inicio + 1]
                        inicio += 1
                    inicio += 1
                    novo = log(substring, "Relacional", self.linhaCont)
                    self.logFinal.append(novo)
                elif self.palavra[inicio] in self.inteiros:
                    for i in range(inicio, len(self.palavra)):
                        if self.palavra[i] in self.inteiros or self.palavra[i] is ".":
                            substring += self.palavra[i]
                        else:
                            inicio = i
                            if '.' in substring:
                                novo = log(substring, "Real", self.linhaCont)
                                self.logFinal.append(novo)
                            else:
                                novo = log(substring, "Inteiro", self.linhaCont)
                                self.logFinal.append(novo)
                            break
                        if i == len(self.palavra) - 1:
                            if '.' in substring:
                                novo = log(substring, "Real", self.linhaCont)
                                self.logFinal.append(novo)
                            else:
                                novo = log(substring, "Inteiro", self.linhaCont)
                                self.logFinal.append(novo)
                            inicio = i + 1
                            break
                elif self.palavra[inicio] in self.multiplicativos:
                    substring += self.palavra[inicio]
                    inicio += 1
                    novo = log(substring, "Multiplicativo", self.linhaCont)
                    self.logFinal.append(novo)
                elif self.palavra[inicio] in self.aditivos:
                    substring += self.palavra[inicio]
                    inicio += 1
                    novo = log(substring, "Aditivo", self.linhaCont)
                    self.logFinal.append(novo)
                else:
                    exit(-11)
                substring = ""
        #--------------------------
        self.limparPalavra()


    def getAnalise(self):
        for self.caract in iter(lambda: self.arquivo.read(1), ''):
            if self.caract is '{':
                while self.caract is not '}':
                    self.caract = self.arquivo.read(1)
                    self.ultimoLido = self.caract
            elif self.caract is ' ' or self.caract is '\t':
                self.SeparaClassifica()
            elif self.caract is '\n':
                self.SeparaClassifica()
                self.linhaCont += 1
            else:
                self.palavra += self.caract
        print("|Token        | Classificação    | Linha")
        print("|-------------|------------------|------")
        for l in self.logFinal:
            print("|", l.token, "-" * (10 - len(l.token)), "|", l.classif, "-" * (15 - len(l.classif)), "|",
                  l.linha)
        return self.logFinal
