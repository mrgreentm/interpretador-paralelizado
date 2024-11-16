import unittest
from interpretador.interpretador import Interpretador
from interpretador.tabela_simbolos import TabelaDeSimbolos

class TesteInterpretador(unittest.TestCase):
    def test_interpretador_basico(self):
        arvore = [('atribuir', 'x', ('+', 5, 10))]
        tabela = TabelaDeSimbolos()
        interpretador = Interpretador(arvore, tabela)
        interpretador.executar()
        self.assertEqual(tabela.obter_simbolo('x'), 15)

if __name__ == '__main__':
    unittest.main()
