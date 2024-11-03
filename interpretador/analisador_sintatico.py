class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.arvore_sintatica = []

    def analisar(self):
        while self.pos < len(self.tokens):
            instrucao = self.instrucao()
            if instrucao:
                self.arvore_sintatica.append(instrucao)
        return self.arvore_sintatica

    def instrucao(self):
        # Simplificado para atribuição `id = expr`
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ID':
            nome_variavel = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'ATRIBUIR':
                self.pos += 1
                expr = self.expressao()
                if self.tokens[self.pos][0] == 'FIM':
                    self.pos += 1
                    return ('atribuir', nome_variavel, expr)
            else:
                raise SyntaxError("Esperado '=' após o identificador")
        return None

    def expressao(self):
        # Suporta operadores binários básicos
        termo = self.tokens[self.pos][1]
        self.pos += 1
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OPERADOR':
            op = self.tokens[self.pos][1]
            self.pos += 1
            prox_termo = self.tokens[self.pos][1]
            self.pos += 1
            return (op, termo, prox_termo)
        return termo
