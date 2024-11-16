import unittest
from interpretador.analisador_lexico import AnalisadorLexico

class TesteAnalisadorLexico(unittest.TestCase):
    def test_lexico_basico(self):
        codigo_fonte = "x = 10;"
        analisador = AnalisadorLexico(codigo_fonte)
        tokens = analisador.analisar()
        self.assertEqual(tokens, [('ID', 'x'), ('ATRIBUIR', '='), ('NUMERO', 10), ('FIM', ';')])

if __name__ == '__main__':
    unittest.main()
