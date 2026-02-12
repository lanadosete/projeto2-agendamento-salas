from flask import Flask, jsonify, request, render_template
from datetime import datetime, timedelta
from database.connection import get_connection

app = Flask(__name__)

# =========================
# FUNÇÃO AUXILIAR – CONFLITO
# =========================

def existe_conflito(cur, id_sala, inicio, fim):
    cur.execute("""
        SELECT 1
        FROM horario_reservado
        WHERE id_sala = %s
          AND status = 'ATIVO'
          AND %s < data_fim
          AND %s > data_inicio
        LIMIT 1;
    """, (id_sala, inicio, fim))
    return cur.fetchone() is not None

# =========================
# HOME
# =========================

@app.route("/")
def index():
    return render_template("index.html")

# =========================
# SALAS
# =========================

@app.route("/salas", methods=["GET"])
def listar_salas():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_sala, nome, valor_hora FROM sala ORDER BY id_sala;")
    salas = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id_sala": s[0], "nome": s[1], "valor_hora": float(s[2])}
        for s in salas
    ])

# =========================
# AGENDAMENTO AVULSO
# =========================

@app.route("/agendamentos/avulso", methods=["POST"])
def agendar_avulso():
    dados = request.get_json()

    try:
        inicio = datetime.fromisoformat(dados["inicio"])
        fim = datetime.fromisoformat(dados["fim"])
        agora = datetime.now()

        if inicio < agora:
            return jsonify({"erro": "Não é permitido agendar para data ou horário no passado."}), 400

        if fim <= inicio:
            return jsonify({"erro": "A hora final deve ser maior que a hora inicial."}), 400

        conn = get_connection()
        cur = conn.cursor()

        if existe_conflito(cur, dados["id_sala"], inicio, fim):
            return jsonify({"erro": "Já existe um agendamento para este horário."}), 400

        cur.execute("""
            INSERT INTO horario_reservado
            (id_profissional, id_sala, data_inicio, data_fim, tipo, status)
            VALUES (%s, %s, %s, %s, 'AVULSO', 'ATIVO');
        """, (
            dados["id_profissional"],
            dados["id_sala"],
            inicio,
            fim
        ))

        conn.commit()
        return jsonify({"mensagem": "Agendamento avulso realizado"}), 201

    except Exception as e:
        conn.rollback()
        mensagem = str(e)

        if hasattr(e, "pgerror") and e.pgerror:
            mensagem = e.pgerror.split("CONTEXT:")[0].strip()

        return jsonify({"erro": mensagem}), 400

    finally:
        cur.close()
        conn.close()

# =========================
# AGENDAMENTO RECORRENTE
# =========================

@app.route("/agendamentos/recorrente", methods=["POST"])
def agendar_recorrente():
    dados = request.get_json()

    id_profissional = dados["id_profissional"]
    id_sala = dados["id_sala"]
    data_inicio = datetime.fromisoformat(dados["data_inicio"])
    data_fim = datetime.fromisoformat(dados["data_fim"])

