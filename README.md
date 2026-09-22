# Alocação Otimizada de Salas com Interval Partitioning

## Alunos

| Matrícula | Aluno |
| -- | -- |
| 211041105 | Bruna de Lima Santos |
| 212005453 | Pedro Luciano de Azevedo |

## Sobre

Trabalho 2 da disciplina de Projeto de Algoritmos do 2º semestre de 2026. O sistema recebe uma grade de atividades acadêmicas e determina a quantidade mínima de salas necessária para realizá-las sem conflitos de horário.

### Problema

Uma instituição precisa distribuir aulas e outras atividades entre salas. Atividades simultâneas não podem ocupar a mesma sala, enquanto uma sala pode ser reutilizada assim que a atividade anterior terminar.

O objetivo é encontrar uma distribuição válida usando o menor número possível de salas.

### Solução

As atividades são importadas de um arquivo CSV contendo identificador, nome, horário de início e horário de término. O sistema utiliza o algoritmo ambicioso de **Interval Partitioning** para distribuir as atividades entre as salas.

Os intervalos são considerados no formato `[início, fim)`. Isso significa que uma atividade que termina às 10:00 não entra em conflito com outra que começa exatamente às 10:00.

Ao final da implementação, o sistema apresenta:

- Quantidade mínima de salas utilizadas;
- Atividades alocadas em cada sala;
- Linha do tempo das salas;
- Pico de atividades simultâneas.

### Algoritmo

O Interval Partitioning processa as atividades em ordem crescente de início. Uma fila de prioridade (*min-heap*) mantém as salas ordenadas pelo horário em que estarão disponíveis.

Para cada atividade:

1. Consulta-se a sala que ficará livre primeiro;
2. Se a sala estiver disponível no início da atividade, ela será reutilizada;
3. Caso contrário, uma nova sala será criada;
4. A atividade será adicionada à sala escolhida;
5. O novo horário de disponibilidade será inserido na fila de prioridade.

O pico de simultaneidade será calculado separadamente. Para horários iguais, eventos de término serão processados antes dos eventos de início, respeitando a convenção `[início, fim)`.

### Formato de entrada

O programa recebe um arquivo CSV com as colunas `id`, `nome`, `inicio` e `fim`. Os horários devem seguir o formato `HH:MM`.

Exemplo:

```csv
id,nome,inicio,fim
1,EDA2,08:00,09:50
2,PA,10:00,11:50
3,Redes,08:00,09:50
```

Um arquivo pronto para demonstração está disponível em [`exemplos/atividades.csv`](./exemplos/atividades.csv).

### Complexidade

Com `n` atividades, a ordenação custa `O(n log n)`. Cada atividade realiza uma consulta e uma atualização na fila de prioridade, também limitadas a `O(log n)`. Dessa forma, a complexidade esperada do algoritmo completo é:

| Operação | Complexidade |
| -- | -- |
| Ler o arquivo CSV | `O(n)` |
| Ordenar as atividades | `O(n log n)` |
| Alocar atividades com *min-heap* | `O(n log n)` |
| Calcular o pico de simultaneidade | `O(n log n)` |
| **Complexidade final** | `O(n log n)` |

## Screenshots

## [Clique aqui para assistir à apresentação](#)

## Instalação

### Pré-requisitos

Antes de começar, certifique-se de ter:

- Python 3.10 ou superior
- Git

Após isso, clone o repositório, acesse a pasta do projeto e siga as instruções
abaixo.

### 1) Instale as dependências do sistema

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

### 2) Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

## Execução

Na raiz do projeto, ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Em seguida, execute:

```bash
python src/main.py exemplos/atividades.csv
```

### Testes

```bash
python -m unittest discover testes
```