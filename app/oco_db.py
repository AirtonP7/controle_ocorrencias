from app.db_firestore import db
from datetime import datetime, date
from app.log_db import registrar_log
import streamlit as st

def adicionar_ocorrencia(unidade_solicitante, usuario_solicitante,
                         descricao, tecnico_responsavel,
                         status_atividade, observacao):

    data_registro = datetime.now().date().strftime("%Y-%m-%d")

    doc_ref = db.collection("ocorrencias").document()
    doc_ref.set({
        "data_registro": data_registro,
        "unidade_solicitante": unidade_solicitante,
        "usuario_solicitante": usuario_solicitante,
        "descricao": descricao,
        "tecnico_responsavel": tecnico_responsavel,
        "status_atividade": status_atividade,
        "dias_pendentes": 0 if status_atividade == "Pendente" else None,
        "observacao": observacao
    })

    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Criação de ocorrência",
        alvo=f"Unidade: {unidade_solicitante}",
        detalhes=f"Técnico: {tecnico_responsavel}, Status: {status_atividade}"
    )

@st.cache_data(ttl=60)
def listar_ocorrencias():
    ocorrencias = []
    docs = db.collection("ocorrencias").order_by("data_registro", direction="DESCENDING").get()
    for doc in docs:
        ocorrencia = doc.to_dict()
        ocorrencia["id"] = doc.id
        ocorrencias.append(ocorrencia)
    return ocorrencias

def editar_ocorrencia(id_ocorrencia, nova_descricao, novo_status, nova_observacao):
    update_data = {
        "descricao": nova_descricao,
        "status_atividade": novo_status,
        "observacao": nova_observacao
    }

    if novo_status == "Pendente":
        doc_ref = db.collection("ocorrencias").document(id_ocorrencia)
        doc = doc_ref.get()
        if doc.exists:
            data_registro_str = doc.to_dict()["data_registro"]
            data_registro = datetime.strptime(data_registro_str, "%Y-%m-%d").date()
            dias_pendentes = (date.today() - data_registro).days
            update_data["dias_pendentes"] = dias_pendentes
        else:
            update_data["dias_pendentes"] = 0
    else:
        update_data["dias_pendentes"] = None

    db.collection("ocorrencias").document(id_ocorrencia).update(update_data)

    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Edição de ocorrência",
        alvo=f"Ocorrência ID: {id_ocorrencia}",
        detalhes=f"Status atualizado: {novo_status}"
    )

def excluir_ocorrencia(id_):
    doc_ref = db.collection("ocorrencias").document(id_)
    doc = doc_ref.get()
    
    descricao = ""
    if doc.exists:
        data = doc.to_dict()
        descricao = data.get("descricao", "")

    doc_ref.delete()

    registrar_log(
        usuario=st.session_state.usuario,
        perfil=st.session_state.perfil,
        acao="Exclusão de ocorrência",
        alvo=f"Ocorrência: {descricao}"
    )
