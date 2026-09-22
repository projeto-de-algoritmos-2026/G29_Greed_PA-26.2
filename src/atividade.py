from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True, slots=True)
class Atividade:
    id: str
    nome: str
    inicio: time
    fim: time

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("o ID da atividade nao pode estar vazio")
        if not self.nome.strip():
            raise ValueError("o nome da atividade nao pode estar vazio")
        if self.inicio >= self.fim:
            raise ValueError("o horario de inicio deve ser anterior ao de termino")

