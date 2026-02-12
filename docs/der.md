# Diagrama Entidade-Relacionamento (DER)  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

---

## Identificação das Entidades

O sistema armazena informações referentes:

- Aos profissionais que realizam agendamentos
- Às salas disponíveis para sublocação
- Aos horários reservados
- Aos padrões de recorrência

As entidades identificadas são:

- Profissional
- Sala
- HorarioReservado
- Recorrencia

---

# Entidades e Atributos

---

## Entidade: Profissional

Representa o usuário que utiliza o sistema para realizar agendamentos.

### Atributos

- id_profissional (PK)
- nome
- email (único)

### Relacionamentos

- Um profissional pode realizar vários horários reservados.
- Um profissional pode possuir várias recorrências.

---

## Entidade: Sala

Representa as salas disponíveis para sublocação.

### Atributos

- id_sala (PK)
- nome (único)
- valor_hora (NUMERIC)

### Relacionamentos

- Uma sala pode possuir vários horários reservados.

---

## Entidade: HorarioReservado

Representa um horário específico reservado por um profissional em uma sala.

### Atributos

- id_horario (PK)
- id_profissional (FK → Profissional)
- id_sala (FK → Sala)
- data_inicio (TIMESTAMPTZ)
- data_fim (TIMESTAMPTZ)
- tipo (AVULSO | RECORRENTE)
- status (ATIVO | CANCELADO)
- id_recorrencia (FK opcional → Recorrencia)

### Regras de Integridade

- data_fim > data_inicio
- Se tipo = AVULSO → id_recorrencia deve ser NULL
- Se tipo = RECORRENTE → id_recorrencia deve estar preenchido
- Não é permitido conflito de horários na mesma sala (garantido por trigger)
- Cancelamento permitido apenas para AVULSO
- Cancelamento exige antecedência mínima de 24 horas

### Relacionamentos

- Um horário reservado pertence a um profissional.
- Um horário reservado pertence a uma sala.
- Um horário reservado pode estar associado a uma recorrência.

---

## Entidade: Recorrencia

Representa um padrão de repetição para geração automática de múltiplos horários reservados.

### Atributos

- id_recorrencia (PK)
- id_profissional (FK → Profissional)
- dia_semana (ARRAY de inteiros)
- hora_inicio (TIME)
- hora_fim (TIME)
- data_inicio (DATE)
- data_fim (DATE)

### Observação

O atributo `dia_semana` é armazenado como ARRAY de inteiros, permitindo que uma única recorrência contenha múltiplos dias da semana.

Padrão utilizado:
- 0 = Domingo
- 1 = Segunda
- 2 = Terça
- 3 = Quarta
- 4 = Quinta
- 5 = Sexta
- 6 = Sábado

### Regras de Integridade

- data_fim ≥ data_inicio
- hora_fim > hora_inicio

### Relacionamentos

- Uma recorrência pertence a um profissional.
- Uma recorrência pode gerar vários horários reservados.

---

# Cardinalidades do Modelo

- Profissional (1) —— (N) HorarioReservado
- Sala (1) —— (N) HorarioReservado
- Profissional (1) —— (N) Recorrencia
- Recorrencia (1) —— (N) HorarioReservado

---

# Observações Estruturais do Modelo

- O sistema utiliza TIMESTAMPTZ para controle preciso de horários.
- O bloqueio de conflitos é implementado por trigger no banco de dados.
- O controle de cancelamento com antecedência mínima de 24h também é implementado por trigger.
- O cálculo mensal é realizado por meio da view vw_valor_mensal.
- O modelo garante integridade entre agendamentos avulsos e recorrentes por meio de constraints e chaves estrangeiras.