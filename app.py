from flask import Flask, request, redirect, session, render_template_string
from flask_cors import CORS
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
CORS(app)

# ==========================================
# AURE PARFUMS - CATALOGO
# ==========================================

perfumes = [
    {
        "id": 1,
        "nombre": "Auré Rose",
        "tipo": "Floral",
        "precio": 850,
        "descripcion": "Un aroma delicado, romantico y femenino.",
        "imagen": "https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 2,
        "nombre": "Auré Noir",
        "tipo": "Amaderado",
        "precio": 950,
        "descripcion": "Elegancia intensa con notas sofisticadas.",
        "imagen": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 3,
        "nombre": "Auré Bloom",
        "tipo": "Floral",
        "precio": 780,
        "descripcion": "Flores frescas para iluminar tu dia.",
        "imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 4,
        "nombre": "Auré Éclat",
        "tipo": "Citrico",
        "precio": 720,
        "descripcion": "Una fragancia fresca, luminosa y ligera.",
        "imagen": "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 5,
        "nombre": "Auré Velvet",
        "tipo": "Oriental",
        "precio": 900,
        "descripcion": "Un aroma envolvente para ocasiones especiales.",
        "imagen": "https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 6,
        "nombre": "Auré Divine",
        "tipo": "Floral",
        "precio": 820,
        "descripcion": "Suavidad y distincion en cada gota.",
        "imagen": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 7,
        "nombre": "Auré Terra",
        "tipo": "Amaderado",
        "precio": 880,
        "descripcion": "Notas calidas inspiradas en la naturaleza.",
        "imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=700&q=85"
    },
    {
        "id": 8,
        "nombre": "Auré Lumière",
        "tipo": "Citrico",
        "precio": 760,
        "descripcion": "Frescura y luz para todos los dias.",
        "imagen": "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=700&q=85"
    }
]

# ==========================================
# DISENO GENERAL: TODO EN UN SOLO ARCHIVO
# ==========================================

