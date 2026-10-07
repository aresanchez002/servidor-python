import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend


# Ruta de prueba
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "success", "message": "Servidor activo y corriendo"})


# Ruta de API de ejemplo (obtener datos)
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(
        {
            "items": [
                {"id": 1, "nombre": "Elemento 1"},
                {"id": 2, "nombre": "Elemento 2"},
            ]
        }
    )


# Ruta de API de ejemplo (recibir datos)
@app.route("/api/data", methods=["POST"])
def post_data():
    data = request.get_json() or {}
    return jsonify(
        {"status": "creado", "recibido": data}
    ), 201


if __name__ == "__main__":
    # Render asigna dinámicamente un puerto en la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)