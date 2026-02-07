# Diagrama de Classes  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Classes representa a estrutura estática do sistema, evidenciando as principais classes, seus atributos e os relacionamentos existentes entre elas.

## Classes Identificadas

### Classe: Sala
- id_sala
- nome
- valor_hora

### Classe: Profissional
- id_profissional
- nome
- email

### Classe: HorarioReservado
- id_horario
- data_inicio
- data_fim
- status
- tipo

### Classe: Recorrencia
- id_recorrencia
- tipo
- intervalo
- data_fim

## Relacionamentos

- Um Profissional pode possuir vários HorariosReservados.
- Uma Sala pode possuir vários HorariosReservados.
- Um HorarioReservado pode estar associado a uma Recorrencia.
