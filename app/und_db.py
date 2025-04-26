from app.db import conectar

def adicionar_unidade(nome, cnpj, rua, numero, cep):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO filiais (nome_fantasia, cnpj, rua, numero, cep) VALUES (?, ?, ?, ?, ?)",
        (nome, cnpj, rua, numero, cep)
    )

    conn.commit()
    conn.close()

def listar_unidades():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_fantasia, cnpj, rua, numero, cep FROM filiais")
    unidades = cursor.fetchall()
    conn.close()
    return unidades

def editar_unidade(id_unidade, novo_nome, novo_cnpj, nova_rua, novo_numero, novo_cep):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE filiais
        SET nome_fantasia = ?, cnpj = ?, rua = ?, numero = ?, cep = ?
        WHERE id = ?
    """, (novo_nome, novo_cnpj, nova_rua, novo_numero, novo_cep, id_unidade))
    conn.commit()
    conn.close()

def excluir_unidade(id_unidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filiais WHERE id = ?", (id_unidade,))
    conn.commit()
    conn.close()
