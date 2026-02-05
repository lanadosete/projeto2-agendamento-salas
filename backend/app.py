from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Backend do Projeto 2 rodando"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
