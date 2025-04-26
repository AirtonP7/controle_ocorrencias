import sqlite3

def conectar():
    return sqlite3.connect("controle_ocorrencias.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            senha TEXT,
            nome_completo TEXT,
            perfil TEXT,
            cargo TEXT,
            setor TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_fantasia TEXT,
            cnpj TEXT,
            rua TEXT,
            numero TEXT,
            cep TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_registro TEXT,
            unidade_solicitante TEXT,
            usuario_solicitante TEXT,
            descricao TEXT,
            tecnico_responsavel TEXT,
            status_atividade TEXT CHECK(status_atividade IN ('Pendente', 'Resolvida')),
            dias_pendentes INTEGER,
            observacao TEXT
        )
    """)
    conn.commit()
    conn.close()
