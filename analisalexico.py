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
              "end", "if", "then", "else", "while", "do", "not", "input", "output"]
    inteiros = []  # type: List(str)
    delimitadores = [",", ".", ";", ":", "(", ")","[","]"]
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

    def novaPalavra(self):
        # global palavra, logFinal, linhaCont
        if self.palavra is not "":
            self.palavra = self.palavra.lower()
            if self.palavra[0].isalpha():
                if self.palavra.isalpha() and self.palavra in self.chaves:
                    self.novo = log(self.palavra, "Chave", self.linhaCont)
                    self.logFinal.append(self.novo)
                else:
                    self.novo = log(self.palavra, "Identificador", self.linhaCont)
                    self.logFinal.append(self.novo)
            else:
                for self.i in self.palavra:
                    if self.i.isalpha():
                        print("CRITICAL ERROR! >> Linha", self.linhaCont)
                        exit()
                if '.' in self.palavra:
                    self.novo = log(self.palavra, "Real", self.linhaCont)
                    self.logFinal.append(self.novo)
                else:
                    self.novo = log(self.palavra, "Inteiro", self.linhaCont)
                    self.logFinal.append(self.novo)
            self.palavra = ""

    def getAnalise(self):
        for self.caract in iter(lambda: self.arquivo.read(1), ''):
            if self.caract is '{':
                while self.caract is not '}':
                    self.caract = self.arquivo.read(1)
                    self.ultimoLido = self.caract
            elif self.caract.isalpha():
                self.palavra += self.caract
            else:
                if self.caract in self.inteiros:
                    self.palavra += self.caract
                elif self.caract in self.aditivos:
                    self.novaPalavra()
                    self.novo = log(self.caract, "Aditivo", self.linhaCont)
                    self.logFinal.append(self.novo)
                elif self.caract in self.multiplicativos:
                    self.novaPalavra()
                    self.novo = log(self.caract, "Multiplicativo", self.linhaCont)
                    self.logFinal.append(self.novo)
                elif self.caract in self.delimitadores:
                    if self.caract is '.' and self.ultimoLido in self.inteiros:
                        self.palavra += self.caract
                    elif self.caract is ':':
                        self.palavra += self.caract
                    else:
                        self.novaPalavra()
                        self.novo = log(self.caract, "Delimitador", self.linhaCont)
                        self.logFinal.append(self.novo)
                elif self.caract in self.relacionais:
                    if self.ultimoLido in self.relacionais:
                        self.palavra += self.caract
                        self.novo = log(self.palavra, "Relacional", self.linhaCont)
                        self.logFinal.append(self.novo)
                        self.limparPalavra()
                    elif self.ultimoLido is ':':
                        self.palavra += self.caract
                        self.novo = log(self.palavra, "Atribuição", self.linhaCont)
                        self.logFinal.append(self.novo)
                        self.limparPalavra()
                    else:
                        self.novaPalavra()
                        self.novo = log(self.caract, "Relacional", self.linhaCont)
                        self.logFinal.append(self.novo)
                elif self.caract in [' ', '	']:
                    self.novaPalavra()
                elif self.caract is '\n':
                    self.novaPalavra()
                    self.linhaCont += 1
                else:
                    print("ERRO! CARACTER INVALIDO \"", self.caract, "\"  > Linha", self.linhaCont)
                    exit();
            self.ultimoLido = self.caract
        self.novaPalavra()
        print("|Token        | Classificação    | Linha")
        print("|-------------|------------------|------")
        for l in self.logFinal:
            print("|", l.token, "-" * (10 - len(l.token)), "|", l.classif, "-" * (15 - len(l.classif)), "|",
                  l.linha)

        print("Sucess")
        return self.logFinal
