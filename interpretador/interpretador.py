class Interpretador:
    def __init__(self, arvore_sintatica, tabela_de_simbolos):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_de_simbolos = tabela_de_simbolos
        self.funcoes = {}

    def executar(self):
        for no in self.arvore_sintatica:
            if no[0] == 'atribuir':
                nome_variavel = no[1]
                expr = self.avaliar(no[2])
                self.tabela_de_simbolos.adicionar_simbolo(nome_variavel, expr)
            elif no[0] == 'if':
                condicao = self.avaliar(no[1])
                if condicao:
                    self.executar_bloco(no[2])
                elif len(no) > 3:  # else bloco
                    self.executar_bloco(no[3])
            elif no[0] == 'while':
                while self.avaliar(no[1]):
                    self.executar_bloco(no[2])
            elif no[0] == 'for':
                variavel = no[1]
                inicio = self.avaliar(no[2])
                fim = self.avaliar(no[3])
                for i in range(inicio, fim):
                    self.tabela_de_simbolos.adicionar_simbolo(variavel, i)
                    self.executar_bloco(no[4])
            elif no[0] == 'def_funcao':
                nome_funcao = no[1]
                parametros = no[2]
                corpo = no[3]
                self.funcoes[nome_funcao] = (parametros, corpo)
            elif no[0] == 'chamada_funcao':
                nome_funcao = no[1]
                argumentos = [self.avaliar(arg) for arg in no[2]]
                self.executar_funcao(nome_funcao, argumentos)

    def executar_bloco(self, bloco):
        for instrucao in bloco:
            self.executar_instrucao(instrucao)

    def executar_instrucao(self, instrucao):
        if instrucao[0] == 'atribuir':
            nome_variavel = instrucao[1]
            expr = self.avaliar(instrucao[2])
            self.tabela_de_simbolos.adicionar_simbolo(nome_variavel, expr)
        elif instrucao[0] == 'chamada_funcao':
            nome_funcao = instrucao[1]
            argumentos = [self.avaliar(arg) for arg in instrucao[2]]
            self.executar_funcao(nome_funcao, argumentos)
        elif instrucao[0] == 'print':
            valor = self.avaliar(instrucao[1])
            print(valor)

    def avaliar(self, expr):
        if isinstance(expr, tuple):
            op, esquerda, direita = expr
            esquerda = self.obter_valor(esquerda)
            direita = self.obter_valor(direita)
            if op == '+':
                return esquerda + direita
            elif op == '-':
                return esquerda - direita
            elif op == '*':
                return esquerda * direita
            elif op == '/':
                return esquerda / direita
            elif op == '==':
                return esquerda == direita
            elif op == '!=':
                return esquerda != direita
            elif op == '<':
                return esquerda < direita
            elif op == '>':
                return esquerda > direita
            elif op == '<=':
                return esquerda <= direita
            elif op == '>=':
                return esquerda >= direita
            elif op == 'and':
                return esquerda and direita
            elif op == 'or':
                return esquerda or direita
        else:
            return self.obter_valor(expr)

    def obter_valor(self, termo):
        if isinstance(termo, int):
            return termo
        elif isinstance(termo, str):
            valor = self.tabela_de_simbolos.obter_simbolo(termo)
            if valor is None:
                raise ValueError(f"Variável '{termo}' não definida")
            return valor

    def executar_funcao(self, nome_funcao, argumentos):
        if nome_funcao not in self.funcoes:
            raise ValueError(f"Função '{nome_funcao}' não definida")

        parametros, corpo = self.funcoes[nome_funcao]
        if len(parametros) != len(argumentos):
            raise ValueError(f"Argumentos incorretos para a função '{nome_funcao}'")

        # Cria um novo contexto para os parâmetros da função
        contexto = dict(zip(parametros, argumentos))
        self.tabela_de_simbolos.adicionar_contexto(contexto)

        # Executa o corpo da função
        self.executar_bloco(corpo)

        # Remove o contexto da função após a execução
        self.tabela_de_simbolos.remover_contexto()
