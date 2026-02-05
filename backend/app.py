from flask import Flask, jsonify
from database.connection import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return "Backend do Projeto 2 rodando"

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

if __name__ == "__main__":
    app.run(debug=True, port=5001)