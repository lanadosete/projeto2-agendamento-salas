-- Projeto 2 (MVP) – Sistema de Gestão de Agendamento de Sublocação de Salas
-- Banco: PostgreSQL
-- Entidades: Profissional, Sala, HorarioReservado, Recorrencia
-- Regras: impedir conflitos (mesma sala e mesmo horário), cancelar avulso até 24h antes, cálculo mensal simulado

-- =========================
-- 1) Tabelas principais
-- =========================

CREATE TABLE IF NOT EXISTS profissional (
  id_profissional BIGSERIAL PRIMARY KEY,
  nome            VARCHAR(120) NOT NULL,
  email           VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sala (
  id_sala     BIGSERIAL PRIMARY KEY,
  nome        VARCHAR(50) NOT NULL UNIQUE,
  valor_hora  NUMERIC(10,2) NOT NULL CHECK (valor_hora >= 0)
);

-- Recorrência (padrão de repetição)
-- dia_semana: 0=domingo ... 6=sábado
CREATE TABLE IF NOT EXISTS recorrencia (
  id_recorrencia BIGSERIAL PRIMARY KEY,
  dia_semana     SMALLINT NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),
  hora_inicio    TIME NOT NULL,
  hora_fim       TIME NOT NULL,
  data_inicio    DATE NOT NULL,
  data_fim       DATE NOT NULL,
  CHECK (hora_fim > hora_inicio),
  CHECK (data_fim >= data_inicio)
);

-- Horário reservado (avulso ou recorrente)
CREATE TABLE IF NOT EXISTS horario_reservado (
  id_horario      BIGSERIAL PRIMARY KEY,
  id_profissional BIGINT NOT NULL REFERENCES profissional(id_profissional),
  id_sala         BIGINT NOT NULL REFERENCES sala(id_sala),

  data_inicio     TIMESTAMPTZ NOT NULL,
  data_fim        TIMESTAMPTZ NOT NULL,

  tipo            VARCHAR(12) NOT NULL CHECK (tipo IN ('AVULSO', 'RECORRENTE')),
  status          VARCHAR(12) NOT NULL DEFAULT 'ATIVO' CHECK (status IN ('ATIVO', 'CANCELADO')),

  id_recorrencia  BIGINT NULL REFERENCES recorrencia(id_recorrencia),

  CHECK (data_fim > data_inicio),

  -- Se tiver recorrencia_id, o tipo deve ser RECORRENTE; se não tiver, deve ser AVULSO
  CHECK (
    (id_recorrencia IS NULL AND tipo = 'AVULSO')
    OR
    (id_recorrencia IS NOT NULL AND tipo = 'RECORRENTE')
  )
);

-- =========================
-- 2) Regra: Impedir conflito de horário (mesma sala, mesmo horário)
-- =========================
-- Implementação: trigger que bloqueia sobreposição de intervalos na mesma sala, considerando apenas status ATIVO.

CREATE OR REPLACE FUNCTION fn_bloquear_conflito()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'ATIVO' THEN
    IF EXISTS (
      SELECT 1
      FROM horario_reservado hr
      WHERE hr.id_sala = NEW.id_sala
        AND hr.status = 'ATIVO'
        AND hr.id_horario <> COALESCE(NEW.id_horario, -1)
        -- sobreposição de intervalos: (inicio < outro_fim) e (fim > outro_inicio)
        AND NEW.data_inicio < hr.data_fim
        AND NEW.data_fim > hr.data_inicio
    ) THEN
      RAISE EXCEPTION 'Conflito: já existe reserva ativa para esta sala no horário informado.';
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_bloquear_conflito_ins ON horario_reservado;
DROP TRIGGER IF EXISTS trg_bloquear_conflito_upd ON horario_reservado;

CREATE TRIGGER trg_bloquear_conflito_ins
BEFORE INSERT ON horario_reservado
FOR EACH ROW
EXECUTE FUNCTION fn_bloquear_conflito();

CREATE TRIGGER trg_bloquear_conflito_upd
BEFORE UPDATE OF id_sala, data_inicio, data_fim, status ON horario_reservado
FOR EACH ROW
EXECUTE FUNCTION fn_bloquear_conflito();

-- =========================
-- 3) Regra: Cancelamento de AVULSO somente até 24h antes
-- =========================
-- Implementação: trigger valida quando status mudar para CANCELADO.

CREATE OR REPLACE FUNCTION fn_cancelamento_24h()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'CANCELADO' AND OLD.status <> 'CANCELADO' THEN

    IF OLD.tipo <> 'AVULSO' THEN
      RAISE EXCEPTION 'Cancelamento permitido apenas para agendamentos avulsos no MVP.';
    END IF;

    IF NOW() > (OLD.data_inicio - INTERVAL '24 hours') THEN
      RAISE EXCEPTION 'Cancelamento não permitido: precisa de 24 horas de antecedência.';
    END IF;

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_cancelamento_24h ON horario_reservado;

CREATE TRIGGER trg_cancelamento_24h
BEFORE UPDATE OF status ON horario_reservado
FOR EACH ROW
EXECUTE FUNCTION fn_cancelamento_24h();

-- =========================
-- 4) Salas fixas do MVP: Sala 1 e Sala 2
-- =========================

INSERT INTO sala (nome, valor_hora)
VALUES
  ('Sala 1', 100.00),
  ('Sala 2', 120.00)
ON CONFLICT (nome) DO NOTHING;

-- =========================
-- 5) Cálculo mensal simulado (exibição): total de horas e total em R$
-- =========================

CREATE OR REPLACE VIEW vw_valor_mensal AS
SELECT
  hr.id_profissional,
  DATE_TRUNC('month', hr.data_inicio) AS mes,
  SUM(EXTRACT(EPOCH FROM (hr.data_fim - hr.data_inicio)) / 3600.0) AS total_horas,
  SUM((EXTRACT(EPOCH FROM (hr.data_fim - hr.data_inicio)) / 3600.0) * s.valor_hora) AS total_valor
FROM horario_reservado hr
JOIN sala s ON s.id_sala = hr.id_sala
WHERE hr.status = 'ATIVO'
GROUP BY hr.id_profissional, DATE_TRUNC('month', hr.data_inicio);
