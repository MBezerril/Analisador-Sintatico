import lexico2

class simbolo:
    simbolo = ''
    tipo = ''

    def __init__(self, simb, tip):
        self.simbolo = simb
        self.tipo = tip


class pilhaSemantica:
    dados = []  # type: List(simbolo)
    begin = 0

    def inicioEscopo(self):
        self.begin += 1
        #print(self.begin)

    def fimEscopo(self):
        if self.begin > 0:
            self.begin -= 1
            #print(self.begin)
        else:
            self.limparEscopo()
            #print("-$")

    def adicionarSimbolo(self, simb):
        if simb.simbolo != '$':
            if self.pesquisaSimboloEscopo(simb.simbolo) != None:
                print("Multiplas variaveis com o mesmo identificador no mesmo escopo")
                exit(-1)
        if simb.tipo == "integer":
            simb.tipo = "Inteiro"
        #print(simb.simbolo, simb.tipo)
        self.dados.append(simb)

    def pesquisaSimbolo(self, simb):
        for x in reversed(self.dados):
            if x.simbolo == simb:
                return x
        return None

    def pesquisaSimboloEscopo(self, simb):
        for x in reversed(self.dados):
            if x.simbolo == '$':
                return None
            if x.simbolo == simb:
                return x
        return None

    def limparEscopo(self):
        x = simbolo('', '')
        while x.simbolo != '$':
            x = self.dados.pop()


class pilhaTipos:
    receptor = ''
    argumento = ''

    def inicializar(self, tipo):
        if self.receptor != '':
            if self.argumento == '':
                self.receptor = ''
                self.argumento = ''
                self.operacao = False
        self.receptor = tipo
        print(self.receptor, ":=")

    def operacao(self):
        self.operacao = True

    def adicionarTipo(self, tipo):
        if tipo == "integer":
            tipo = "Inteiro"
        if tipo == "real":
            tipo = "Real"
        if self.argumento != '':
            if tipo != self.argumento:
                self.argumento = "Real"
        else:
            self.argumento = tipo
        print(self.argumento)

    def finalizar(self):
        print(self.receptor, ":= ", self.argumento)
        print("----------------------")
        if self.receptor != '':
            if self.argumento == '':
                self.receptor = ''
                self.argumento = ''
                return True
            if self.receptor == "Inteiro" and self.argumento == "Real":
                return False
            self.receptor = ''
            self.argumento = ''
            return True
        else:
            self.receptor = ''
            self.argumento = ''
            return True



