from app.db import conectar
from datetime import datetime, date

def adicionar_ocorrencia(unidade_solicitante, usuario_solicitante,
                         descricao, tecnico_responsavel,
                         status_atividade, observacao):
    conn = conectar()
    cursor = conn.cursor()

    data_registro = datetime.now().date()

    # Calcula dias pendentes no momento do cadastro
    if status_atividade == "Pendente":
        dias_pendentes = 0
    else:
        dias_pendentes = None

    cursor.execute("""
        INSERT INTO ocorrencias (
            data_registro, unidade_solicitante, usuario_solicitante,
            descricao, tecnico_responsavel, status_atividade,
            dias_pendentes, observacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data_registro, unidade_solicitante, usuario_solicitante,
        descricao, tecnico_responsavel, status_atividade,
        dias_pendentes, observacao
    ))
    conn.commit()
    conn.close()


def listar_ocorrencias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ocorrencias ORDER BY data_registro DESC")
    ocorrencias = cursor.fetchall()
    conn.close()
    return ocorrencias


def editar_ocorrencia(id_ocorrencia, nova_descricao, novo_status, nova_observacao):
    conn = conectar()
    cursor = conn.cursor()

    if novo_status == "Concluido":
        cursor.execute("""
            UPDATE ocorrencias
            SET descricao = ?, status_atividade = ?, observacao = ?, dias_pendentes = NULL
            WHERE id = ?
        """, (nova_descricao, novo_status, nova_observacao, id_ocorrencia))
    else:
        cursor.execute("SELECT data_registro FROM ocorrencias WHERE id = ?", (id_ocorrencia,))
        data = cursor.fetchone()
        if data:
            data_registro = datetime.strptime(data[0], "%Y-%m-%d").date()
            dias_pendentes = (date.today() - data_registro).days
        else:
            dias_pendentes = 0

        cursor.execute("""
            UPDATE ocorrencias
            SET descricao = ?, status_atividade = ?, observacao = ?, dias_pendentes = ?
            WHERE id = ?
        """, (nova_descricao, novo_status, nova_observacao, dias_pendentes, id_ocorrencia))

    conn.commit()
    conn.close()



def excluir_ocorrencia(id_ocorrencia):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ocorrencias WHERE id = ?", (id_ocorrencia,))
    conn.commit()
    conn.close()
