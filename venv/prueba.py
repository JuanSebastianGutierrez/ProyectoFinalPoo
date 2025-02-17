import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "Participantes.db")
try:
    conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
    print("Conexión exitosa a la base de datos en modo solo lectura.")
    conn.close()
except sqlite3.Error as e:
    print(f"Error al conectar en modo solo lectura: {e}")
