# Casos de Uso  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

---

## Ator Principal

**Profissional** – Usuário responsável por visualizar salas, realizar agendamentos, cancelar horários e consultar o valor mensal devido.

---

## Caso de Uso 1 – Visualizar Salas Disponíveis

**Descrição:** Permite ao profissional visualizar as salas disponíveis para sublocação.

**Ator:** Profissional

**Fluxo Principal:**
1. O profissional acessa o sistema.
2. O sistema exibe a lista de salas disponíveis.

---

## Caso de Uso 2 – Agendar Horário

**Descrição:** Permite ao profissional realizar o agendamento de um horário em uma sala específica.

**Ator:** Profissional

**Fluxo Principal:**
1. O profissional seleciona a sala desejada.
2. O profissional informa a data e o horário.
3. O sistema verifica conflitos de horário.
4. O sistema confirma o agendamento caso não haja conflito.

---

## Caso de Uso 3 – Cancelar Agendamento

**Descrição:** Permite ao profissional cancelar um agendamento previamente realizado.

**Ator:** Profissional

**Fluxo Principal:**
1. O profissional seleciona um agendamento.
2. O sistema verifica se o cancelamento respeita o prazo mínimo de 24 horas.
3. O sistema realiza o cancelamento quando permitido.

---

## Caso de Uso 4 – Consultar Valor Mensal

**Descrição:** Permite ao profissional consultar o valor total mensal calculado com base nos horários utilizados.

**Ator:** Profissional

**Fluxo Principal:**
1. O profissional solicita a consulta do valor mensal.
2. O sistema calcula o total com base nos agendamentos.
3. O sistema exibe o valor calculado.
