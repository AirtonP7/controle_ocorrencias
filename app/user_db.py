import sqlite3
import bcrypt
from app.db import conectar

def conectar():
    return sqlite3.connect("controle_ocorrencias.db")

def adicionar_usuario(login, senha, nome, perfil, cargo, setor):
    conn = conectar()
    cursor = conn.cursor()
    senha_criptografada = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    cursor.execute("""
        INSERT INTO usuarios (login, senha, nome_completo, perfil, cargo, setor)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (login, senha_criptografada, nome, perfil, cargo, setor))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, login, nome_completo, perfil, cargo, setor FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def editar_usuario(id_usuario, login, nome, perfil, cargo, setor):
    print(">>> EDITANDO USUÁRIO", id_usuario, login, nome, perfil, cargo, setor)  # DEBUG
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET login = ?, nome_completo = ?, perfil = ?, cargo = ?, setor = ?
        WHERE id = ?
    """, (login, nome, perfil, cargo, setor, id_usuario))
    conn.commit()
    conn.close()


def excluir_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conn.commit()
    conn.close()

def alterar_senha_usuario(id_usuario, nova_senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_criptografada = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt())
    cursor.execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE id = ?
    """, (senha_criptografada, id_usuario))
    conn.commit()
    conn.close()

def validar_login(login, senha_digitada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, login, senha, perfil
        FROM usuarios
        WHERE login = ?
    """, (login,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        id_usuario, login_db, senha_hash, perfil = usuario
        if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
            return (id_usuario, login_db, perfil)
    return None

