from interfaces import IComponent
from services import AnalisadorLexico

class AnalisadorLexicoComponent(IComponent):
    def process(self, code):
        analisador_lexico = AnalisadorLexico()
        return analisador_lexico.tokenerizar(self, code)