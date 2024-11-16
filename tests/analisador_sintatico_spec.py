import unittest
from interpretador.analisador_lexico import AnalisadorLexico
from interpretador.analisador_sintatico import AnalisadorSintatico

class TesteAnalisadorSintatico(unittest.TestCase):
    def test_sintatico_basico(self):
        codigo_fonte = "x = 5 + 10;"
        analisador_lexico = AnalisadorLexico(codigo_fonte)
        tokens = analisador_lexico.analisar()
        analisador_sintatico = AnalisadorSintatico(tokens)
        arvore = analisador_sintatico.analisar()
        self.assertEqual(arvore, [('atribuir', 'x', ('+', 5, 10))])

if __name__ == '__main__':
    unittest.main()
