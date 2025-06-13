import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date, datetime
from app.und_db import listar_unidades
from app.oco_db import adicionar_ocorrencia, listar_ocorrencias, editar_ocorrencia
from app.user_db import adicionar_usuario, listar_usuarios, editar_usuario, excluir_usuario
from app.temas import aplicar_tema
from app.components.sidebar_colaborador import menu_lateral_colaborador

def painel_colaborador(usuario_logado):
    aplicar_tema()
    aba = menu_lateral_colaborador()

    # REGISTRAR NOVA OCORRÊNCIA
    if aba == "Registrar Ocorrencias":
        st.markdown("## 📝 Registrar Nova Ocorrência")

        unidades = listar_unidades()
        unidades_disp = [""] + [u['nome'] for u in unidades]

        tecnico_resp = listar_usuarios()
        tecnico_disp = [""] + [u['login'] for u in tecnico_resp]  # Adiciona opção vazia

        with st.form("form_nova_ocorrencia"):
            descricao = st.text_input("Descrição da Ocorrência", key="desc_oco_colab")
            usuario_solicitante = st.selectbox("Solicitante", tecnico_disp, key="user_oco_colab")

            unidade = st.selectbox("Unidade", unidades_disp, key="unid_oco_colab")
            status = st.selectbox("Status da Atividade", ["", "Pendente", "Resolvida"], key="status_oco_colab")
            observacao = st.text_area("Observações", key="obs_oco_colab")
            submitted = st.form_submit_button("Registrar Ocorrência")

        if submitted:
            if descricao and usuario_solicitante and unidade and status:
                adicionar_ocorrencia(
                    unidade_solicitante=unidade,
                    usuario_solicitante=usuario_solicitante,
                    descricao=descricao,
                    tecnico_responsavel=usuario_logado,
                    status_atividade=status,
                    observacao=observacao
                )

                for campo in ["desc_oco_colab", "user_oco_colab", "unid_oco_colab", "status_oco_colab", "obs_oco_colab"]:
                    st.session_state.pop(campo, None)
                    st.session_state[campo] = ""

                st.success("Ocorrência registrada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")

    # MINHAS OCORRÊNCIAS
    elif aba == "Ocorrencias":
        st.markdown("## 📋 Ocorrências que estou responsável")

        ocorrencias = listar_ocorrencias()
        minhas = [o for o in ocorrencias if o['tecnico_responsavel'] == usuario_logado]

        if not minhas:
            st.info("Nenhuma ocorrência atribuída a você.")
            return

        dados = []
        for ocorr in minhas:
            id_ = ocorr['id']
            data_registro = ocorr['data_registro']
            unidade = ocorr['unidade_solicitante']
            usuario_solicitante = ocorr['usuario_solicitante']
            descricao = ocorr['descricao']
            tecnico = ocorr['tecnico_responsavel']
            status = ocorr['status_atividade']
            dias_pendentes = (date.today() - datetime.strptime(data_registro, "%Y-%m-%d").date()).days if status == "Pendente" else ""
            observacao = ocorr['observacao']

            dados.append({
                "ID": id_,
                "Solicitante": usuario_solicitante,
                "Unidade": unidade,
                "Data": data_registro,
                "Descrição": descricao,
                "Técnico Responsável": tecnico,
                "Status": status,
                "Dias Pendentes": dias_pendentes,
                "Observações": observacao
            })

        df = pd.DataFrame(dados)
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

        # Exportar Excel
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.drop(columns=["ID"]).to_excel(writer, index=False, sheet_name="Ocorrências")

        st.download_button(
            label="📥 Exportar para Excel",
            data=buffer.getvalue(),
            file_name=f"ocorrencias_{usuario_logado.lower()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("### ✏️ Atualizar Ocorrências Pendentes")
        for ocorr in minhas:
            if ocorr['status_atividade'] == "Pendente":
                id_ = ocorr['id']
                descricao = ocorr['descricao']
                observacao = ocorr['observacao']
                with st.form(f"form_editar_ocorrencia_{id_}"):
                    st.write(f"**Ocorrência:** {descricao}")
                    novo_status = st.selectbox("Status", ["Pendente", "Resolvida"], index=0, key=f"status_{id_}")
                    nova_observacao = st.text_area("Observações", value=observacao or "", key=f"obs_{id_}")
                    salvar = st.form_submit_button("Salvar Alterações")
                    if salvar:
                        editar_ocorrencia(id_, descricao, novo_status, nova_observacao)
                        st.success("Ocorrência atualizada!")
                        st.rerun()

    # SAIR
    elif aba == "Sair":
        st.session_state.clear()
        st.rerun()