ESTILO = """
<style>
:root {
    --rosa: #f2dce3;
    --rosa-claro: #fff8fa;
    --rosa-fuerte: #b66f86;
    --crema: #fcf8f2;
    --negro: #211c1e;
    --dorado: #b99a67;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    background: var(--crema);
    color: var(--negro);
    font-family: Arial, sans-serif;
}

a { color: inherit; text-decoration: none; }

header {
    background: rgba(255, 250, 250, .97);
    padding: 16px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    border-bottom: 1px solid #eadce0;
}

.logo {
    font-family: Georgia, serif;
    font-size: 34px;
    color: #855266;
    margin: 0;
    letter-spacing: 1px;
}

.logo small {
    display: block;
    text-align: center;
    font: 10px Arial, sans-serif;
    letter-spacing: 7px;
    margin-top: -2px;
}

nav {
    display: flex;
    align-items: center;
    gap: 24px;
    font-size: 14px;
}

nav a:hover { color: var(--rosa-fuerte); }

.hero {
    min-height: 340px;
    padding: 55px 7%;
    display: flex;
    align-items: center;
    background:
        linear-gradient(90deg, rgba(245,219,225,.96), rgba(245,219,225,.45)),
        url('https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=1600&q=90')
        center 48% / cover;
}

.hero-text { max-width: 510px; }

.etiqueta {
    color: #8e586b;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: bold;
}

.hero h2 {
    font: 46px/1.12 Georgia, serif;
    margin: 15px 0;
}

.hero p {
    max-width: 390px;
    line-height: 1.7;
}

.boton {
    display: inline-block;
    background: var(--negro);
    color: white;
    border: 0;
    border-radius: 30px;
    padding: 13px 23px;
    margin-top: 12px;
    cursor: pointer;
    font-size: 13px;
}

.boton:hover { background: #805467; }

.beneficios {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background: #fffafb;
    padding: 20px 5%;
    text-align: center;
    gap: 15px;
    border-bottom: 1px solid #f0e2e5;
}

.beneficios strong { display: block; font-size: 13px; }
.beneficios span { font-size: 12px; color: #777; }

.seccion {
    max-width: 1200px;
    margin: auto;
    padding: 42px 24px;
}

.titulo {
    text-align: center;
    font: 32px Georgia, serif;
    margin: 0 0 12px;
}

.subtitulo {
    text-align: center;
    color: #777;
    margin: 0 0 28px;
    font-size: 14px;
}

.catalogo {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
}

.tarjeta {
    background: white;
    border: 1px solid #eee1e4;
    border-radius: 10px;
    overflow: hidden;
    transition: transform .2s, box-shadow .2s;
}

.tarjeta:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px #6b455012;
}

.tarjeta img {
    width: 100%;
    height: 210px;
    object-fit: cover;
    display: block;
    background: var(--rosa);
}

.info { padding: 16px; }

.info h3 {
    margin: 0 0 8px;
    font: 21px Georgia, serif;
}

.tipo {
    color: #98677b;
    font-size: 12px;
}

.descripcion {
    color: #777;
    font-size: 13px;
    line-height: 1.5;
    min-height: 38px;
}

.precio {
    font-weight: bold;
    margin: 12px 0;
}

.info .boton {
    width: 100%;
    text-align: center;
    padding: 12px 8px;
}

.filtros {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 24px 0;
}

.filtros input, .filtros select, .campo {
    padding: 13px;
    border: 1px solid #e1d4d8;
    border-radius: 8px;
    background: white;
    font-size: 14px;
}

.filtros input { width: min(400px, 100%); }

.panel {
    max-width: 760px;
    margin: 35px auto;
    padding: 28px;
    background: white;
    border: 1px solid #eee0e5;
    border-radius: 14px;
}

.fila {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
}

.fila img {
    width: 85px;
    height: 85px;
    object-fit: cover;
    border-radius: 8px;
}

.fila-info { flex: 1; }
.fila h3 { margin: 0 0 8px; }

.eliminar {
    color: #a54f69;
    font-size: 13px;
}

.total {
    text-align: right;
    font-size: 23px;
    font-weight: bold;
    margin: 24px 0;
}

.campo {
    display: block;
    width: 100%;
    margin: 12px 0;
}

footer {
    background: #f0dfe4;
    text-align: center;
    padding: 28px 15px;
    font-size: 13px;
    line-height: 1.8;
}

.vacio { text-align: center; padding: 40px 10px; }

.oculto { display: none !important; }

@media (max-width: 850px) {
    .catalogo { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hero h2 { font-size: 36px; }
}

@media (max-width: 500px) {
    header { justify-content: center; }
    nav { gap: 15px; }
    .hero { padding: 40px 7%; }
    .hero h2 { font-size: 32px; }
    .beneficios { grid-template-columns: 1fr; }
    .catalogo { gap: 12px; }
    .tarjeta img { height: 155px; }
    .info { padding: 12px; }
    .info h3 { font-size: 18px; }
    .panel { padding: 18px; }
}
</style>
"""

# ==========================================
# PLANTILLA COMPARTIDA
# ==========================================

PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Descubre tu próxima fragancia en Auré Parfums.">
    <title>{{ titulo }} | Auré Parfums</title>
    """ + ESTILO + """
</head>
<body>
<header>
    <a href="/" aria-label="Auré Parfums, inicio">
        <h1 class="logo">Auré<small>PARFUMS</small></h1>
    </a>
    <nav>
        <a href="/">Inicio</a>
        <a href="/catalogo">Catálogo</a>
        <a href="/carrito">Carrito ({{ cantidad }})</a>
    </nav>
</header>

{{ contenido|safe }}

<footer>
    <strong class="logo">Auré</strong>
    <div>PARFUMS</div>
    <p>Una fragancia para cada versión de ti.</p>
    <span>Proyecto académico de Cómputo en la Nube · 2026</span>
