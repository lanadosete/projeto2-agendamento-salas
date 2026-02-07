from flask import Flask, jsonify, request, render_template
from database.connection import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/salas", methods=["GET"])
def listar_salas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_sala, nome, valor_hora FROM sala ORDER BY id_sala;")
    salas = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for s in salas:
        resultado.append({
            "id_sala": s[0],
            "nome": s[1],
            "valor_hora": float(s[2])
        })

    return jsonify(resultado)

from flask import request

@app.route("/salas/disponiveis", methods=["GET"])
def salas_disponiveis():
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    if not inicio or not fim:
        return jsonify({"erro": "Parâmetros 'inicio' e 'fim' são obrigatórios"}), 400

    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT s.id_sala, s.nome, s.valor_hora
    FROM sala s
    WHERE NOT EXISTS (
        SELECT 1
        FROM horario_reservado hr
        WHERE hr.id_sala = s.id_sala
          AND hr.status = 'ATIVO'
          AND %s < hr.data_fim
          AND %s > hr.data_inicio
    )
    ORDER BY s.id_sala;
    """

    cur.execute(sql, (inicio, fim))
    salas = cur.fetchall()

    cur.close()
    conn.close()

    resultado = []
    for s in salas:
        resultado.append({
            "id_sala": s[0],
            "nome": s[1],
            "valor_hora": float(s[2])
        })

    return jsonify(resultado)

@app.route("/agendamentos/avulso", methods=["POST"])
def agendar_avulso():
    dados = request.get_json()

    id_profissional = dados.get("id_profissional")
    id_sala = dados.get("id_sala")
    data_inicio = dados.get("data_inicio")
    data_fim = dados.get("data_fim")

    if not all([id_profissional, id_sala, data_inicio, data_fim]):
        return jsonify({"erro": "Dados obrigatórios não informados"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO horario_reservado
            (id_profissional, id_sala, data_inicio, data_fim, tipo)
            VALUES (%s, %s, %s, %s, 'AVULSO');
            """,
            (id_profissional, id_sala, data_inicio, data_fim)
        )
        conn.commit()
        return jsonify({"mensagem": "Agendamento realizado com sucesso"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 400

    finally:
        cur.close()
        conn.close()

@app.route("/agendamentos/cancelar", methods=["POST"])
def cancelar_agendamento():
    dados = request.get_json()
    id_horario = dados.get("id_horario")

    if not id_horario:
        return jsonify({"erro": "id_horario é obrigatório"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE horario_reservado
            SET status = 'CANCELADO'
            WHERE id_horario = %s;
            """,
            (id_horario,)
        )

        if cur.rowcount == 0:
            conn.rollback()
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        conn.commit()
        return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 400

    finally:
        cur.close()
        conn.close()

@app.route("/valor-mensal", methods=["GET"])
def consultar_valor_mensal():
    id_profissional = request.args.get("id_profissional")

    if not id_profissional:
        return jsonify({"erro": "id_profissional é obrigatório"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT mes, total_horas, total_valor
        FROM vw_valor_mensal
        WHERE id_profissional = %s
        ORDER BY mes;
        """,
        (id_profissional,)
    )

    dados = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for d in dados:
        resultado.append({
            "mes": str(d[0]),
            "total_horas": float(d[1]),
            "total_valor": float(d[2])
        })

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True, port=5001)