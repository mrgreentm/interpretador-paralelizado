class ServidorCalculadora:
    def __init__(self, canal):
        self.canal = canal

    def executar(self):
        while True:
            dados, conn = self.canal.receber()
            operacao, valor1, valor2 = dados.split()
            valor1, valor2 = int(valor1), int(valor2)
            resultado = self.calcular(operacao, valor1, valor2)
            conn.sendall(str(resultado).encode('utf-8'))
            print(f"Operação: {operacao}, Valores: {valor1}, {valor2}, Resultado: {resultado}")

    def calcular(self, operacao, valor1, valor2):
        if operacao == '+':
            return valor1 + valor2
        elif operacao == '-':
            return valor1 - valor2
        elif operacao == '*':
            return valor1 * valor2
        elif operacao == '/':
            return valor1 / valor2
        else:
            raise ValueError(f"Operação inválida: {operacao}")
