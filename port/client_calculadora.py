class ClienteCalculadora:
    def __init__(self, canal):
        self.canal = canal

    def enviar_operacao(self, operacao, valor1, valor2):
        mensagem = f"{operacao} {valor1} {valor2}"
        resultado = self.canal.enviar(mensagem)
        print(f"Resultado recebido: {resultado}")
