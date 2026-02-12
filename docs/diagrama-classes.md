# Diagrama de Classes  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Classes representa a estrutura estática do sistema, evidenciando as principais classes persistidas no banco de dados, seus atributos e os relacionamentos existentes entre elas.

O sistema segue arquitetura Web com Backend em Flask e Banco de Dados PostgreSQL.

---

# Classe: Profissional

Representa o usuário do sistema responsável por realizar e gerenciar agendamentos.

## Atributos

- id_profissional : Integer (PK)
- nome : String
- email : String (único)

## Relacionamentos

- Um Profissional pode possuir vários HorarioReservado.
- Um Profissional pode possuir várias Recorrencia.

---

# Classe: Sala

Representa as salas disponíveis para sublocação.

## Atributos

- id_sala : Integer (PK)
- nome : String (único)
- valor_hora : Decimal

## Relacionamentos

- Uma Sala pode possuir vários HorarioReservado.

---

# Classe: Recorrencia

Representa um padrão de agendamento recorrente criado pelo profissional.

## Atributos

- id_recorrencia : Integer (PK)
- dia_semana : List<Integer>  
  (0 = Domingo, 1 = Segunda, ..., 6 = Sábado)
- hora_inicio : Time
- hora_fim : Time
- data_inicio : Date
- data_fim : Date

## Regras de Integridade

- hora_fim > hora_inicio
- data_fim ≥ data_inicio
- Pelo menos um dia da semana deve ser informado

## Relacionamentos

- Uma Recorrencia pertence a um Profissional.
- Uma Recorrencia pode gerar vários HorarioReservado.

---

# Classe: HorarioReservado

Representa um horário efetivamente reservado no sistema.

## Atributos

- id_horario : Integer (PK)
- data_inicio : DateTime
- data_fim : DateTime
- tipo : Enum (AVULSO | RECORRENTE)
- status : Enum (ATIVO | CANCELADO)

## Regras de Integridade

- data_fim > data_inicio
- Se tipo = AVULSO → não possui Recorrencia associada
- Se tipo = RECORRENTE → deve estar associado a uma Recorrencia

## Relacionamentos

- Um HorarioReservado pertence a um Profissional.
- Um HorarioReservado pertence a uma Sala.
- Um HorarioReservado pode estar associado a uma Recorrencia.

---

# Relacionamentos e Cardinalidades

- Profissional 1 ─── N HorarioReservado
- Profissional 1 ─── N Recorrencia
- Sala 1 ─── N HorarioReservado
- Recorrencia 1 ─── N HorarioReservado

---

# Regras de Negócio Implementadas no Banco

As seguintes regras estão implementadas no PostgreSQL por meio de triggers:

### ✔ Bloqueio de Conflito de Horário
Função: `fn_bloquear_conflito()`

Impede inserção ou atualização de horários sobrepostos na mesma sala quando o status é ATIVO.

---

### ✔ Cancelamento com 24h de Antecedência
Função: `fn_cancelamento_24h()`

Permite cancelar apenas:
- Agendamentos do tipo AVULSO
- Com pelo menos 24 horas de antecedência

---

# Arquitetura do Sistema

Profissional  
→ Interface Web (HTML / CSS / JavaScript)  
→ Backend (Flask - Python)  
→ Banco de Dados (PostgreSQL)

---