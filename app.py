import os
import sqlite3
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = "hello_kitty_makeup.db"


def init_db():
    """Inicializa la base de datos SQLite y crea las tablas con datos iniciales."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabla de Productos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen TEXT NOT NULL
        )
    """
    )

    # Tabla de Ventas (para la gráfica)
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

    # Insertar datos de prueba si está vacía
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            (
                "Labial Matte Kawaii",
                "Labios",
                250.0,
                "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400",
            ),
            (
                "Paleta Hello Kitty Nude",
                "Ojos",
                480.0,
                "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400",
            ),
            (
                "Base Glow Rosada",
                "Rostro",
                390.0,
                "https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=400",
            ),
            (
                "Set Brochas Kitty Pink",
                "Accesorios",
                320.0,
                "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400",
            ),
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, categoria, precio, imagen) VALUES (?, ?, ?, ?)",
            productos_iniciales,
        )

        ventas_iniciales = [(1, 150), (2, 90), (3, 60), (4, 120)]
        cursor.executemany(
            "INSERT INTO ventas (producto_id, unidades_vendidas) VALUES (?, ?)",
            ventas_iniciales,
        )

    conn.commit()
    conn.close()


# Inicializar la Base de Datos
init_db()

# --- Plantilla HTML Kawaii Hello Kitty ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello Kitty Beauty Store & Analytics 🎀</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Fredoka', sans-serif; }
        body { background-color: #fff0f5; color: #5a3a41; }
        header { background: linear-gradient(135deg, #ffb6c1, #ff69b4); color: white; padding: 30px 20px; text-align: center; position: relative; border-bottom: 5px solid #ff1493; }
        header h1 { font-size: 2.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: center; gap: 15px; }
        .kitty-logo { width: 65px; height: auto; filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.2)); }
        header p { font-size: 1.2rem; margin-top: 5px; opacity: 0.95; }
        .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
        .section-title { font-size: 1.8rem; color: #d63384; margin-bottom: 20px; text-align: center; display: flex; align-items: center; justify-content: center; gap: 10px; }
        
        /* Gráfica Card */
        .chart-card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 8px 20px rgba(255,105,180,0.15); border: 2px solid #ffb6c1; margin-bottom: 40px; }
        
        /* Grid de Productos */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; }
        .card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 8px 15px rgba(0,0,0,0.06); border: 2px solid #ffe4e1; transition: transform 0.3s, box-shadow 0.3s; text-align: center; padding-bottom: 20px; position: relative; }
        .card:hover { transform: translateY(-7px); box-shadow: 0 12px 20px rgba(255,105,180,0.25); }
        .card img { width: 100%; height: 200px; object-fit: cover; }
        .card h3 { color: #ff1493; font-size: 1.3rem; margin: 15px 0 5px; }
        .card .badge { background: #ffe4e1; color: #d63384; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .price { font-size: 1.3rem; font-weight: bold; color: #5a3a41; margin-bottom: 15px; }
        .btn { background: #ff69b4; color: white; border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; font-size: 1rem; font-weight: 600; box-shadow: 0 4px 10px rgba(255,105,180,0.3); transition: background 0.2s; }
        .btn:hover { background: #ff1493; }
        footer { text-align: center; padding: 30px; color: #ff69b4; margin-top: 50px; font-weight: 600; }
    </style>
</head>
<body>

    <header>
        <h1>
            <img class="kitty-logo" src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" alt="Hello Kitty">
            Hello Kitty Makeup Store
            <img class="kitty-logo" src="https://upload.wikimedia.org/wikipedia/en/0/05/Hello_kitty_character_art.png" alt="Hello Kitty">
        </h1>
        <p>Maquillaje Kawaii & Base de Datos con Estadísticas 🎀</p>
    </header>

    <div class="container">
        <!-- Sección de Gráfica con Porcentajes -->
        <div class="chart-card">
            <h2 class="section-title">📊 Porcentaje de Ventas por Producto</h2>
            <canvas id="salesChart" height="120"></canvas>
        </div>

        <!-- Catálogo de Productos -->
        <h2 class="section-title">✨ Catálogo de Productos Disponibles</h2>
        <div class="grid" id="productGrid">
            <!-- Cargado dinámicamente con JS desde SQLite -->
        </div>
    </div>

    <footer>
        <p>🎀 Hello Kitty Beauty App — Creado con Python, Flask & SQLite 🎀</p>
    </footer>

    <script>
        // Cargar Estadísticas y Dibujar Gráfica de Barras con Porcentajes
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
                            'rgba(255, 105, 180, 0.75)',
                            'rgba(255, 182, 193, 0.85)',
                            'rgba(255, 20, 147, 0.75)',
                            'rgba(218, 112, 214, 0.75)'
                        ],
                        borderColor: [
                            '#ff1493',
                            '#ff69b4',
                            '#c71585',
                            '#ba55d3'
                        ],
                        borderWidth: 2,
                        borderRadius: 12
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

        // Cargar Productos desde la Base de Datos SQLite
        async function loadProducts() {
            const res = await fetch('/api/productos');
            const productos = await res.json();
            const grid = document.getElementById('productGrid');
            grid.innerHTML = '';

            productos.forEach(prod => {
                grid.innerHTML += `
                    <div class="card">
                        <img src="${prod.imagen}" alt="${prod.nombre}">
                        <h3>${prod.nombre}</h3>
                        <span class="badge">${prod.categoria}</span>
                        <div class="price">$${prod.precio.toFixed(2)} MXN</div>
                        <button class="btn">Comprar ✨</button>
                    </div>
                `;
            });
        }

        loadChart();
        loadProducts();
    </script>
</body>
</html>
"""


# --- RUTAS DE FLASK ---


@app.route("/", methods=["GET"])
def home():
    """Ruta principal que renderiza la página web."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/productos", methods=["GET"])
def get_productos():
    """Obtiene los productos desde SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, categoria, precio, imagen FROM productos")
    filas = cursor.fetchall()
    conn.close()

    productos = [
        {
            "id": f[0],
            "nombre": f[1],
            "categoria": f[2],
            "precio": f[3],
            "imagen": f[4],
        }
        for f in filas
    ]
    return jsonify(productos)


@app.route("/api/estadisticas", methods=["GET"])
def get_estadisticas():
    """Calcula las ventas y devuelve los porcentajes de cada producto."""
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