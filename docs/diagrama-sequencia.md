# Diagrama de Sequência  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Sequência representa a interação temporal entre os componentes do sistema, evidenciando a troca de mensagens entre os participantes para execução dos principais casos de uso.

O sistema segue arquitetura Web:

Profissional  
→ Interface Web (Frontend)  
→ Backend (Flask)  
→ Banco de Dados (PostgreSQL)

---

# 1. Agendar Horário Avulso

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. Profissional informa sala, data, hora início e hora fim.
2. Interface Web envia requisição:
   POST /agendamentos/avulso
3. Backend recebe os dados.
4. Backend realiza validações:
   - Data não pode estar no passado
   - Hora final > hora inicial
5. Backend chama função auxiliar `existe_conflito()`.
6. Backend envia comando INSERT para tabela `horario_reservado`.
7. Banco executa:
   - Constraints
   - Trigger `fn_bloquear_conflito()`
8. Banco retorna:
   - Sucesso → OK
   - Erro → Exception
9. Backend executa:
   - Commit (em caso de sucesso)
   - Rollback (em caso de erro)
10. Backend retorna resposta JSON.
11. Interface Web exibe:
   - Modal de sucesso
   ou
   - Toast de erro.

---

# 2. Agendar Horário Recorrente

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. Profissional ativa modo recorrente.
2. Profissional informa:
   - Data inicial
   - Data final
   - Hora início
   - Hora fim
   - Dias da semana
3. Interface envia:
   POST /agendamentos/recorrente
4. Backend valida:
   - Data final ≥ data inicial
   - Data inicial não pode estar no passado
   - Pelo menos um dia selecionado
   - Hora final > hora inicial
5. Backend insere registro na tabela `recorrencia`.
6. Backend percorre o intervalo de datas:
   - Para cada data válida:
     - Verifica conflito
     - Prepara horário da ocorrência
7. Backend envia INSERT para cada ocorrência em `horario_reservado`.
8. Banco executa:
   - Constraints
   - Trigger `fn_bloquear_conflito()`
9. Caso ocorra conflito:
   - Banco retorna erro
   - Backend executa rollback completo
10. Caso todas ocorrências sejam válidas:
    - Backend executa commit
11. Backend retorna JSON.
12. Interface exibe confirmação ou erro.

---

# 3. Cancelar Agendamento

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. Profissional seleciona agendamento avulso ativo.
2. Interface envia:
   POST /agendamentos/cancelar
3. Backend executa UPDATE em `horario_reservado`.
4. Banco executa Trigger `fn_cancelamento_24h()`:
   - Verifica tipo = AVULSO
   - Verifica antecedência mínima de 24h
5. Banco retorna sucesso ou erro.
6. Backend executa commit ou rollback.
7. Backend retorna JSON.
8. Interface exibe modal de confirmação ou mensagem de erro.

---

# 4. Listar Agendamentos

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. Profissional seleciona filtro:
   - AVULSO
   - RECORRENTE
   - HISTÓRICO
2. Interface envia:
   GET /agendamentos?filtro=...
3. Backend executa consulta correspondente:
   - SELECT simples para avulsos
   - SELECT com JOIN e agregação para recorrentes
   - SELECT combinado para histórico
4. Banco retorna registros.
5. Backend formata dados em JSON.
6. Interface renderiza lista.

---

# 5. Consultar Valor Mensal

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. Profissional seleciona mês.
2. Interface envia:
   GET /valor-mensal/detalhado
3. Backend executa três consultas:
   - Total geral
   - Total avulso
   - Total recorrente
4. Banco retorna valores agregados.
5. Backend envia JSON.
6. Interface exibe resumo financeiro.

---

# Considerações Técnicas

- Validações ocorrem em dois níveis:
  1. Backend (regra de negócio)
  2. Banco de Dados (garantia de integridade)

- Conflito de horário protegido por:
  - Função Python `existe_conflito()`
  - Trigger `fn_bloquear_conflito()`

- Cancelamento protegido por:
  - Trigger `fn_cancelamento_24h()`

- Comunicação Frontend ↔ Backend ocorre via Fetch API (AJAX).

- Todas as respostas são retornadas em formato JSON.