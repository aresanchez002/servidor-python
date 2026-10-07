import os
import sqlite3
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = "arelly_cosmetics_hk_v3.db"

# URL de la imagen completa generada
IMAGE_URL = "watermarked_img_2698944802837133687.jpg"


def init_db():
    """Inicializa la base de datos SQLite con los 5 productos y posiciones CSS de imagen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen TEXT NOT NULL,
            posicion_css TEXT NOT NULL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            unidades_vendidas INTEGER NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """
    )

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            (
                "Labial Matte Hello Kitty Edition",
                "Labios",
                240.0,
                IMAGE_URL,
                "0% 80%",
            ),
            (
                "Paleta de Sombras Hello Kitty Pink",
                "Ojos & Rostro",
                580.0,
                IMAGE_URL,
                "45% 70%",
            ),
            (
                "Set de Brochas Edición Hello Kitty",
                "Accesorios",
                420.0,
                IMAGE_URL,
                "25% 10%",
            ),
            (
                "Rubor Sostenible Hello Kitty Rose",
                "Mejillas",
                290.0,
                IMAGE_URL,
                "85% 15%",
            ),
            (
                "Iluminador Diamond Hello Kitty Shine",
                "Rostro",
                340.0,
                IMAGE_URL,
                "95% 85%",
            ),
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, categoria, precio, imagen, posicion_css) VALUES (?, ?, ?, ?, ?)",
            productos_iniciales,
        )

        ventas_iniciales = [(1, 160), (2, 110), (3, 125), (4, 90), (5, 80)]
        cursor.executemany(
            "INSERT INTO ventas (producto_id, unidades_vendidas) VALUES (?, ?)",
            ventas_iniciales,
        )

    conn.commit()
    conn.close()


init_db()

