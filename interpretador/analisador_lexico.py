import re

class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens = []

    def analisar(self):
        # Definindo os padrões para os tokens
        especificacao_tokens = [
            ('NUMERO', r'\d+'),                   # Números inteiros
            ('ATRIBUIR', r'='),                   # Atribuição
            ('FIM', r';'),                        # Fim de instrução
            ('ID', r'[A-Za-z_]\w*'),              # Identificadores e palavras-chave
            ('OPERADOR_ARIT', r'[+\-*/]'),        # Operadores aritméticos
            ('OPERADOR_REL', r'==|!=|<=|>=|<|>'), # Operadores relacionais
            ('OPERADOR_LOG', r'\b(and|or|not)\b'),# Operadores lógicos
            ('PARENTESES_ESQ', r'\('),            # Parêntese esquerdo
            ('PARENTESES_DIR', r'\)'),            # Parêntese direito
            ('CHAVE_ESQ', r'\{'),                 # Chave esquerda
            ('CHAVE_DIR', r'\}'),                 # Chave direita
            ('COLCHETE_ESQ', r'\['),              # Colchete esquerdo para listas
            ('COLCHETE_DIR', r'\]'),              # Colchete direito para listas
            ('VIRGULA', r','),                    # Vírgula
            ('COMENTARIO', r'#.*'),               # Comentários
            ('ESPACO', r'[ \t]+'),                # Espaços e tabulações
            ('NOVA_LINHA', r'\n'),                # Nova linha
            ('ERRO', r'.'),                       # Caracteres inválidos
        ]
        
        # Compilação da expressão regular para melhorar o desempenho
        padrao_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in especificacao_tokens)
        
        # Palavras-chave específicas
        palavras_chave = {'if', 'else', 'for', 'while', 'def', 'return', 'in', 'to', 'print'}

        # Iteração sobre o código fonte usando finditer para reconhecer cada token
        for mo in re.finditer(padrao_regex, self.codigo_fonte):
            tipo = mo.lastgroup
            valor = mo.group()
            if tipo == 'NUMERO':
                valor = int(valor)
            elif tipo == 'ESPACO' or tipo == 'NOVA_LINHA' or tipo == 'COMENTARIO':
                continue
            elif tipo == 'ID' and valor in palavras_chave:
                tipo = valor.upper()  # Converte palavras-chave para tokens específicos
            elif tipo == 'ERRO':
                raise RuntimeError(f'Caractere inesperado: {valor} na posição {mo.start()}')
            self.tokens.append((tipo, valor))

        return self.tokens
