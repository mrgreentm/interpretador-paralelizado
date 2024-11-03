import re

class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens = []

    def analisar(self):
        especificacao_tokens = [
            ('NUMERO', r'\d+'),            # Números
            ('ATRIBUIR', r'='),            # Atribuição
            ('FIM', r';'),                 # Fim de linha
            ('ID', r'[A-Za-z_]\w*'),       # Identificadores
            ('OPERADOR', r'[+\-*/]'),      # Operadores aritméticos
            ('ESPACO', r'[ \t]+'),         # Espaços e tabulações
            ('NOVA_LINHA', r'\n'),         # Nova linha
            ('ERRO', r'.'),                # Caracteres inválidos
        ]
        
        for mo in re.finditer('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in especificacao_tokens), self.codigo_fonte):
            tipo = mo.lastgroup
            valor = mo.group()
            if tipo == 'NUMERO':
                valor = int(valor)
            elif tipo == 'ESPACO' or tipo == 'NOVA_LINHA':
                continue
            elif tipo == 'ERRO':
                raise RuntimeError(f'Caractere inesperado {valor}')
            self.tokens.append((tipo, valor))

        return self.tokens