# Validação: data final não pode ser menor que inicial
    if data_fim.date() < data_inicio.date():
        return jsonify({
            "erro": "A data final da recorrência deve ser maior ou igual à data inicial."
        }), 400

    hora_inicio = dados["hora_inicio"]
    hora_fim = dados["hora_fim"]
    dias_semana = dados["dias_semana"]

    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if data_inicio < hoje:
        return jsonify({"erro": "A data inicial da recorrência não pode ser no passado."}), 400

    if not dias_semana:
        return jsonify({"erro": "Selecione pelo menos um dia da semana."}), 400

    if hora_fim <= hora_inicio:
        return jsonify({"erro": "A hora final deve ser maior que a hora inicial."}), 400

    conn = get_connection()
    cur = conn.cursor()
   
   
    dias_int = [int(d) for d in dias_semana]

    try:
        cur.execute("""
            INSERT INTO recorrencia
            (id_profissional, dia_semana, hora_inicio, hora_fim, data_inicio, data_fim)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_recorrencia;
        """, (
            id_profissional,
            dias_int,
            hora_inicio,
            hora_fim,
            data_inicio.date(),
            data_fim.date()
        ))
        id_recorrencia = cur.fetchone()[0]
        for dia in dias_semana:

            # cur.execute("""
            #     INSERT INTO recorrencia
            #     (id_profissional, dia_semana, hora_inicio, hora_fim, data_inicio, data_fim)
            #     VALUES (%s, %s, %s, %s, %s, %s)
            #     RETURNING id_recorrencia;
            # """, (
            #     id_profissional,
            #     dia,
            #     hora_inicio,
            #     hora_fim,
            #     data_inicio.date(),
            #     data_fim.date()
            # ))

            # id_recorrencia = cur.fetchone()[0]
            atual = data_inicio

            while atual.date() <= data_fim.date():

                # Python: 0=Seg, 1=Ter, ..., 6=Dom
                dia_python = atual.weekday()

                # Converter para padrão banco: 0=Dom, 1=Seg, ..., 6=Sáb
                dia_banco = (dia_python + 1) % 7

                if dia_banco == dia:

                    inicio_dt = atual.replace(
                        hour=int(hora_inicio[:2]),
                        minute=int(hora_inicio[3:])
                    )

                    fim_dt = atual.replace(
                        hour=int(hora_fim[:2]),
                        minute=int(hora_fim[3:])
                    )

                    # ✅ CORREÇÃO CRÍTICA: bloqueia conflito com AVULSO e RECORRENTE
                    if existe_conflito(cur, id_sala, inicio_dt, fim_dt):
                        conn.rollback()
                        return jsonify({
                            "erro": "Conflito de horário detectado em uma das ocorrências."
                        }), 400

                    cur.execute("""
                        INSERT INTO horario_reservado
                        (id_profissional, id_sala, data_inicio, data_fim, tipo, status, id_recorrencia)
                        VALUES (%s, %s, %s, %s, 'RECORRENTE', 'ATIVO', %s);
                    """, (
                        id_profissional,
                        id_sala,
                        inicio_dt,
                        fim_dt,
                        id_recorrencia
                    ))

                atual += timedelta(days=1)

        conn.commit()
        return jsonify({"mensagem": "Recorrência criada com sucesso"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 400

    finally:
        cur.close()
        conn.close()

# =========================
# LISTAR AGENDAMENTOS
# =========================

@app.route("/agendamentos", methods=["GET"])
def listar_agendamentos():
    filtro = request.args.get("filtro", "AVULSO")

    conn = get_connection()
    cur = conn.cursor()

    if filtro == "AVULSO":
        cur.execute("""
            SELECT hr.id_horario, s.nome, hr.data_inicio, hr.data_fim, hr.status
            FROM horario_reservado hr
            JOIN sala s ON s.id_sala = hr.id_sala
            WHERE hr.tipo = 'AVULSO'
              AND hr.status = 'ATIVO'
            ORDER BY hr.data_inicio DESC;
        """)
        dados = cur.fetchall()
        resultado = [{
            "id": d[0],
            "sala": d[1],
            "descricao": f"{d[2]} → {d[3]}",
            "status": d[4],
            "tipo": "AVULSO"
        } for d in dados]

    elif filtro == "RECORRENTE":
        cur.execute("""
            SELECT 
                r.id_recorrencia,
                s.nome,
                TO_CHAR(MIN(r.data_inicio), 'DD/MM/YYYY'),
                TO_CHAR(MAX(r.data_fim), 'DD/MM/YYYY'),
                r.hora_inicio,
                r.hora_fim,
                ARRAY(
                SELECT CASE num
                    WHEN 0 THEN 'Domingo'
                    WHEN 1 THEN 'Segunda-feira'
                    WHEN 2 THEN 'Terça-feira'
                    WHEN 3 THEN 'Quarta-feira'
                    WHEN 4 THEN 'Quinta-feira'
                    WHEN 5 THEN 'Sexta-feira'
                    WHEN 6 THEN 'Sábado'
                END
                FROM unnest(dia_semana) AS num
                ) AS dias,
                MIN(r.data_criacao) AS criado_em
            FROM recorrencia r
            JOIN horario_reservado hr 
                ON hr.id_recorrencia = r.id_recorrencia
            JOIN sala s 
                ON s.id_sala = hr.id_sala
            WHERE hr.status = 'ATIVO'
            GROUP BY 
                r.id_recorrencia,
                s.nome,
                r.hora_inicio,
                r.hora_fim
            ORDER BY MIN(r.data_criacao) DESC;
        """)

        dados = cur.fetchall()

        resultado = [{
            "id": d[0],
            "sala": d[1],
            "descricao": f"{d[2]} até {d[3]} | {d[4]}–{d[5]} | Dias: {' - '.join(d[6])}",
            "status": "ATIVO",
            "tipo": "RECORRENTE",
            "criado_em": d[7]
        } for d in dados]
        
    else:
            cur.execute("""
                SELECT DISTINCT
                    COALESCE(hr.id_recorrencia, hr.id_horario),
                    s.nome, hr.tipo, hr.status, hr.data_inicio, hr.data_fim
                FROM horario_reservado hr
                JOIN sala s ON s.id_sala = hr.id_sala
                WHERE hr.status = 'CANCELADO'
                OR hr.data_fim < NOW()
                ORDER BY hr.data_inicio DESC;
            """)
            dados = cur.fetchall()
            resultado = [{
                "id": d[0],
                "sala": d[1],
                "descricao": f"{d[4]} → {d[5]}",
                "status": d[3],
                "tipo": d[2]
            } for d in dados]

    cur.close()
    conn.close()
    return jsonify(resultado)

# =========================
# CANCELAR AGENDAMENTO
# =========================

@app.route("/agendamentos/cancelar", methods=["POST"])
def cancelar_agendamento():
    dados = request.get_json()
    id_horario = dados.get("id_horario")

    if not id_horario:
        return jsonify({"erro": "ID do agendamento não informado."}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE horario_reservado
            SET status = 'CANCELADO'
            WHERE id_horario = %s
              AND status = 'ATIVO'
              AND tipo = 'AVULSO';
        """, (id_horario,))

        if cur.rowcount == 0:
            return jsonify({"erro": "Agendamento não encontrado ou não pode ser cancelado."}), 400

        conn.commit()
        return jsonify({"mensagem": "Agendamento cancelado com sucesso."})

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e).split("\n")[0]}), 400

    finally:
        cur.close()
        conn.close()

# =========================
# VALOR MENSAL
# =========================

@app.route("/valor-mensal/detalhado", methods=["GET"])
def valor_mensal_detalhado():
    id_profissional = request.args.get("id_profissional")
    mes = request.args.get("mes")

    conn = get_connection()
    cur = conn.cursor()

    # TOTAL GERAL
    cur.execute("""
        SELECT
            SUM((EXTRACT(EPOCH FROM (hr.data_fim - hr.data_inicio)) / 3600) * s.valor_hora)
        FROM horario_reservado hr
        JOIN sala s ON s.id_sala = hr.id_sala
        WHERE hr.id_profissional = %s
          AND hr.status = 'ATIVO'
          AND TO_CHAR(hr.data_inicio, 'YYYY-MM') = %s;
    """, (id_profissional, mes))
    total_geral = cur.fetchone()[0] or 0

    # AVULSO
    cur.execute("""
        SELECT
            SUM((EXTRACT(EPOCH FROM (hr.data_fim - hr.data_inicio)) / 3600) * s.valor_hora)
        FROM horario_reservado hr
        JOIN sala s ON s.id_sala = hr.id_sala
        WHERE hr.id_profissional = %s
          AND hr.tipo = 'AVULSO'
          AND hr.status = 'ATIVO'
          AND TO_CHAR(hr.data_inicio, 'YYYY-MM') = %s;
    """, (id_profissional, mes))
    total_avulso = cur.fetchone()[0] or 0

    # RECORRENTE
    cur.execute("""
        SELECT
            SUM((EXTRACT(EPOCH FROM (hr.data_fim - hr.data_inicio)) / 3600) * s.valor_hora)
        FROM horario_reservado hr
        JOIN sala s ON s.id_sala = hr.id_sala
        WHERE hr.id_profissional = %s
          AND hr.tipo = 'RECORRENTE'
          AND hr.status = 'ATIVO'
          AND TO_CHAR(hr.data_inicio, 'YYYY-MM') = %s;
    """, (id_profissional, mes))
    total_recorrente = cur.fetchone()[0] or 0

    cur.close()
    conn.close()

    return jsonify({
        "total": float(total_geral),
        "avulso": float(total_avulso),
        "recorrente": float(total_recorrente)
    })

# =========================
# TELA DE AGENDAR
# =========================

@app.route("/agendar/<int:id_sala>")
def agendar_sala(id_sala):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_sala, nome, valor_hora FROM sala WHERE id_sala = %s;",
        (id_sala,)
    )
    sala = cur.fetchone()

    cur.close()
    conn.close()

    if not sala:
        return "Sala não encontrada", 404

    return render_template("agendar.html", sala={
        "id_sala": sala[0],
        "nome": sala[1],
        "valor_hora": float(sala[2])
    })

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5001)