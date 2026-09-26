from dataclasses import dataclass, field
from datetime import time

from atividade import Atividade

@dataclass
class Sala:
    id: int
    atividades: list[Atividade] = field(default_factory=list)

    @property
    def livre_a_partir(self) -> time:
        # a sala fica livre quando a ultima atividade dela termina
        return self.atividades[-1].fim

    def alocar(self, atividade: Atividade) -> None:
        self.atividades.append(atividade)
