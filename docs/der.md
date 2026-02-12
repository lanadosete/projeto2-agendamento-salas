# Diagrama Entidade-Relacionamento (DER)  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

---

## Identificação das Entidades

O sistema armazena informações referentes às salas disponíveis, aos profissionais que realizam agendamentos, aos horários reservados e aos padrões de recorrência.

As entidades identificadas são:

- Profissional
- Sala
- HorarioReservado
- Recorrencia

---

## Entidades e Atributos

---

### Entidade: Profissional

Representa o usuário que utiliza o sistema para realizar agendamentos.

**Atributos:**

- id_profissional (PK)
- nome
- email (único)

**Relacionamentos:**

- Um profissional pode realizar vários agendamentos.
- Um profissional pode possuir várias recorrências.

---

### Entidade: Sala

Representa as salas disponíveis para sublocação.

**Atributos:**

- id_sala (PK)
- nome (único)
- valor_hora

**Relacionamentos:**

- Uma sala pode possuir vários horários reservados.

---

### Entidade: HorarioReservado

Representa um horário específico reservado por um profissional em uma sala.

**Atributos:**

- id_horario (PK)
- id_profissional (FK → Profissional)
- id_sala (FK → Sala)
- data_inicio (TIMESTAMPTZ)
- data_fim (TIMESTAMPTZ)
- tipo (AVULSO ou RECORRENTE)
- status (ATIVO ou CANCELADO)
- id_recorrencia (FK opcional → Recorrencia)

**Regras de Negócio Implementadas:**

- data_fim deve ser maior que data_inicio.
- Não pode haver conflito de horários na mesma sala.
- Cancelamento permitido apenas para agendamentos AVULSOS.
- Cancelamento deve respeitar antecedência mínima de 24 horas.
- Se tipo = AVULSO → id_recorrencia deve ser NULL.
- Se tipo = RECORRENTE → id_recorrencia deve estar preenchido.

**Relacionamentos:**

- Um horário reservado pertence a um profissional.
- Um horário reservado pertence a uma sala.
- Um horário reservado pode estar associado a uma recorrência.

---

### Entidade: Recorrencia

Representa um padrão de repetição para criação automática de múltiplos horários reservados.

**Atributos:**

- id_recorrencia (PK)
- id_profissional (FK → Profissional)
- dia_semana (ARRAY de inteiros)
- hora_inicio (TIME)
- hora_fim (TIME)
- data_inicio (DATE)
- data_fim (DATE)

**Observação Importante:**

O atributo dia_semana é armazenado como ARRAY de inteiros, permitindo que uma única recorrência contenha múltiplos dias da semana (exemplo: [1, 3, 5]).

**Relacionamentos:**

- Uma recorrência pertence a um profissional.
- Uma recorrência pode gerar vários horários reservados.

---

## Cardinalidades

- Profissional (1) — (N) HorarioReservado
- Sala (1) — (N) HorarioReservado
- Profissional (1) — (N) Recorrencia
- Recorrencia (1) — (N) HorarioReservado

---

## Observações Estruturais do Modelo

- O sistema utiliza TIMESTAMPTZ para controle preciso de horários.
- O bloqueio de conflitos é realizado por trigger no banco de dados.
- O controle de cancelamento (24h) também é realizado por trigger.
- O cálculo mensal é feito por meio da view vw_valor_mensal.
- O modelo garante integridade entre agendamentos avulsos e recorrentes por meio de constraints.