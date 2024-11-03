class Interpretador:
    def __init__(self, arvore_sintatica, tabela_de_simbolos):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_de_simbolos = tabela_de_simbolos

    def executar(self):
        for no in self.arvore_sintatica:
            if no[0] == 'atribuir':
                nome_variavel = no[1]
                expr = self.avaliar(no[2])
                self.tabela_de_simbolos.adicionar_simbolo(nome_variavel, expr)
                print(f"{nome_variavel} = {expr}")

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