class AnalisadorSintatico:
    logFinal = []  # type: List(lexico2.log)
    pos = 0
    tipos = ["integer", "real", "boolean"]
    pilha = pilhaSemantica()
    tiposVariaveis = pilhaTipos()
    x = 0

    def __init__(self, log):
        self.logFinal = log

    def proximo(self):
        self.pos += 1

    def programa(self):
        if len(self.logFinal) > 0:
            if self.logFinal[self.pos].token != 'program':
                print("FALTA PROGRAM|linha: ", self.logFinal[self.pos].linha)
                return False
            self.pilha.adicionarSimbolo(simbolo('$', '$'))
            self.proximo()
            if self.logFinal[self.pos].classif != "Identificador":
                print("FALTA IDENTIFICADOR DO PROGRAMA |linha: ", self.logFinal[self.pos].linha)
                return False
            self.proximo()
            if self.logFinal[self.pos].token != ";":
                print("FALTA ; NA DECLARAÇÃO DO PROGRAMA |linha: ", self.logFinal[self.pos].linha)
                return False
            self.proximo()
            if self.logFinal[self.pos].token == "var":
                self.proximo()
                if not self.variaveis():
                    print("ERRO NA DECLARACAO DAS VARIÁVEIS |linha: ", self.logFinal[self.pos].linha)
                    return False
            if self.logFinal[self.pos].token == "procedure":
                if not self.subprograma():
                    print("ERRO NA DECLARACAO DE SUBPROGRAMA |linha: ", self.logFinal[self.pos].linha)
                    return False

            if self.logFinal[self.pos].token == "begin":
                self.pilha.inicioEscopo()
                self.proximo()
                if not self.comandoComposto():
                    print("ERRO NA DECLARACAO DE COMMANDO COMPOSTO |linha: ", self.logFinal[self.pos].linha)
                    return False
            self.pilha.fimEscopo()
            if self.logFinal[self.pos].token != ".":
                print("AUSENCIA DO . PARA FIM DO PROGRAMA |linha: ", self.logFinal[self.pos].linha)
                return False
        return True

    def variaveis(self):

        while self.logFinal[self.pos].classif == "Identificador":
            listaDeVariaveis = []
            listaDeVariaveis.append(self.logFinal[self.pos].token)
            self.proximo()
            while self.logFinal[self.pos].token != ":":
                if self.logFinal[self.pos].token != ",":
                    print("FALTA , DEPOIS DE UM ID |linha: ", self.logFinal[self.pos].linha)
                    return False
                self.proximo()
                if self.logFinal[self.pos].classif != "Identificador":
                    print("FALTA ID DEPOIS DE UMA , |linha: ", self.logFinal[self.pos].linha)
                    return False
                listaDeVariaveis.append(self.logFinal[self.pos].token)
                self.proximo()
            if self.logFinal[self.pos].token != ':':
                print("ERRO! ESPERADO UM :|linha: ", self.logFinal[self.pos].linha)
                return False
            self.proximo()
            if self.logFinal[self.pos].token not in self.tipos:
                print("TIPO DE VARIAVEL ESPERADO|linha: ", self.logFinal[self.pos].linha)
                return False
            tipoVariaveis = ''
            if self.logFinal[self.pos].token == "integer":
                tipoVariaveis = "Inteiro"
            if self.logFinal[self.pos].token == "real":
                tipoVariaveis = "Real"
            for x in listaDeVariaveis:
                self.pilha.adicionarSimbolo(simbolo(x, tipoVariaveis))
            self.proximo()
            if self.logFinal[self.pos].token != ";":
                print("ERRO! ESPERADO UM ;|linha: ", self.logFinal[self.pos].linha)
                return False
            self.proximo()
        return True

    def argumentos(self):
        if self.logFinal[self.pos].token != "(":
            return True
        self.proximo()
        while self.logFinal[self.pos].token == "var" or self.logFinal[self.pos].classif == "Identificador":
            listaDeVariaveis = []
            if self.logFinal[self.pos].token == "var":
                self.proximo()
            if self.logFinal[self.pos].classif != "Identificador":
                print("FALTA ID DE ARGUMENTO |linha: ", self.logFinal[self.pos].linha)
                return False
            listaDeVariaveis.append(self.logFinal[self.pos].token)
            self.proximo()
            while self.logFinal[self.pos].token != ":":
                if self.logFinal[self.pos].token != ",":
                    print("FALTA , DEPOIS DE UM ID |linha: ", self.logFinal[self.pos].linha)
                    return False
                self.proximo()
                if self.logFinal[self.pos].classif != "Identificador":
                    print("FALTA ID DEPOIS DE UMA , |linha: ", self.logFinal[self.pos].linha)
                    return False
                listaDeVariaveis.append(self.logFinal[self.pos].token)
                self.proximo()
            if self.logFinal[self.pos].token != ':':
                print("ERRO! ESPERADO UM :|linha: ", self.logFinal[self.pos].linha)
                return False
            self.proximo()
            if self.logFinal[self.pos].token not in self.tipos:
                print("TIPO DE VARIAVEL ESPERADO|linha: ", self.logFinal[self.pos].linha)
                return False
            for x in listaDeVariaveis:
                self.pilha.adicionarSimbolo(simbolo(x, self.logFinal[self.pos].token))
            self.proximo()
            if self.logFinal[self.pos].token != ";":
                if self.logFinal[self.pos].token != ")":
                    print("ERRO! ESPERADO UM ; OU ) |linha: ", self.logFinal[self.pos].linha)
                    return False
            else:
                self.proximo()
        if self.logFinal[self.pos].token != ")":
            print("ERRO! ESPERADO UM ) |linha:", self.logFinal[self.pos].linha)
            return False
        self.proximo()
        if self.logFinal[self.pos].token != ";":
            print("ERRO! ESPERADO UM ; |linha: ", self.logFinal[self.pos].linha)
            return False
        self.proximo()
        return True

    def comandos_opcionais(self):
        if not self.logFinal[self.pos].token == 'end':
            self.lista_de_comandos1()
        self.pilha.fimEscopo()

    def lista_de_comandos1(self):
        if self.comando():
            return self.lista_de_comandos2()
        else:
            return False

    def lista_de_comandos2(self):
        if self.logFinal[self.pos].token != ';':
            return True
        else:
            if not self.tiposVariaveis.finalizar():
                print("Conversão inválida de Real para Integer | Linha:", self.logFinal[self.pos].linha)
                exit(-3)
            self.proximo()
            if self.comando():
                return self.lista_de_comandos2()

    def parte_else(self):
        if self.logFinal[self.pos].token != "else":
            return True
        else:
            self.proximo()
            return self.comando()

    def comando(self):
        if self.logFinal[self.pos].classif == "Identificador":
            if self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token) is None:
                print("Variável não declarada:", self.logFinal[self.pos].token)
                exit(-2)
            if self.logFinal[self.pos + 1].token == ':=':
                self.tiposVariaveis.inicializar(self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token).tipo)
                self.proximo()
                self.proximo()
                return self.expressao()
            elif self.logFinal[self.pos + 1].token == '(':
                self.proximo()
                self.proximo()
                if not self.lista_de_expressoes1():
                    return False
                if self.logFinal[self.pos].token == ')':
                    self.proximo()
                    return True
            else:
                self.tiposVariaveis.adicionarTipo(self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token).tipo)
                self.proximo()
                return True
        elif self.logFinal[self.pos].token == "begin":
            if not self.tiposVariaveis.finalizar():
                print("Conversão inválida de Real para Integer | Linha:", self.logFinal[self.pos].linha)
                exit(-3)
            self.pilha.inicioEscopo()
            self.proximo()
            return self.comandoComposto()
        elif self.logFinal[self.pos].token == "if":
            self.proximo()
            if not self.expressao():
                return False
            if self.logFinal[self.pos].token != "then":
                return False
            self.proximo()
            if not self.comando():
                return False
            return self.parte_else()
        elif self.logFinal[self.pos].token == "while":
            self.proximo()
            if not self.expressao():
                return False
            if self.logFinal[self.pos].token != "do":
                return False
            self.proximo()
            if not self.comando():
                return False
            return True
        else:
            return False

    def lista_de_expressoes1(self):
        if self.expressao():
            return self.lista_de_expressoes2()
        else:
            return False

    def lista_de_expressoes2(self):
        if self.logFinal[self.pos].token == ',':
            self.proximo()
            if not self.expressao():
                return False
            return self.lista_de_expressoes2()
        else:
            return True

    def expressao(self):
        if self.expressao_simples1():
            if self.op_relacional():
                if not self.expressao_simples1():
                    print("ERRO DE EXPRESSAO", self.logFinal[self.pos].linha)
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def expressao_simples1(self):
        if self.termo1():
            return self.expressao_simples2()
        elif self.sinal():
            if self.termo1():
                return self.expressao_simples2()
            else:
                return False

    def expressao_simples2(self):
        if self.op_aditivo():
            if not self.termo1():
                return False
            else:
                return self.expressao_simples2()
        else:
            return True

    def termo1(self):
        if self.fator():
            return self.termo2()
        else:
            return False

    def termo2(self):
        if not self.op_multiplicativo():
            return True
        else:
            if not self.fator():
                return False
            if not self.termo2():
                return False
            return True

    def fator(self):
        if self.logFinal[self.pos].classif == "Identificador":
            if self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token) == None:
                print("Variável não declarada:", self.logFinal[self.pos].token)
                exit(-2)
            self.tiposVariaveis.adicionarTipo(self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token).tipo)
            self.proximo()
            if self.logFinal[self.pos].token == '(':
                self.proximo()
                if not self.lista_de_expressoes1():
                    return False
                self.proximo()
                if not self.logFinal[self.pos].token == ')':
                    return False
                return True
            else:
                return True
        elif self.logFinal[self.pos].token == '(':
            self.proximo()
            if not self.expressao():
                return False
            if self.logFinal[self.pos].token == ')':
                self.proximo()
            else:
                return False
            return True
        elif self.logFinal[self.pos].classif in ["Real", "Inteiro"]:
            self.tiposVariaveis.adicionarTipo(self.logFinal[self.pos].classif)
            self.proximo()
            return True
        elif self.logFinal[self.pos].classif == "Chave":
            if self.logFinal[self.pos].token in ["true", "false"]:
                self.proximo()
                return True
            elif self.logFinal[self.pos].token == "not":
                self.proximo()
                return self.fator()

    def sinal(self):
        if self.logFinal[self.pos] in ['+', '-']:
            self.proximo()
            return True
        else:
            return False

    def op_relacional(self):
        if self.logFinal[self.pos].token in ["=", "<", ">", "<=", ">=", "<>"]:
            self.proximo()
            return True
        else:
            return False

    def op_aditivo(self):
        if self.logFinal[self.pos].token in ["+", "-", "or"]:
            self.proximo()
            return True
        else:
            return False

    def op_multiplicativo(self):
        if self.logFinal[self.pos].token in ["*", "/", "and"]:
            self.proximo()
            return True
        else:
            return False

    def comandoComposto(self):
        if self.logFinal[self.pos].token == "end":
            self.pilha.fimEscopo()
            self.proximo()
            return True
        else:
            if not self.lista_de_comandos1():
                return False
            else:
                if self.logFinal[self.pos].token != "end":
                    print("AUSENCIA DO END |linha: ", self.logFinal[self.pos].linha)
                    return False
                else:
                    if not self.tiposVariaveis.finalizar():
                        print("Conversão inválida de Real para Integer | Linha:", self.logFinal[self.pos].linha )
                        exit(-3)
                    self.pilha.fimEscopo()
                    self.proximo()
                    return True

    def subprograma(self):
        while self.logFinal[self.pos].token == "procedure":
            self.proximo()
            if self.logFinal[self.pos].classif != "Identificador":
                print("FALTA ID DEPOIS DE UMA , |linha:", self.logFinal[self.pos].linha)
                return False
            if self.pilha.pesquisaSimbolo(self.logFinal[self.pos].token) != None:
                print("Multiplas funções com o mesmo nome:", self.logFinal[self.pos].token)
                exit(-2)
            self.pilha.adicionarSimbolo(simbolo(self.logFinal[self.pos].token, "Procedure"))
            self.pilha.adicionarSimbolo(simbolo('$', '$'))
            self.proximo()
            if not self.argumentos():
                print("ERRO NA DECLARACAO DE ARGUMENTOS DE SUBPROGRAMA |linha: ", self.logFinal[self.pos].linha)
                return False
            if self.logFinal[self.pos].token == "var":
                self.proximo()
                if not self.variaveis():
                    print("ERRO NA DECLARACAO DAS VARIÁVEIS DE SUBPROGRAMA |linha: ", self.logFinal[self.pos].linha)
                    return False
            if self.logFinal[self.pos].token == "procedure":
                self.pilha.adicionarSimbolo(simbolo(self.logFinal[self.pos].token, "Procedure"))
                self.pilha.adicionarSimbolo(simbolo('$', '$'))
                if not self.subprograma():
                    print("ERRO NA DECLARACAO DE SUBPROGRAMA DE SUBPROGRAMA |linha: ", self.logFinal[self.pos].linha)
                    return False
            if self.logFinal[self.pos].token == "begin":
                self.pilha.inicioEscopo()
                self.proximo()
                if not self.comandoComposto():
                    print("ERRO NA DECLARACAO DE COMMANDO COMPOSTO |linha: ", self.logFinal[self.pos].linha)
                    return False
            if self.logFinal[self.pos].token != ";":
                print("ERRO! ESPERADO UM ;|linha:", self.logFinal[self.pos].linha)
                return False
            self.proximo()
        self.pilha.fimEscopo()
        return True

"""EXECUÇÃO TOTAL!"""

# lido = input('Enter input:')
lexico = lexico2.AnalisadorLexico("bubble.txt")
log = lexico.getAnalise()
sintatico = AnalisadorSintatico(log)
print(sintatico.programa())
