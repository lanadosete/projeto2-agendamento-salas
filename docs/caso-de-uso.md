# Casos de Uso  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

---

# 🎭 Ator Principal

**Profissional**  
Usuário responsável por utilizar o sistema para realizar e gerenciar agendamentos de salas.

---

# 📌 Caso de Uso 1 – Visualizar Salas Disponíveis

## Descrição
Permite ao profissional visualizar todas as salas cadastradas no sistema.

## Ator
Profissional

## Fluxo Principal
1. O profissional acessa o sistema.
2. O profissional seleciona a opção "Visualizar Salas".
3. O sistema consulta o banco de dados.
4. O sistema exibe a lista de salas com nome e valor por hora.

## Fluxo Alternativo
- Caso não existam salas cadastradas, o sistema informa que não há salas disponíveis.

---

# 📌 Caso de Uso 2 – Agendar Horário Avulso

## Descrição
Permite ao profissional reservar uma sala em um horário específico.

## Ator
Profissional

## Fluxo Principal
1. O profissional seleciona uma sala.
2. O profissional informa:
   - Data
   - Hora de início
   - Hora de fim
3. O sistema valida:
   - Data não pode estar no passado.
   - Hora final deve ser maior que hora inicial.
4. O sistema verifica conflito de horário.
5. O sistema registra o agendamento como ATIVO.
6. O sistema exibe confirmação de sucesso.

## Fluxos Alternativos

### 2A – Conflito de horário
- O sistema detecta sobreposição com outro agendamento.
- O sistema exibe mensagem de erro.

### 2B – Data no passado
- O sistema bloqueia o agendamento.
- Exibe mensagem de erro.

---

# 📌 Caso de Uso 3 – Agendar Horário Recorrente

## Descrição
Permite ao profissional criar um padrão de agendamento repetido em dias específicos da semana.

## Ator
Profissional

## Fluxo Principal
1. O profissional seleciona uma sala.
2. Marca a opção "Agendamento recorrente".
3. Informa:
   - Data inicial
   - Data final
   - Hora início
   - Hora fim
   - Dias da semana
4. O sistema valida:
   - Data final ≥ data inicial
   - Data inicial não pode estar no passado
   - Pelo menos um dia da semana selecionado
   - Hora final > hora inicial
5. O sistema cria um registro de Recorrencia.
6. O sistema gera automaticamente os HorariosReservados correspondentes.
7. O sistema verifica conflitos em cada ocorrência.
8. Caso não haja conflito, salva todos os registros.
9. O sistema exibe confirmação de sucesso.

## Fluxos Alternativos

### 3A – Conflito em uma ocorrência
- O sistema cancela toda a operação.
- Nenhuma ocorrência é salva.
- Exibe mensagem de erro.

### 3B – Nenhum dia selecionado
- O sistema bloqueia o envio.
- Exibe mensagem de erro.

---

# 📌 Caso de Uso 4 – Cancelar Agendamento

## Descrição
Permite cancelar um agendamento avulso ativo.

## Ator
Profissional

## Fluxo Principal
1. O profissional acessa "Meus Agendamentos".
2. Seleciona um agendamento avulso ativo.
3. Solicita cancelamento.
4. O sistema verifica:
   - Se é do tipo AVULSO.
   - Se possui pelo menos 24 horas de antecedência.
5. O sistema altera o status para CANCELADO.
6. O sistema exibe confirmação.

## Fluxos Alternativos

### 4A – Tentativa de cancelar recorrente
- Sistema bloqueia.
- Exibe mensagem de erro.

### 4B – Menos de 24h
- Sistema bloqueia.
- Exibe mensagem de erro.

---

# 📌 Caso de Uso 5 – Consultar Meus Agendamentos

## Descrição
Permite visualizar agendamentos filtrando por tipo.

## Ator
Profissional

## Fluxo Principal
1. O profissional acessa "Meus Agendamentos".
2. Seleciona o filtro:
   - Avulsos
   - Recorrentes
   - Histórico
3. O sistema consulta o banco.
4. O sistema exibe os registros conforme o filtro.

---

# 📌 Caso de Uso 6 – Consultar Valor Mensal

## Descrição
Permite consultar o total mensal baseado nos agendamentos ativos.

## Ator
Profissional

## Fluxo Principal
1. O profissional acessa "Consultar Valor Mensal".
2. Seleciona o mês desejado.
3. O sistema calcula:
   - Total geral
   - Total avulsos
   - Total recorrentes
4. O sistema exibe os valores.

## Regra de Negócio
- Apenas agendamentos com status ATIVO são considerados no cálculo.

---

# 📌 Caso de Uso 7 – Visualizar Histórico

## Descrição
Permite visualizar:
- Agendamentos cancelados
- Agendamentos já finalizados

## Ator
Profissional

## Fluxo Principal
1. O profissional seleciona o filtro "Histórico".
2. O sistema consulta registros cancelados ou expirados.
3. O sistema exibe os dados.

---

# 📌 Caso de Uso 8 – Validação de Conflito

## Descrição
Garante que não existam reservas sobrepostas na mesma sala.

## Ator
Sistema

## Regra
- Não é permitido inserir ou atualizar horários que se sobreponham a outro ATIVO.

---

# 📌 Caso de Uso 9 – Validação de Datas e Dias da Semana

## Descrição
Garante integridade nas recorrências.

## Regras
- Data final ≥ data inicial.
- Data não pode estar no passado.
- Pelo menos um dia da semana selecionado.
- A data escolhida deve coincidir com os dias permitidos.
- Hora final > hora inicial.

---

# 📌 Caso de Uso 10 – Cálculo Automático do Valor Mensal

## Descrição
Calcula automaticamente o valor com base na duração do horário e no valor da sala.

## Regra
Valor = (Horas Utilizadas) × (Valor da Sala)

---