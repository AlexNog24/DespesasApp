import sqlite3
from datetime import datetime

DB_NAME = "despesas.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Criar a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_despesa(data, descricao, categoria, valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO despesas (data, descricao, categoria, valor)
        VALUES (?, ?, ?, ?)
    ''', (data, descricao, categoria, valor))
    conn.commit()
    conn.close()

def obter_despesas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, data, descricao, categoria, valor FROM despesas ORDER BY data DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def apagar_despesa(id_despesa):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM despesas WHERE id = ?', (id_despesa,))
    conn.commit()
    conn.close()

def total_por_categoria():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT categoria, SUM(valor) FROM despesas GROUP BY categoria')
    rows = cursor.fetchall()
    conn.close()
    return rows

def adicionar_orcamento(nome, tipo, valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orcamento (nome, tipo, valor) VALUES (?, ?, ?)', (nome, tipo, valor))
    conn.commit()
    conn.close()

def obter_orcamento():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, tipo, valor FROM orcamento ORDER BY tipo DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def apagar_orcamento(id_orcamento):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orcamento WHERE id = ?', (id_orcamento,))
    conn.commit()
    conn.close()

# --- NOVAS FUNÇÕES: FILTROS POR MÊS ---
def obter_meses_disponiveis():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT substr(data, 1, 7) FROM despesas ORDER BY data DESC")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        return [r[0] for r in rows]
    else:
        return [datetime.now().strftime("%Y-%m")]

def obter_despesas_mes(ano_mes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, descricao, categoria, valor FROM despesas WHERE data LIKE ? ORDER BY data DESC", (f"{ano_mes}-%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def total_por_categoria_mes(ano_mes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, SUM(valor) FROM despesas WHERE data LIKE ? GROUP BY categoria", (f"{ano_mes}-%",))
    rows = cursor.fetchall()
    conn.close()
    return rows