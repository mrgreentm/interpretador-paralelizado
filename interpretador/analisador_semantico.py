class AnalisadorSemantico:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_de_simbolos = {}

    def analisar(self):
        for no in self.arvore_sintatica:
            if no[0] == 'atribuir':
                nome_variavel = no[1]
                expr = no[2]
                # Armazena o nome da variável na tabela de símbolos
                self.tabela_de_simbolos[nome_variavel] = expr
            else:
                raise ValueError(f"Tipo de declaração desconhecida: {no}")
