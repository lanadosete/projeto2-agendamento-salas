# Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

Projeto desenvolvido como **MVP (Produto Mínimo Viável)** para a disciplina **Projeto Integrado I**, do curso de **Sistemas de Informação – UFPA Campus Cametá**.

O sistema tem como objetivo permitir o agendamento de salas para sublocação, aplicando regras de negócio para evitar conflitos de horários e realizar o cálculo mensal de valores de forma simulada.

---

# Visão Geral

O sistema permite que um profissional:

- Visualize salas disponíveis
- Realize agendamentos avulsos
- Realize agendamentos recorrentes
- Cancele agendamentos avulsos respeitando antecedência mínima de 24 horas
- Visualize seus agendamentos (ativos e histórico)
- Consulte o valor mensal devido com base nas horas utilizadas

O projeto é composto por:

- Interface Web (Frontend – HTML, CSS, JavaScript)
- Backend em Python com Flask
- Banco de Dados PostgreSQL
- Regras de negócio implementadas no banco (Triggers e Constraints)

---

# Ator do Sistema

## Profissional

Usuário responsável por:

- Visualizar salas
- Realizar agendamentos
- Cancelar horários
- Consultar valores mensais

No MVP atual, o profissional é fixo (`id_profissional = 1`).

---

# Tecnologias Utilizadas

## Backend
- Python 3
- Flask

## Frontend
- HTML5
- CSS3
- JavaScript

## Banco de Dados
- PostgreSQL
- pgAdmin 4
- SQL (PostgreSQL)

---

# 🗄 Estrutura do Banco de Dados

O banco contém as seguintes estruturas:

## Tabelas

### profissional
- id_profissional (PK)
- nome
- email

### sala
- id_sala (PK)
- nome
- valor_hora

### recorrencia
- id_recorrencia (PK)
- id_profissional (FK)
- dia_semana (INTEGER[])
- hora_inicio (TIME)
- hora_fim (TIME)
- data_inicio (DATE)
- data_fim (DATE)

### horario_reservado
- id_horario (PK)
- id_profissional (FK)
- id_sala (FK)
- data_inicio (TIMESTAMPTZ)
- data_fim (TIMESTAMPTZ)
- tipo (AVULSO | RECORRENTE)
- status (ATIVO | CANCELADO)
- id_recorrencia (FK opcional)

---

## View

### vw_valor_mensal

Responsável por calcular:

- Total de horas utilizadas por mês
- Valor total devido com base no valor/hora da sala

---

# ⚙ Regras de Negócio

## 1. Bloqueio de Conflito de Horário

Não é permitido realizar dois agendamentos sobrepostos para a mesma sala.

Implementado por:

- Trigger `fn_bloquear_conflito`
- Validação adicional no backend

---

## 2. Cancelamento com 24h de Antecedência

O cancelamento é permitido apenas para agendamentos avulsos e deve respeitar antecedência mínima de 24 horas.

Implementado por:

- Trigger `fn_cancelamento_24h`

---

## 3. Agendamento Recorrente

Permite criar reservas periódicas com:

- Data inicial
- Data final
- Horário fixo
- Lista de dias da semana (armazenados em ARRAY)

O sistema gera automaticamente todas as ocorrências dentro do período definido.

Se qualquer ocorrência gerar conflito, toda a operação é cancelada (rollback).

---

## 4. Cálculo Mensal Simulado

O valor mensal é calculado com base em:

```
(total de horas utilizadas) × (valor/hora da sala)
```

Pode ser consultado via:

```sql
SELECT * FROM vw_valor_mensal;
```

Ou diretamente pela interface web.

---

# Salas do Sistema

As salas são fixas no MVP:

- Sala 1 – R$ 100,00/hora
- Sala 2 – R$ 120,00/hora

São inseridas automaticamente pelo script SQL.

---

# Execução do Projeto

## 1. Criar o Banco

Criar um banco chamado:

```
agendamento_salas
```

Executar o script SQL localizado em:

```
docs/sql/schema.sql
```

---

## 2. Criar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

## 3. Instalar Dependências

```bash
pip install flask psycopg2
```

---

## 4. Configurar Conexão

Editar o arquivo:

```
database/connection.py
```

Inserindo os dados corretos do PostgreSQL.

---

## 5. Executar o Sistema

```bash
python app.py
```

O sistema será iniciado em:

```
http://localhost:5001
```

---

# 📂 Estrutura do Projeto

```
├── app.py
├── database/
│   └── connection.py
├── templates/
│   ├── index.html
│   └── agendar.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/
├── docs/
│   ├── requisitos.md
│   ├── casos-de-uso.md
│   ├── der.md
│   ├── diagrama-classes.md
│   ├── diagrama-sequencia.md
│   ├── sql/
│   │   └── schema.sql
│   └── img-diagrams/
│       ├── diagrama-caso-de-uso.png
│       ├── diagrama-entidade-relacionamento.png
│       ├── diagrama-de-classes.png
│       └── diagrama-de-sequencia.png
└── README.md
```

---

# Documentação Incluída

O repositório contém:

- Documento de Requisitos
- Casos de Uso
- Diagrama de Caso de Uso
- Diagrama Entidade-Relacionamento (DER)
- Diagrama de Classes
- Diagrama de Sequência
- Script SQL completo
- README do projeto

---

# Limitações do MVP

- Não possui autenticação
- Profissional fixo (id = 1)
- Não realiza cobrança real
- Execução local
- Não possui controle de múltiplos usuários simultâneos

---

# Possíveis Evoluções Futuras

- Sistema de login e autenticação
- Cadastro dinâmico de profissionais
- Dashboard administrativo
- Deploy em ambiente de produção
- Integração com sistema de pagamento
- Controle de permissões
- API REST documentada

---

# Desenvolvedores

- Lana Lourrani  
- Leonardo Davi  
- Kildery Douglas  

---

# Considerações Finais

Este projeto foi desenvolvido como MVP acadêmico, com foco em:

- Modelagem correta de banco de dados
- Aplicação de regras de negócio via triggers
- Implementação de recorrência com geração automática de ocorrências
- Integração entre frontend, backend e banco de dados
- Simulação de cálculo financeiro mensal

O sistema não realiza cobranças reais, sendo apenas uma simulação para fins educacionais.