# --- Plantilla HTML Kawaii Hello Kitty ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arelly Cosmetics 🎀 - Hello Kitty Edition</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Fredoka', sans-serif; }
        body { background-color: #fff0f5; color: #5a3a41; }
        header { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #d63384; padding: 35px 20px; text-align: center; border-bottom: 5px solid #ff69b4; position: relative; }
        header h1 { font-size: 2.8rem; text-shadow: 1px 1px 2px rgba(255,255,255,0.8); display: flex; align-items: center; justify-content: center; gap: 15px; }
        .kitty-logo { width: 65px; height: auto; filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.15)); }
        header p { font-size: 1.25rem; margin-top: 5px; color: #b8256f; font-weight: 600; }
        .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
        .section-title { font-size: 1.8rem; color: #d63384; margin-bottom: 25px; text-align: center; display: flex; align-items: center; justify-content: center; gap: 10px; }
        
        /* Grid de Productos */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 50px; }
        .card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 8px 15px rgba(0,0,0,0.06); border: 2px solid #ffe4e1; transition: transform 0.3s, box-shadow 0.3s; text-align: center; padding-bottom: 20px; position: relative; }
        .card:hover { transform: translateY(-7px); box-shadow: 0 12px 20px rgba(255,105,180,0.25); }
        
        /* Formato e imagen recortada enfocado en cada producto */
        .img-container { width: 100%; height: 200px; overflow: hidden; position: relative; }
        .card img.prod-img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.6); }
        
        .card h3 { color: #ff1493; font-size: 1.15rem; margin: 12px 10px 5px; }
        .card .badge { background: #ffe4e1; color: #d63384; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; display: inline-block; margin-bottom: 8px; }
        .sales-info { font-size: 0.9rem; color: #e83e8c; font-weight: bold; background: #fff0f5; padding: 5px 10px; margin: 0 15px 10px; border-radius: 10px; }
        .price { font-size: 1.25rem; font-weight: bold; color: #5a3a41; margin-bottom: 12px; }
        .btn { background: #ff69b4; color: white; border: none; padding: 8px 18px; border-radius: 25px; cursor: pointer; font-size: 0.95rem; font-weight: 600; box-shadow: 0 4px 10px rgba(255,105,180,0.3); transition: background 0.2s; }
        .btn:hover { background: #ff1493; }
        .kitty-corner { position: absolute; top: 10px; right: 10px; width: 35px; z-index: 2; filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); }

        /* Contenedor de la Gráfica */
        .chart-card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 8px 20px rgba(255,105,180,0.15); border: 2px solid #ffb6c1; margin-bottom: 40px; }
        
        footer { text-align: center; padding: 30px; color: #ff69b4; margin-top: 50px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 10px; }
    </style>
</head>
<body>

    <header>
        <h1>
            <img class="kitty-logo" src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" alt="Hello Kitty">
            Arelly Cosmetics
            <img class="kitty-logo" src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" alt="Hello Kitty">
        </h1>
        <p>🎀 Colección Especial Hello Kitty 🎀</p>
    </header>

    <div class="container">
        <!-- 1. Catálogo de Productos con Imagen Distribuida -->
        <h2 class="section-title">
            <img src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" style="width: 35px;" alt="HK">
            Productos en Venta (Hello Kitty Edition)
            <img src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" style="width: 35px;" alt="HK">
        </h2>
        <div class="grid" id="productGrid"></div>

        <!-- 2. Gráfica de Porcentajes -->
        <div class="chart-card">
            <h2 class="section-title">
                📊 Porcentaje de Ventas de Cada Producto
            </h2>
            <canvas id="salesChart" height="120"></canvas>
        </div>
    </div>

    <footer>
        <img src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" style="width: 30px;" alt="HK">
        <span>Arelly Cosmetics App — Creado con Python, Flask & SQLite</span>
        <img src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" style="width: 30px;" alt="HK">
    </footer>

    <script>
        async function loadProducts() {
            const res = await fetch('/api/productos');
            const productos = await res.json();
            const grid = document.getElementById('productGrid');
            grid.innerHTML = '';

            productos.forEach(prod => {
                grid.innerHTML += `
                    <div class="card">
                        <img class="kitty-corner" src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" alt="HK">
                        <div class="img-container">
                            <img class="prod-img" src="${prod.imagen}" style="object-position: ${prod.posicion_css};" alt="${prod.nombre}">
                        </div>
                        <h3>${prod.nombre}</h3>
                        <span class="badge">${prod.categoria}</span>
                        <div class="sales-info">🛍️ Vendidos: ${prod.unidades_vendidas} uds.</div>
                        <div class="price">$${prod.precio.toFixed(2)} MXN</div>
                        <button class="btn">Comprar ✨</button>
                    </div>
                `;
            });
        }

        async function loadChart() {
            const res = await fetch('/api/estadisticas');
            const data = await res.json();

            const ctx = document.getElementById('salesChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Porcentaje de Ventas (%)',
                        data: data.porcentajes,
                        backgroundColor: [
                            'rgba(255, 105, 180, 0.8)',
                            'rgba(255, 182, 193, 0.9)',
                            'rgba(255, 20, 147, 0.8)',
                            'rgba(218, 112, 214, 0.8)',
                            'rgba(255, 160, 122, 0.8)'
                        ],
                        borderColor: [
                            '#ff1493',
                            '#ff69b4',
                            '#c71585',
                            '#ba55d3',
                            '#ff6347'
                        ],
                        borderWidth: 2,
                        borderRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw + '% del total de ventas';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) { return value + '%'; }
                            }
                        }
                    }
                }
            });
        }

        loadProducts();
        loadChart();
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/productos", methods=["GET"])
def get_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.nombre, p.categoria, p.precio, p.imagen, p.posicion_css, COALESCE(SUM(v.unidades_vendidas), 0)
        FROM productos p
        LEFT JOIN ventas v ON p.id = v.producto_id
        GROUP BY p.id
    """
    )
    filas = cursor.fetchall()
    conn.close()

    productos = [
        {
            "id": f[0],
            "nombre": f[1],
            "categoria": f[2],
            "precio": f[3],
            "imagen": f[4],
            "posicion_css": f[5],
            "unidades_vendidas": f[6],
        }
        for f in filas
    ]
    return jsonify(productos)


@app.route("/api/estadisticas", methods=["GET"])
def get_estadisticas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.nombre, SUM(v.unidades_vendidas)
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        GROUP BY p.id
    """
    )
    datos = cursor.fetchall()
    conn.close()

    total_unidades = sum(d[1] for d in datos) if datos else 1

    labels = [d[0] for d in datos]
    porcentajes = [round((d[1] / total_unidades) * 100, 1) for d in datos]

    return jsonify({"labels": labels, "porcentajes": porcentajes})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)