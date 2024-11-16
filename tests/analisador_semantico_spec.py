import unittest
from interpretador.analisador_sintatico import AnalisadorSintatico
from interpretador.analisador_semantico import AnalisadorSemantico

class TesteAnalisadorSemantico(unittest.TestCase):
    def test_semantico_basico(self):
        arvore = [('atribuir', 'x', 10)]
        analisador = AnalisadorSemantico(arvore)
        analisador.analisar()
        self.assertIn('x', analisador.tabela_de_simbolos)

if __name__ == '__main__':
    unittest.main()
