# ocorrencias.py

from db_firestore import db
from datetime import datetime

def calcular_dias_pendentes(data_str):
    formatos = ["%Y-%m-%d", "%d/%m/%Y"]
    for fmt in formatos:
        try:
            data_ocorrencia = datetime.strptime(data_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Formato de data inválido: {data_str}")

    hoje = datetime.now()
    return (hoje - data_ocorrencia).days

def adicionar_ocorrencia(data_registro, descricao, observacao, status_atividade,
                         tecnico_responsavel, unidade_solicitante, usuario_solicitante):
    dias_pendentes = calcular_dias_pendentes(data_registro)
    doc_ref = db.collection("ocorrencias").document()
    doc_ref.set({
        "data_registro": data_registro,
        "descrição": descricao,
        "observação": observacao,
        "status_atividade": status_atividade,
        "tecnico_responsavel": tecnico_responsavel,
        "unidade_solicitante": unidade_solicitante,
        "usuario_solicitante": usuario_solicitante,
        "dias_pendentes": dias_pendentes
    })

def listar_ocorrencias():
    docs = db.collection("ocorrencias").stream()
    ocorrencias = []
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        if dados.get("status_atividade") != "concluido":
            dados["dias_pendentes"] = calcular_dias_pendentes(dados["data_registro"])
        ocorrencias.append(dados)
    return ocorrencias

def atualizar_ocorrencia(ocorrencia_id, dados: dict):
    if "data_registro" in dados:
        dados["dias_pendentes"] = calcular_dias_pendentes(dados["data_registro"])
    db.collection("ocorrencias").document(ocorrencia_id).update(dados)

def excluir_ocorrencia(ocorrencia_id):
    db.collection("ocorrencias").document(ocorrencia_id).delete()