</footer>
</body>
</html>
"""

def mostrar(titulo, contenido, **datos):
    carrito = session.get("carrito", [])
    return render_template_string(
        PLANTILLA,
        titulo=titulo,
        contenido=contenido,
        cantidad=len(carrito),
        **datos
    )

def obtener_carrito():
    ids = session.get("carrito", [])
    return [
        p for pid in ids
        for p in perfumes if p["id"] == pid
    ]

def dinero(cantidad):
    return f"${cantidad:,.2f} MXN"

def tarjeta(p):
    return f"""
    <article class="tarjeta producto"
             data-nombre="{p['nombre'].lower()}"
             data-tipo="{p['tipo'].lower()}">
        <img src="{p['imagen']}"
             alt="Perfume {p['nombre']}"
             loading="lazy"
             onerror="this.style.display='none'">
        <div class="info">
            <span class="tipo">{p['tipo']}</span>
            <h3>{p['nombre']}</h3>
            <p class="descripcion">{p['descripcion']}</p>
            <div class="precio">{dinero(p['precio'])}</div>
            <a class="boton" href="/agregar/{p['id']}">
                Agregar al carrito
            </a>
        </div>
    </article>
    """

# ==========================================
# INICIO
# ==========================================

@app.route("/")
def inicio():
    destacados = "".join(tarjeta(p) for p in perfumes[:4])

    contenido = f"""
    <section class="hero">
        <div class="hero-text">
            <span class="etiqueta">El arte de perfumarte</span>
            <h2>Una fragancia para cada versión de ti.</h2>
            <p>Descubre aromas que expresan tu esencia,
               resaltan tu personalidad y convierten
               cada momento en algo especial.</p>
            <a class="boton" href="/catalogo">Ver colección →</a>
        </div>
    </section>

    <section class="beneficios">
        <div>✧ <strong>Fragancias para ti</strong>
             <span>Encuentra tu estilo</span></div>
        <div>♢ <strong>Compra sencilla</strong>
             <span>Explora nuestro catálogo</span></div>
        <div>♡ <strong>Atención personalizada</strong>
             <span>Tu esencia es única</span></div>
    </section>

    <main class="seccion">
        <h2 class="titulo">Nuestras fragancias favoritas</h2>
        <p class="subtitulo">Pequeños detalles, grandes recuerdos.</p>
        <div class="catalogo">{destacados}</div>
        <p style="text-align:center;margin-top:30px">
            <a class="boton" href="/catalogo">Descubrir todos los perfumes</a>
        </p>
    </main>
    """

    return mostrar("Inicio", contenido)

# ==========================================
# CATALOGO, BUSQUEDA Y FILTROS
# ==========================================

@app.route("/catalogo")
def catalogo():
    productos = "".join(tarjeta(p) for p in perfumes)

    contenido = f"""
    <main class="seccion">
        <h2 class="titulo">Catálogo de perfumes</h2>
        <p class="subtitulo">Encuentra la fragancia perfecta para ti.</p>

        <div class="filtros">
            <input id="buscar" type="search"
                   placeholder="Buscar perfume..." aria-label="Buscar perfume">
            <select id="tipo" aria-label="Filtrar por aroma">
                <option value="">Todos los aromas</option>
                <option value="floral">Floral</option>
                <option value="amaderado">Amaderado</option>
                <option value="citrico">Cítrico</option>
                <option value="oriental">Oriental</option>
            </select>
        </div>

        <div id="catalogo" class="catalogo">{productos}</div>
        <p id="sin-resultados" class="vacio oculto">
            No encontramos perfumes con esos criterios.
        </p>
    </main>

    <script>
    const buscar = document.getElementById('buscar');
    const tipo = document.getElementById('tipo');
    const tarjetas = document.querySelectorAll('.producto');

    function filtrar() {{
        let visibles = 0;
        tarjetas.forEach(t => {{
            const coincideNombre = t.dataset.nombre.includes(
                buscar.value.toLowerCase().trim()
            );
            const coincideTipo = !tipo.value ||
                t.dataset.tipo === tipo.value;
            const mostrar = coincideNombre && coincideTipo;
            t.classList.toggle('oculto', !mostrar);
            if (mostrar) visibles++;
        }});
        document.getElementById('sin-resultados')
            .classList.toggle('oculto', visibles > 0);
    }}

    buscar.addEventListener('input', filtrar);
    tipo.addEventListener('change', filtrar);
    </script>
    """

    return mostrar("Catálogo", contenido)

# ==========================================
# AGREGAR AL CARRITO
# ==========================================

@app.route("/agregar/<int:pid>")
def agregar(pid):
    if not any(p["id"] == pid for p in perfumes):
        return redirect("/catalogo")

    carrito = session.get("carrito", [])
    carrito.append(pid)
    session["carrito"] = carrito
    session.modified = True
    return redirect(request.referrer or "/catalogo")

# ==========================================
# ELIMINAR PRODUCTO DEL CARRITO
# ==========================================

@app.route("/eliminar/<int:pid>", methods=["POST"])
def eliminar(pid):
    carrito = session.get("carrito", [])
    if pid in carrito:
        carrito.remove(pid)
    session["carrito"] = carrito
    return redirect("/carrito")

# ==========================================
# VACIAR CARRITO
# ==========================================

@app.route("/vaciar", methods=["POST"])
def vaciar():
    session["carrito"] = []
    return redirect("/carrito")

# ==========================================
# CARRITO
# ==========================================

@app.route("/carrito")
def carrito():
    productos = obtener_carrito()
    total = sum(p["precio"] for p in productos)

    if not productos:
        contenido = """
        <main class="panel vacio">
            <div style="font-size:55px">♡</div>
            <h2>Tu carrito está vacío</h2>
            <p>Tu próxima fragancia favorita te espera.</p>
            <a class="boton" href="/catalogo">Explorar perfumes</a>
        </main>
        """
        return mostrar("Carrito", contenido)

    filas = ""
    for p in productos:
        filas += f"""
        <div class="fila">
            <img src="{p['imagen']}" alt="{p['nombre']}">
            <div class="fila-info">
                <h3>{p['nombre']}</h3>
                <span class="tipo">{p['tipo']}</span>
                <p>{dinero(p['precio'])}</p>
                <form action="/eliminar/{p['id']}" method="post">
                    <button class="eliminar" type="submit">
                        Eliminar
                    </button>
                </form>
            </div>
        </div>
        """

    contenido = f"""
    <main class="panel">
        <h2 class="titulo">Tu carrito</h2>
        <p class="subtitulo">Revisa tus productos antes de continuar.</p>
        {filas}
        <div class="total">Total: {dinero(total)}</div>

        <form action="/comprar" method="post">
            <label for="nombre">Nombre completo</label>
            <input class="campo" id="nombre" name="nombre"
                   maxlength="100" required>

            <label for="correo">Correo electrónico</label>
            <input class="campo" id="correo" type="email" name="correo"
                   maxlength="150" required>

            <button class="boton" type="submit">
                Registrar pedido
            </button>
        </form>

        <form action="/vaciar" method="post">
            <button class="campo" type="submit">Vaciar carrito</button>
        </form>
        <a href="/catalogo">← Seguir comprando</a>
    </main>
    """

    return mostrar("Carrito", contenido)

# ==========================================
# CONFIRMACION DE PEDIDO
# ==========================================

@app.route("/comprar", methods=["POST"])
def comprar():
    productos = obtener_carrito()

    if not productos:
        return redirect("/carrito")

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()

    if not nombre or len(nombre) > 100 or not correo or len(correo) > 150:
        return "Revisa los datos ingresados.", 400

    total = sum(p["precio"] for p in productos)
    cantidad = len(productos)

    # Esta versión muestra una confirmación.
    # Para guardar pedidos permanentemente se necesita una base de datos.
    session["carrito"] = []

    contenido = f"""
    <main class="panel vacio">
        <div style="font-size:55px;color:#b66f86">✓</div>
        <span class="etiqueta">Auré Parfums</span>
        <h2 class="titulo">¡Gracias por tu pedido, {nombre}!</h2>
        <p>Tu pedido se registró en esta demostración.</p>
        <p>Correo de contacto: {correo}</p>
        <hr style="border:0;border-top:1px solid #eee">
        <p>Productos: {cantidad}</p>
        <h2>Total: {dinero(total)}</h2>
        <p style="color:#777;font-size:13px">
            Este sitio no procesa pagos reales ni envía correos.
        </p>
        <a class="boton" href="/">Volver a la tienda</a>
    </main>
    """

    return mostrar("Pedido confirmado", contenido)

# ==========================================
# SERVIDOR
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)),
            debug=False)