import sqlite3
from sqlite3 import Connection

DB_PATH = 'db/bot_database.db'

def get_connection() -> Connection:
    """Retorna a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    """Cria as tabelas necessárias no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()

    # Criação da tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            mercado_pago_email TEXT
        )
    ''')

    conn.commit()
    conn.close()

