# Diagrama de Classes  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Classes representa a estrutura estática do sistema, evidenciando as principais entidades persistidas no banco de dados, seus atributos e os relacionamentos existentes entre elas.

O sistema segue arquitetura Web com Backend em Flask e Banco de Dados PostgreSQL.

---

# Classe: Profissional

Representa o usuário do sistema responsável por realizar agendamentos.

## Atributos

- id_profissional : BIGSERIAL (PK)
- nome : VARCHAR(120)
- email : VARCHAR(120) (único)

## Relacionamentos

- Um Profissional pode possuir vários HorarioReservado.
- Um Profissional pode possuir várias Recorrencias.

---

# Classe: Sala

Representa as salas disponíveis para sublocação.

## Atributos

- id_sala : BIGSERIAL (PK)
- nome : VARCHAR(50) (único)
- valor_hora : NUMERIC(10,2)

## Relacionamentos

- Uma Sala pode possuir vários HorarioReservado.

---

# Classe: Recorrencia

Representa um padrão de agendamento recorrente criado pelo profissional.

## Atributos

- id_recorrencia : BIGSERIAL (PK)
- id_profissional : BIGINT (FK → Profissional)
- dia_semana : INTEGER[]  
  (array contendo os dias da semana selecionados)
- hora_inicio : TIME
- hora_fim : TIME
- data_inicio : DATE
- data_fim : DATE

## Regras

- hora_fim > hora_inicio
- data_fim ≥ data_inicio

## Relacionamentos

- Uma Recorrencia pertence a um Profissional.
- Uma Recorrencia pode gerar vários HorarioReservado.

---

# Classe: HorarioReservado

Representa um horário efetivamente reservado no sistema.

## Atributos

- id_horario : BIGSERIAL (PK)
- id_profissional : BIGINT (FK → Profissional)
- id_sala : BIGINT (FK → Sala)
- data_inicio : TIMESTAMPTZ
- data_fim : TIMESTAMPTZ
- tipo : VARCHAR(12)  
  (AVULSO | RECORRENTE)
- status : VARCHAR(12)  
  (ATIVO | CANCELADO)
- id_recorrencia : BIGINT (FK → Recorrencia, opcional)

## Regras

- data_fim > data_inicio
- Se tipo = AVULSO → id_recorrencia deve ser NULL
- Se tipo = RECORRENTE → id_recorrencia não pode ser NULL

## Relacionamentos

- Um HorarioReservado pertence a um Profissional.
- Um HorarioReservado pertence a uma Sala.
- Um HorarioReservado pode estar associado a uma Recorrencia.

---

# Relacionamentos Gerais

- Profissional 1 ─── N HorarioReservado
- Profissional 1 ─── N Recorrencia
- Sala 1 ─── N HorarioReservado
- Recorrencia 1 ─── N HorarioReservado

---

# Regras de Negócio Implementadas

As regras abaixo não são apenas conceituais — elas estão implementadas no Banco de Dados via triggers:

### ✔ Bloqueio de Conflito de Horário
Implementado pela função:
- fn_bloquear_conflito()

Impede inserção ou atualização de horários sobrepostos na mesma sala.

---

### Cancelamento com 24h de Antecedência
Implementado pela função:
- fn_cancelamento_24h()

Permite cancelar apenas:
- Agendamentos AVULSOS
- Com pelo menos 24 horas de antecedência

---

# Arquitetura

O sistema segue modelo:

Profissional  
→ Interface Web (HTML/CSS/JS)  
→ Backend Flask  
→ PostgreSQL  

---