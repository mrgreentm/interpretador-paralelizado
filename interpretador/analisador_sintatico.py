class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.arvore_sintatica = []

    def analisar(self):
        while self.pos < len(self.tokens):
            instrucao = self.instrucao()
            if instrucao:
                self.arvore_sintatica.append(instrucao)  # Adicionando diretamente ao final da árvore sintática
        return self.arvore_sintatica

    def instrucao(self):
        if self.pos >= len(self.tokens):
            return None

        token_tipo, token_valor = self.tokens[self.pos]

        if token_tipo == 'ID':  # Atribuição ou chamada de função/método
            return self.atribuicao_ou_chamada()
        elif token_tipo == 'IF':  # Condicional
            return self.condicional()
        elif token_tipo == 'WHILE':  # Laço while
            return self.laco_while()
        elif token_tipo == 'FOR':  # Laço for
            return self.laco_for()
        elif token_tipo == 'DEF':  # Definição de função
            return self.definicao_funcao()
        elif token_tipo == 'RETURN':  # Instrução de retorno
            return self.instrucao_return()
        elif token_tipo == 'PRINT':  # Instrução de impressão
            return self.instrucao_print()
        else:
            # Se o token não corresponder a nenhum dos casos acima, retornamos uma mensagem de erro
            raise SyntaxError(f"Instrução inválida: {token_valor}")

    def instrucao_print(self):
        self.pos += 1  # Avança o token 'PRINT'
        if self.tokens[self.pos][0] == 'PARENTESES_ESQ':
            self.pos += 1  # Consome o '('
            expr = self.expressao()  # Avalia a expressão dentro de 'print'
            if self.tokens[self.pos][0] == 'PARENTESES_DIR':
                self.pos += 1  # Consome o ')'
                return ('print', expr)
            else:
                raise SyntaxError("Esperado ')' após expressão em 'print'")
        else:
            raise SyntaxError("Esperado '(' após 'print'")

    def atribuicao_ou_chamada(self):
        nome_variavel = self.tokens[self.pos][1]
        self.pos += 1

        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ATRIBUIR':
            self.pos += 1
            expr = self.expressao()
            return ('atribuir', nome_variavel, expr)

        elif self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'PARENTESES_ESQ':
            # Chamada de função
            self.pos += 1
            args = self.lista_argumentos()
            if self.tokens[self.pos][0] == 'PARENTESES_DIR':
                self.pos += 1
                return ('chamada_funcao', nome_variavel, args)
            else:
                raise SyntaxError("Esperado ')' após os argumentos da função")

        elif self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'PONTO':
            # Chamada de método
            self.pos += 1
            metodo = self.tokens[self.pos][1]  # Nome do método (ex: append)
            self.pos += 1
            if self.tokens[self.pos][0] == 'PARENTESES_ESQ':
                self.pos += 1
                args = self.lista_argumentos()
                if self.tokens[self.pos][0] == 'PARENTESES_DIR':
                    self.pos += 1
                    return ('chamada_metodo', nome_variavel, metodo, args)
                else:
                    raise SyntaxError("Esperado ')' após os argumentos do método")
            else:
                raise SyntaxError("Esperado '(' após o nome do método")
        else:
            raise SyntaxError("Esperado '=' ou '(' após o identificador")

    def condicional(self):
        self.pos += 1
        condicao = self.expressao()
        if self.tokens[self.pos][0] == 'CHAVE_ESQ':
            self.pos += 1
            bloco_if = self.bloco()
            bloco_else = None
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ELSE':
                self.pos += 1
                if self.tokens[self.pos][0] == 'CHAVE_ESQ':
                    self.pos += 1
                    bloco_else = self.bloco()
                else:
                    raise SyntaxError("Esperado '{' após 'else'")
            return ('if', condicao, bloco_if, bloco_else)
        else:
            raise SyntaxError("Esperado '{' após condição 'if'")

    def laco_while(self):
        self.pos += 1
        condicao = self.expressao()
        if self.tokens[self.pos][0] == 'CHAVE_ESQ':
            self.pos += 1
            bloco = self.bloco()
            return ('while', condicao, bloco)
        else:
            raise SyntaxError("Esperado '{' após condição 'while'")

    def laco_for(self):
        # Avança o token 'FOR'
        self.pos += 1
        variavel = self.tokens[self.pos][1]  # Nome da variável de loop
        self.pos += 1

        # Verifica se o token seguinte é 'IN'
        if self.tokens[self.pos][0] == 'IN':
            self.pos += 1
            inicio = self.expressao()  # Expressão de início do laço

            # Verifica se o token seguinte é 'TO'
            if self.tokens[self.pos][0] == 'TO':
                self.pos += 1
                fim = self.expressao()  # Expressão de fim do laço

                # Verifica se há uma chave de abertura '{' para o bloco do laço
                if self.tokens[self.pos][0] == 'CHAVE_ESQ':
                    self.pos += 1
                    bloco = self.bloco()  # Bloco de instruções dentro do laço
                    return ('for', variavel, inicio, fim, bloco)
                else:
                    raise SyntaxError("Esperado '{' após 'for'")
            else:
                raise SyntaxError("Esperado 'to' após a expressão de início no laço 'for'")
        else:
            raise SyntaxError("Esperado 'in' após o identificador no laço 'for'")

    def definicao_funcao(self):
        self.pos += 1
        nome_funcao = self.tokens[self.pos][1]  # Nome da função
        self.pos += 1
        if self.tokens[self.pos][0] == 'PARENTESES_ESQ':  # Parênteses para parâmetros
            self.pos += 1
            parametros = self.lista_argumentos()
            if self.tokens[self.pos][0] == 'PARENTESES_DIR':
                self.pos += 1
                if self.tokens[self.pos][0] == 'CHAVE_ESQ':
                    self.pos += 1
                    corpo = self.bloco()
                    return ('def_funcao', nome_funcao, parametros, corpo)
                else:
                    raise SyntaxError("Esperado '{' após declaração de função")
            else:
                raise SyntaxError("Esperado ')' após parâmetros da função")
        else:
            raise SyntaxError("Esperado '(' após nome da função")


    def instrucao_return(self):
        self.pos += 1  # Avança para o token após o 'RETURN'
        expr = self.expressao()  # Expressão para o retorno, se houver
        return ('return', expr)

    def lista_argumentos(self):
        args = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'PARENTESES_DIR':
            args.append(self.expressao())
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'VIRGULA':
                self.pos += 1
        return args

    def bloco(self):
        bloco = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'CHAVE_DIR':
            instrucao = self.instrucao()
            if instrucao:
                bloco.append(instrucao)  # Adicionando ao bloco, sem usar append diretamente no loop
        self.pos += 1  # Consome o 'CHAVE_DIR'
        return bloco

    def expressao(self):
        termo = self.termo()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('OPERADOR_ARIT', 'OPERADOR_REL', 'OPERADOR_LOG'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            prox_termo = self.termo()
            termo = (op, termo, prox_termo)
        return termo

    def termo(self):
        token_tipo, token_valor = self.tokens[self.pos]
        if token_tipo == 'NUMERO':
            self.pos += 1
            return token_valor
        elif token_tipo == 'ID':
            self.pos += 1
            return token_valor
        elif token_tipo == 'PARENTESES_ESQ':
            self.pos += 1
            expr = self.expressao()
            if self.tokens[self.pos][0] == 'PARENTESES_DIR':
                self.pos += 1
                return expr
            else:
                raise SyntaxError("Esperado ')' após expressão")
        else:
            raise SyntaxError(f"Expressão inválida: {token_valor}")
