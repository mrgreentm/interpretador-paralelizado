class TabelaDeSimbolos:
    def __init__(self):
        self.simbolos = {}

    def adicionar_simbolo(self, nome, valor):
        self.simbolos[nome] = valor

    def obter_simbolo(self, nome):
        return self.simbolos.get(nome, None)
