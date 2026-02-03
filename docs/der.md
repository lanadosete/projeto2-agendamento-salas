# Diagrama Entidade-Relacionamento (DER)  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

---

## Identificação das Entidades

O sistema proposto necessita armazenar informações referentes às salas disponíveis,
aos profissionais que realizam agendamentos e aos horários agendados. Para isso,
foram identificadas as seguintes entidades principais.

### Entidade: Sala
Representa as salas disponíveis para sublocação no sistema.

### Entidade: Profissional
Representa o profissional que utiliza o sistema para realizar agendamentos.

### Entidade: HorarioReservado
Representa um horário específico reservado por um profissional em uma sala,
contendo informações de data e horário.

### Entidade: Recorrencia
Representa o padrão de repetição associado a um ou mais horários reservados,
permitindo a criação de reservas recorrentes.
