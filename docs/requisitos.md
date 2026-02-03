# Documento de Requisitos  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

**Disciplina:** Projeto Integrado I  
**Curso:** Sistemas de Informação  
**Instituição:** UFPA – Campus Cametá  

---

## 1. Introdução

Este documento descreve os requisitos do Sistema de Gestão de Agendamento de Sublocação de Salas,
desenvolvido como Projeto 2 da disciplina Projeto Integrado I. O sistema tem como objetivo permitir
o controle de agendamentos de salas, aplicando regras de negócio para evitar conflitos de horários
e realizar o cálculo mensal de valores de forma simulada.

---

## 2. Requisitos Funcionais

**RF01** – O sistema deve permitir o cadastro e a visualização das salas disponíveis para sublocação.

**RF02** – O sistema deve permitir que o profissional visualize a disponibilidade de horários das salas.

**RF03** – O sistema deve permitir o agendamento de horários avulsos para uma sala específica.

**RF04** – O sistema deve permitir o agendamento de horários recorrentes para uma sala específica.

**RF05** – O sistema deve impedir o agendamento de horários conflitantes para a mesma sala.

**RF06** – O sistema deve permitir o cancelamento de agendamentos avulsos respeitando o prazo mínimo de 24 horas de antecedência.

**RF07** – O sistema deve calcular e exibir o valor total mensal devido pelo profissional com base nos horários utilizados.

---

## 3. Requisitos Não Funcionais

**RNF01** – O sistema deve utilizar o banco de dados PostgreSQL para armazenamento das informações.

**RNF02** – O backend do sistema deve ser desenvolvido utilizando a linguagem Python.

**RNF03** – O sistema deve possuir uma interface simples, priorizando a usabilidade e clareza das informações.

**RNF04** – O sistema deve ser desenvolvido como um MVP (Produto Mínimo Viável), conforme escopo definido para a disciplina Projeto Integrado I.

**RNF05** – O sistema não deve realizar cobranças reais, apenas simular o cálculo dos valores mensais.
