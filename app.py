from flask import Flask, jsonify, render_template_string
import sqlite3
import pandas as pd

app = Flask(__name__)

# --- 1. BASE DE DATOS SQLITE (TIENDA DE TECNOLOGÍA) ---
def init_db():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            metodo_pago TEXT NOT NULL,
            monto_total REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM ventas')
    if cursor.fetchone()[0] == 0:
        datos_ejemplo = [
            ('Laptop Pro 15', 'Cómputo', 1200.00, 5, 'Tarjeta de Crédito', 6000.00, 18),
            ('Smartphone X', 'Telefonía', 800.00, 8, 'Transferencia', 6400.00, 25),
            ('Audífonos Noise-Cancel', 'Audio', 150.00, 15, 'Tarjeta de Crédito', 2250.00, 4),
            ('Monitor 4K 27"', 'Cómputo', 350.00, 10, 'Efectivo', 3500.00, 12),
            ('Teclado Mecánico', 'Accesorios', 90.00, 20, 'Transferencia', 1800.00, 30),
            ('Tablet Pro 11', 'Telefonía', 600.00 