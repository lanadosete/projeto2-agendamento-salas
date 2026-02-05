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

if __name__ == "__main__":
    app.run(debug=True, port=5001)
