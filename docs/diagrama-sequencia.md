# Diagrama de Sequência  
## Projeto 2 – Sistema de Gestão de Agendamento de Sublocação de Salas

O Diagrama de Sequência representa a interação entre os componentes do sistema ao longo do tempo, descrevendo a troca de mensagens para a realização de um caso de uso.

## Caso de Uso Representado
Agendar Horário Avulso

## Participantes
- Profissional
- Interface Web
- Backend (Flask)
- Banco de Dados (PostgreSQL)

## Sequência de Interações

1. O Profissional informa a sala, a data e o horário desejados.
2. A Interface Web envia a requisição de agendamento ao Backend.
3. O Backend recebe e valida os dados da requisição.
4. O Backend solicita ao Banco de Dados a inserção do horário reservado.
5. O Banco de Dados verifica conflitos de horário e regras de integridade.
6. O Banco de Dados retorna sucesso ou erro ao Backend.
7. O Backend retorna a resposta ao Profissional.
