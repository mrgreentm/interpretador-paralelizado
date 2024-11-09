class AnalisadorSemantico:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_de_simbolos = {}

    def analisar(self):
        for no in self.arvore_sintatica:
            if no[0] == 'atribuir':
                nome_variavel = no[1]
                expr = no[2]
                self.tabela_de_simbolos[nome_variavel] = expr
            elif no[0] == 'for':
                nome_variavel = no[1]
                inicio = no[2]
                fim = no[3]
                # Lógica para tratar o laço 'for' (se necessário)
                # Aqui podemos fazer verificações como garantir que as variáveis de controle estão corretas
                self.tabela_de_simbolos[nome_variavel] = (inicio, fim)  # Exemplo de como armazenar a info do laço
            else:
                raise ValueError(f"Tipo de declaração desconhecida: {no}")
