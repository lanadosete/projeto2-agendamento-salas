# Diagrama de Sequência  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Sequência representa a interação entre os componentes do sistema ao longo do tempo, demonstrando como as mensagens são trocadas entre os participantes para execução dos casos de uso.

---

# 1️⃣ Agendar Horário Avulso

## Participantes
- Profissional
- Interface Web (Frontend)
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência

1. Profissional informa sala, data e horário.
2. Interface Web envia requisição `POST /agendamentos/avulso`.
3. Backend recebe os dados.
4. Backend valida:
   - Data não está no passado
   - Hora final maior que hora inicial
5. Backend chama função `existe_conflito()`.
6. Backend solicita INSERT em `horario_reservado`.
7. Banco executa:
   - Constraints
   - Trigger `fn_bloquear_conflito()`
8. Banco retorna sucesso ou erro.
9. Backend faz commit ou rollback.
10. Backend retorna JSON para Interface.
11. Interface exibe:
    - Modal de sucesso
    ou
    - Toast de erro.

---

# 2️⃣ Agendar Horário Recorrente

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência

1. Profissional ativa modo recorrente.
2. Profissional informa:
   - Data inicial
   - Data final
   - Hora início
   - Hora fim
   - Dias da semana
3. Interface envia `POST /agendamentos/recorrente`.
4. Backend valida:
   - Data final ≥ data inicial
   - Data inicial não está no passado
   - Pelo menos um dia selecionado
   - Hora final > hora inicial
5. Backend insere registro na tabela `recorrencia`.
6. Backend percorre intervalo de datas:
   - Gera cada ocorrência
   - Verifica conflito para cada data
7. Backend insere registros em `horario_reservado`.
8. Banco executa:
   - Constraint
   - Trigger de conflito
9. Em caso de conflito:
   - Backend faz rollback completo.
10. Em caso de sucesso:
   - Backend faz commit.
11. Interface exibe resultado.

---

# 3️⃣ Cancelar Agendamento

## Participantes
- Profissional
- Interface Web
- Backend
- Banco de Dados

## Sequência

1. Profissional clica em cancelar.
2. Interface envia `POST /agendamentos/cancelar`.
3. Backend executa UPDATE em `horario_reservado`.
4. Banco executa Trigger `fn_cancelamento_24h()`:
   - Verifica se é AVULSO
   - Verifica se possui 24h de antecedência
5. Banco retorna sucesso ou erro.
6. Backend faz commit ou rollback.
7. Interface exibe modal de confirmação ou erro.

---

# 4️⃣ Listar Agendamentos

## Participantes
- Profissional
- Interface Web
- Backend
- Banco de Dados

## Sequência

1. Profissional seleciona filtro:
   - Avulso
   - Recorrente
   - Histórico
2. Interface envia `GET /agendamentos?filtro=...`
3. Backend executa SELECT correspondente:
   - Consulta simples para avulsos
   - Consulta com JOIN e agregação para recorrentes
   - Consulta combinada para histórico
4. Banco retorna registros.
5. Backend formata dados em JSON.
6. Interface renderiza lista na tela.

---

# 5️⃣ Consultar Valor Mensal

## Participantes
- Profissional
- Interface Web
- Backend
- Banco de Dados

## Sequência

1. Profissional seleciona mês.
2. Interface envia `GET /valor-mensal/detalhado`.
3. Backend executa 3 consultas:
   - Total geral
   - Total avulso
   - Total recorrente
4. Banco retorna valores agregados.
5. Backend envia JSON.
6. Interface exibe resumo financeiro.

---

# 🔎 Considerações Técnicas Importantes

- A validação ocorre em dois níveis:
  1. Backend (regra de negócio)
  2. Banco de Dados (garantia de integridade)

- Conflito de horário é protegido por:
  - Função auxiliar Python
  - Trigger `fn_bloquear_conflito`

- Cancelamento é protegido por:
  - Trigger `fn_cancelamento_24h`

- A comunicação Frontend ↔ Backend ocorre via Fetch API (AJAX).

- Todas as respostas são retornadas em formato JSON.

---