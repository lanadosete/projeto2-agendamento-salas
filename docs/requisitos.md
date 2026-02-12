# Documento de Requisitos  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

**Disciplina:** Projeto Integrado I  
**Curso:** Sistemas de Informação  
**Instituição:** UFPA – Campus Cametá  

---

# 1. Introdução

Este documento descreve os requisitos do Sistema de Gestão de Agendamento de Sublocação de Salas,
desenvolvido como Projeto 2 da disciplina Projeto Integrado I.

O sistema tem como objetivo permitir que um profissional realize o gerenciamento de
agendamentos de salas, aplicando regras de negócio para:

- Evitar conflitos de horários
- Controlar recorrências
- Permitir cancelamentos com restrições
- Calcular automaticamente o valor mensal devido

O sistema foi desenvolvido como um MVP (Produto Mínimo Viável),
priorizando a implementação das regras de negócio essenciais.

---

# 2. Escopo do Sistema

O sistema permite:

- Visualizar salas disponíveis
- Agendar horários avulsos
- Agendar horários recorrentes
- Cancelar agendamentos avulsos
- Visualizar agendamentos ativos
- Visualizar histórico de agendamentos
- Consultar o valor mensal devido

Não faz parte do escopo:

- Autenticação de múltiplos usuários
- Pagamentos reais
- Cancelamento de recorrências completas
- Notificações automáticas

---

# 3. Requisitos Funcionais

## RF01 – Visualizar Salas
O sistema deve permitir que o profissional visualize todas as salas disponíveis, exibindo:
- Nome da sala
- Valor por hora

---

## RF02 – Agendar Horário Avulso
O sistema deve permitir que o profissional realize agendamento avulso informando:
- Sala
- Data
- Hora de início
- Hora de fim

O sistema deve:
- Validar que a data não seja no passado
- Validar que a hora final seja maior que a hora inicial
- Verificar conflito de horário
- Registrar o agendamento como ATIVO

---

## RF03 – Agendar Horário Recorrente
O sistema deve permitir que o profissional realize agendamento recorrente informando:
- Sala
- Data inicial
- Data final
- Hora de início
- Hora de fim
- Dias da semana

O sistema deve:
- Validar que a data final seja maior ou igual à data inicial
- Validar que a data inicial não esteja no passado
- Validar que pelo menos um dia da semana esteja selecionado
- Validar que a hora final seja maior que a hora inicial
- Gerar automaticamente todas as ocorrências
- Verificar conflito em cada ocorrência
- Cancelar toda a operação caso exista conflito

---

## RF04 – Impedir Conflito de Horário
O sistema deve impedir a inserção ou atualização de horários que se sobreponham
a outro agendamento ATIVO na mesma sala.

A validação deve ocorrer:
- No backend
- No banco de dados (trigger)

---

## RF05 – Cancelar Agendamento Avulso
O sistema deve permitir cancelar apenas agendamentos do tipo AVULSO.

O sistema deve:
- Verificar se o agendamento está ATIVO
- Verificar se o cancelamento ocorre com pelo menos 24 horas de antecedência
- Alterar o status para CANCELADO

---

## RF06 – Visualizar Meus Agendamentos
O sistema deve permitir visualizar agendamentos com os seguintes filtros:
- Avulsos ativos
- Recorrentes ativos
- Histórico (cancelados ou finalizados)

---

## RF07 – Consultar Valor Mensal
O sistema deve permitir consultar o valor mensal com base nos agendamentos ATIVOS.

O sistema deve:
- Permitir selecionar o mês
- Calcular o total geral
- Calcular o total de avulsos
- Calcular o total de recorrentes
- Exibir os valores detalhados

---

## RF08 – Registrar Recorrência
O sistema deve armazenar:
- Dias da semana selecionados
- Intervalo de datas
- Horário
- Profissional associado

---

## RF09 – Manter Histórico
O sistema deve manter registros cancelados e finalizados para consulta posterior.

---

# 4. Requisitos Não Funcionais

## RNF01 – Banco de Dados
O sistema deve utilizar PostgreSQL para armazenamento das informações.

---

## RNF02 – Backend
O sistema deve ser desenvolvido utilizando Python com framework Flask.

---

## RNF03 – Interface
O sistema deve possuir interface web simples, responsiva e intuitiva.

---

## RNF04 – Integridade de Dados
O sistema deve garantir integridade por meio de:
- Constraints no banco
- Triggers para bloqueio de conflito
- Triggers para regra de cancelamento
- Validações no backend

---

## RNF05 – Desempenho
As consultas de listagem e cálculo mensal devem ser executadas em tempo adequado
para uso acadêmico.

---

## RNF06 – Usabilidade
O sistema deve:
- Exibir mensagens claras de erro
- Utilizar modais para confirmação
- Utilizar notificações (toast) para feedback ao usuário

---

## RNF07 – MVP Acadêmico
O sistema deve atender aos requisitos mínimos definidos para o Projeto Integrado I,
sem necessidade de autenticação ou controle multiusuário.

---

# 5. Regras de Negócio

## RN01 – Conflito de Horário
Não é permitido haver dois agendamentos ATIVOS para a mesma sala
com sobreposição de horário.

---

## RN02 – Cancelamento 24h
Cancelamentos só podem ocorrer com no mínimo 24 horas de antecedência.

---

## RN03 – Cálculo de Valor
Valor mensal = (Horas Utilizadas) × (Valor da Sala)

---

## RN04 – Recorrência Atômica
Se qualquer ocorrência da recorrência gerar conflito,
toda a operação deve ser cancelada.

---

## RN05 – Datas Válidas
- Data inicial não pode estar no passado.
- Data final deve ser maior ou igual à data inicial.

---

# 6. Tecnologias Utilizadas

- Python
- Flask
- PostgreSQL
- HTML
- CSS
- JavaScript
- Git e GitHub