import unittest

from port.channel import Channel
from port.server_calculadora import ServidorCalculadora

class TesteServidorCalculadora(unittest.TestCase):
    def test_servidor_calcula(self):
        canal = Channel("CalculadoraServidor", port=12345)
        servidor = ServidorCalculadora(canal)
        resultado = servidor.calcular('+', 5, 3)
        self.assertEqual(resultado, 8)

if __name__ == '__main__':
    unittest.main()
