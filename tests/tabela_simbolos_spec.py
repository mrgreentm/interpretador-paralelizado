import unittest

from interpretador.tabela_simbolos import TabelaDeSimbolos

class TesteTabelaDeSimbolos(unittest.TestCase):
    def test_tabela_simbolos_basico(self):
        tabela = TabelaDeSimbolos()
        tabela.adicionar_simbolo('x', 42)
        self.assertEqual(tabela.obter_simbolo('x'), 42)

if __name__ == '__main__':
    unittest.main()
