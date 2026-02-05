# Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

Projeto desenvolvido como MVP (Produto Mínimo Viável) para a disciplina Projeto Integrado I do curso de Sistemas de Informação da UFPA – Campus Cametá.

O sistema tem como objetivo permitir o agendamento de salas para sublocação, aplicando regras de negócio para evitar conflitos de horários e realizar o cálculo mensal de valores de forma simulada.

## Funcionalidades do Sistema

- Visualização das salas disponíveis
- Agendamento de horários avulsos
- Agendamento de horários recorrentes
- Cancelamento de agendamentos avulsos com antecedência mínima de 24 horas
- Consulta do valor mensal devido com base nos horários utilizados (simulado)

## Ator do Sistema

- Profissional: usuário responsável por visualizar salas, realizar agendamentos, cancelar horários e consultar o valor mensal.

## Tecnologias Utilizadas

- PostgreSQL
- pgAdmin 4
- SQL (PostgreSQL)

Não foi utilizada API ou interface gráfica neste MVP, conforme escopo do Projeto 2.

## Banco de Dados (PostgreSQL)

### Pré-requisitos

- PostgreSQL instalado
- pgAdmin 4

### Criação do banco e das tabelas

1. Abra o pgAdmin 4
2. Conecte-se ao servidor PostgreSQL
3. Crie um banco de dados com o nome:

agendamento_salas

4. Selecione o banco criado
5. Clique em Ferramenta de Consulta
6. Execute o script SQL disponível em:

docs/sql/schema.sql

Após a execução, serão criadas as seguintes tabelas:
- profissional
- sala
- recorrencia
- horario_reservado

E a view:
- vw_valor_mensal

## Salas do Sistema

As salas do sistema são fixas, conforme o escopo do projeto:
- Sala 1
- Sala 2

Essas salas são inseridas automaticamente pelo script SQL.

Para conferência:
SELECT * FROM sala;

## Regras de Negócio Implementadas

- Bloqueio de conflito de horário: não é permitido realizar dois agendamentos sobrepostos para a mesma sala.
- Cancelamento de agendamento avulso: permitido apenas com antecedência mínima de 24 horas.
- Cálculo mensal simulado: o valor mensal é calculado com base no total de horas utilizadas e no valor/hora da sala.

As regras de negócio são implementadas diretamente no banco de dados, utilizando triggers e views.

## Consulta do Valor Mensal

Para consultar o valor mensal devido por um profissional:
SELECT * FROM vw_valor_mensal;

A consulta retorna o mês de referência, o total de horas utilizadas e o valor total calculado (simulado).

## Documentação do Projeto

O repositório contém:
- Documento de requisitos
- Casos de uso
- Diagrama de caso de uso
- Diagrama Entidade-Relacionamento (DER)
- Script SQL do banco de dados

Todos os artefatos seguem rigorosamente o escopo definido para o Projeto 2 – Projeto Integrado I.

## Observações Finais

Este projeto foi desenvolvido como MVP, não realizando cobranças reais e não possuindo interface gráfica ou API no momento.

Como evolução futura, está prevista a criação de uma interface gráfica ou web para interação com o sistema.

