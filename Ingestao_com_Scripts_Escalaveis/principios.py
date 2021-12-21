import datetime
import math
from typing import List

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

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]) :
        self.experiencias = experiencias
        self.pessoa = pessoa

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self):
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos, já " \
               f"trabalhou em {self.quantidade_de_experiencias} empresas " \
               f"e atualmente trabalha na empresa {self.empresa_atual}"

class Vivente:
    def __init__(self, nome:str, data_de_nascimento: datetime.date) -> None:
        self.data_de_nascimento = data_de_nascimento
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def emite_ruido(self, ruido:str):
        print (f"{self.nome} emitiu ruido: {ruido}")

class PessoaHeranca(Vivente):
    def __str__(self)-> str:
        return f"{self.nome} tem {self.idade} anos" 

    def fala(self, frase:str):
        return self.emite_ruido(frase)

class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str):
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def late(self):
        return self.emite_ruido('Au! Au!')


liliane = Pessoa(nome="Liliane", sobrenome="Santos", data_de_nascimento=datetime.date(1985,2,18))
print(liliane)

curriculo_liliane = Curriculo(
    pessoa=liliane,
    experiencias=['ACS','Powerlogic','Grupo Real','Algar Tech','Kyros']
)
print(curriculo_liliane)

curriculo_liliane.adiciona_experiencia('Tribanco')
print(curriculo_liliane)

lilianeHeranca = PessoaHeranca(nome='Liliane', data_de_nascimento=datetime.date(1985,2,18))
print(lilianeHeranca)

tommy = Cachorro(nome="Tommy", data_de_nascimento=datetime.date(2016,10,20), raca="Bulldog Francês")
print(tommy)

tommy.late()
tommy.late()
tommy.late()
lilianeHeranca.fala("Para de latir Tommy!")
tommy.late()