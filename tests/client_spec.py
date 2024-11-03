import unittest

from client.calculadora_client import ClienteCalculadora
from port.channel import Channel

class TesteClienteCalculadora(unittest.TestCase):
    def test_cliente_envia_operacao(self):
        canal = Channel("CalculadoraCliente", port=12345)
        cliente = ClienteCalculadora(canal)
        resultado = cliente.enviar_operacao('+', 5, 3)
        self.assertEqual(resultado, '8')

if __name__ == '__main__':
    unittest.main()
