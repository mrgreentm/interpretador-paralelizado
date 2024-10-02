from interfaces import IComponent
from services import AnalisadorSintatico

class AnalisadorSintaticoComponent(IComponent):
    def process(self, tokens):
        parser = AnalisadorSintatico(tokens)
        return parser.parse()