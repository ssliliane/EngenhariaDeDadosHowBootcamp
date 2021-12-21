import datetime
import math

class Pessoa:
    def __init__(self, nome:str, sobrenome: str, data_de_nascimento: datetime.date):
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    #decorator para indicar que é um propriedade de pessoa
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self)-> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos" 

liliane = Pessoa(nome="Liliane", sobrenome="Santos", data_de_nascimento=datetime.date(1985,2,18))

print(liliane)