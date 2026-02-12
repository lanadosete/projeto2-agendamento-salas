# Documento de Requisitos  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

**Disciplina:** Projeto Integrado I  
**Curso:** Sistemas de Informação  
**Instituição:** UFPA – Campus Cametá  

---

# 1. Introdução

Este documento descreve os requisitos do Sistema de Gestão de Agendamento de Sublocação de Salas, desenvolvido como Projeto 2 da disciplina Projeto Integrado I.

O sistema tem como objetivo permitir que um profissional realize o gerenciamento de agendamentos de salas, aplicando regras de negócio para:

- Evitar conflitos de horários
- Controlar agendamentos recorrentes
- Permitir cancelamentos com restrições
- Calcular automaticamente o valor mensal devido

O sistema foi desenvolvido como um MVP (Produto Mínimo Viável), priorizando a implementação das regras essenciais de negócio e integridade de dados.

---

# 2. Escopo do Sistema

## 2.1 O sistema permite:

- Visualizar salas disponíveis
- Agendar horários avulsos
- Agendar horários recorrentes
- Cancelar agendamentos avulsos
- Visualizar agendamentos ativos
- Visualizar histórico de agendamentos
- Consultar o valor mensal devido

## 2.2 Não faz parte do escopo:

- Autenticação de múltiplos usuários
- Controle de permissões
- Pagamentos reais
- Cancelamento completo de recorrências
- Notificações automáticas
- Integração com sistemas externos

---

# 3. Requisitos Funcionais

## RF01 – Visualizar Salas

O sistema deve permitir que o profissional visualize todas as salas disponíveis, exibindo:

- Nome da sala  
- Valor por hora  

---

## RF02 – Agendar Horário Avulso

O sistema deve permitir que o profissional realize um agendamento avulso informando:

- Sala  
- Data  
- Hora de início  
- Hora de fim  

O sistema deve:

- Validar que a data não esteja no passado
- Validar que a hora final seja maior que a hora inicial
- Verificar conflito de horário
- Registrar o agendamento com status **ATIVO**
- Exibir confirmação de sucesso ou mensagem de erro

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
- Registrar o padrão de recorrência
- Gerar automaticamente todas as ocorrências correspondentes
- Verificar conflito em cada ocorrência
- Cancelar toda a operação caso exista conflito
- Exibir confirmação de sucesso ou erro

---

## RF04 – Cancelar Agendamento Avulso

O sistema deve permitir cancelar apenas agendamentos do tipo **AVULSO**.

O sistema deve:

- Verificar se o agendamento está com status ATIVO
- Verificar se o cancelamento ocorre com pelo menos 24 horas de antecedência
- Alterar o status para **CANCELADO**
- Exibir confirmação ao usuário

---

## RF05 – Visualizar Meus Agendamentos

O sistema deve permitir que o profissional visualize seus agendamentos utilizando filtros:

- Avulsos ativos
- Recorrentes ativos
- Histórico (cancelados ou finalizados)

O sistema deve exibir:

- Nome da sala
- Período ou descrição do agendamento
- Status do agendamento

---

## RF06 – Consultar Valor Mensal

O sistema deve permitir consultar o valor mensal devido com base nos agendamentos ATIVOS.

O sistema deve:

- Permitir selecionar o mês desejado
- Calcular o total geral
- Calcular o total referente a agendamentos avulsos
- Calcular o total referente a agendamentos recorrentes
- Exibir os valores detalhados

---

## RF07 – Manter Histórico

O sistema deve manter armazenados:

- Agendamentos cancelados
- Agendamentos já finalizados

Esses registros devem estar disponíveis para consulta posterior.

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

- Constraints no banco de dados
- Triggers para bloqueio de conflito
- Triggers para regra de cancelamento
- Validações no backend
- Validações no frontend

---

## RNF05 – Desempenho

As consultas de listagem e cálculo mensal devem ser executadas em tempo adequado para uso acadêmico.

---

## RNF06 – Usabilidade

O sistema deve:

- Exibir mensagens claras de erro
- Utilizar modais para confirmação
- Utilizar notificações (toast) para feedback ao usuário
- Organizar as informações de forma clara

---

## RNF07 – MVP Acadêmico

O sistema deve atender aos requisitos mínimos definidos para a disciplina Projeto Integrado I, sem necessidade de autenticação ou controle multiusuário.

---

# 5. Regras de Negócio

## RN01 – Conflito de Horário

Não é permitido haver dois agendamentos com status ATIVO para a mesma sala com sobreposição de horário.

A validação deve ocorrer:

- No backend (função auxiliar)
- No banco de dados (trigger `fn_bloquear_conflito()`)

---

## RN02 – Cancelamento com 24 Horas

Cancelamentos são permitidos apenas:

- Para agendamentos do tipo AVULSO
- Com no mínimo 24 horas de antecedência

Regra implementada via trigger `fn_cancelamento_24h()`.

---

## RN03 – Cálculo de Valor

Valor mensal = (Horas Utilizadas) × (Valor da Sala)

O cálculo considera apenas agendamentos com status ATIVO.

---

## RN04 – Recorrência Atômica

Se qualquer ocorrência de uma recorrência gerar conflito de horário, toda a operação deve ser cancelada e nenhuma ocorrência deve ser registrada.

---

## RN05 – Validação de Datas

- Data inicial não pode estar no passado.
- Data final deve ser maior ou igual à data inicial.
- Hora final deve ser maior que hora inicial.

---

# 6. Tecnologias Utilizadas

- Python
- Flask
- PostgreSQL
- HTML
- CSS
- JavaScript
- Git e GitHub