import streamlit as st
import pandas as pd
from app.oco_db import adicionar_ocorrencia, listar_ocorrencias, editar_ocorrencia, excluir_ocorrencia
from app.und_db import adicionar_unidade, listar_unidades, editar_unidade, excluir_unidade
from app.user_db import adicionar_usuario, listar_usuarios, editar_usuario, excluir_usuario
from datetime import datetime, date
from app.dashboard_admin import painel_dashboard_admin
import app.log_db
from app.db_firestore import db
from app.temas import aplicar_tema
from app.admin_tools import criar_usuario_firebase, excluir_usuario_firebase, redefinir_senha_firebase
from firebase_admin import auth as admin_auth
import secrets
import string
from app.redefinir_senha import tela_redefinir_senha
from app.components.sidebar_admin import menu_lateral_admin
from app.components.utils import botoes_abas_horizontais
from app.components.contato_feedback import contato_feedback
import io
import time

def gerar_senha_segura(tamanho=10):
    alfabeto = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alfabeto) for _ in range(tamanho))



def painel_admin(usuario):
    aplicar_tema()
    if st.session_state.perfil not in ["admin", "superadmin"]:
        st.error("⛔ Acesso restrito! Você não tem permissão para acessar esta área.")
        return

    # Sidebar lateral personalizada
    secao = menu_lateral_admin()
    #st.markdown(f"## 🎛️ Painel Administrativo — {secao}")

    st.markdown("---")

    if secao == "Dashboard":
        painel_dashboard_admin()
    elif secao == "Usuarios":
        secao_usuarios()
    elif secao == "Unidades":
        secao_unidades()
    elif secao == "Ocorrencias":
        secao_ocorrencias(usuario)
    elif secao == "Logs":
        secao_logs()
    elif secao == "RedefinirSenha":
        tela_redefinir_senha()
    elif secao == "Sair":
        st.session_state.clear()
        st.rerun()


### Seção: Usuários
def secao_usuarios():
    aplicar_tema()
    st.header("👥 Gerenciamento de Usuários")
    aba = botoes_abas_horizontais("usuarios", ["Registrar", "Editar", "Relatório"])

    for campo in ["new_login", "new_nome", "new_perfil", "new_cargo", "new_setor", "new_senha"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    if "msg_sucesso_usuario" in st.session_state:
        st.success("Usuário cadastrado com sucesso!")
        del st.session_state["msg_sucesso_usuario"]

    # REGISTRAR NOVO USUÁRIO
    if aba == "Registrar":
        st.subheader("Registrar Novo Usuário")
        DOMINIO_PADRAO = "@grupomax.com"

        perfis_disponiveis = ["admin", "colaborador"]
        if st.session_state.perfil == "superadmin":
            perfis_disponiveis.insert(0, "superadmin")

        with st.form("form_usuario"):
            username = st.text_input("Usuário*", key="new_login")
            nome = st.text_input("Nome completo*", key="new_nome")
            perfil = st.selectbox("Perfil*", [""] + perfis_disponiveis, key="new_perfil")
            cargo = st.text_input("Cargo*", key="new_cargo")
            setor = st.text_input("Setor*", key="new_setor")
            senha = st.text_input("Senha do usuário*", type="password", key="new_senha")
            submitted = st.form_submit_button("Cadastrar Usuário")
            st.text("* Campos Obrigatorios")

        if submitted:
            if username and nome and perfil and senha:
                email = f"{username.lower()}{DOMINIO_PADRAO}"

                if perfil == "superadmin" and st.session_state.perfil != "superadmin":
                    st.warning("⛔ Apenas SuperAdmins podem criar outros SuperAdmins.")
                else:
                    adicionar_usuario(email, nome, perfil, cargo, setor)
                    resultado_firebase = criar_usuario_firebase(email, senha)
                    st.success("✅ Usuário cadastrado com sucesso!")
                    st.info(f"📧 E-mail gerado: `{email}`")
                    st.write(resultado_firebase)
                    for campo in ["new_login", "new_nome", "new_perfil", "new_cargo", "new_setor", "new_senha"]:
                        st.session_state.pop(campo, None)
                    st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos obrigatórios.")

    elif aba == "Editar":
        st.subheader("Editar ou Excluir Usuários")
        usuarios = listar_usuarios()

        # Filtro para esconder superadmins se não for superadmin
        if st.session_state.perfil != "superadmin":
            usuarios = [u for u in usuarios if u["perfil"] != "superadmin"]

        if not usuarios:
            st.info("Nenhum usuário disponível.")
        else:
            usuarios_opcoes = {f"{u['login']} - {u['nome_completo']} ({u['perfil']})": u for u in usuarios}
            escolha = st.selectbox("Selecione um usuário para editar", [""] + list(usuarios_opcoes.keys()))

            if escolha:
                user = usuarios_opcoes[escolha]
                id_ = user['id']
                login = user['login']
                nome = user['nome_completo']
                perfil = user['perfil']
                cargo = user['cargo']
                setor = user['setor']

                with st.expander(f"Editar usuário: {nome}", expanded=True):
                    with st.form(f"form_editar_usuario_{id_}"):
                        st.markdown(f"**Login (e-mail):** `{login}`")
                        novo_nome = st.text_input("Nome completo", value=nome, key=f"nome_{id_}")

                        perfis_disponiveis = ["admin", "colaborador"]
                        if st.session_state.perfil == "superadmin":
                            perfis_disponiveis.insert(0, "superadmin")

                        novo_perfil = st.selectbox("Perfil", perfis_disponiveis,
                                                   index=perfis_disponiveis.index(perfil) if perfil in perfis_disponiveis else 0,
                                                   key=f"perfil_{id_}")
                        novo_cargo = st.text_input("Cargo", value=cargo, key=f"cargo_{id_}")
                        novo_setor = st.text_input("Setor", value=setor, key=f"setor_{id_}")

                        if st.form_submit_button("Salvar Alterações"):
                            editar_usuario(id_, login, novo_nome, novo_perfil, novo_cargo, novo_setor)
                            for campo in [f"nome_{id_}", f"perfil_{id_}", f"cargo_{id_}", f"setor_{id_}"]:
                                st.session_state.pop(campo, None)
                            st.success("Usuário editado com sucesso!")
                            st.rerun()

            st.markdown("---")
            st.markdown("### 🗑️ Excluir Usuário")
            excluir_opcoes = {f"{u['login']} - {u['nome_completo']} ({u['perfil']})": u['id'] for u in usuarios}
            usuario_excluir = st.selectbox("Selecione um usuário para excluir", [""] + list(excluir_opcoes.keys()))

            if usuario_excluir:
                id_usuario_excluir = excluir_opcoes[usuario_excluir]
                usuario_info = next((u for u in usuarios if u['id'] == id_usuario_excluir), None)

                if usuario_info and usuario_info['perfil'] == "superadmin" and st.session_state.perfil != "superadmin":
                    st.warning("⛔ Você não tem permissão para excluir um SuperAdmin.")
                else:
                    if st.button("Confirmar Exclusão"):
                        excluir_usuario(id_usuario_excluir)
                        try:
                            user_firebase = admin_auth.get_user_by_email(usuario_info["login"])
                            resultado_exclusao = excluir_usuario_firebase(user_firebase.uid)
                            st.info(resultado_exclusao)
                        except Exception as e:
                            st.warning(f"⚠️ Usuário excluído do Firestore, mas não foi possível remover do Firebase Auth: {e}")
                        st.success("Usuário excluído com sucesso!")
                        st.rerun()

    elif aba == "Relatório":
        st.subheader("📋 Relatório de Usuários")
        usuarios = listar_usuarios()

        if st.session_state.perfil != "superadmin":
            usuarios = [u for u in usuarios if u["perfil"] != "superadmin"]

        if usuarios:
            df = pd.DataFrame(usuarios).rename(columns={
                "login": "Login", "nome_completo": "Nome", "perfil": "Perfil",
                "cargo": "Cargo", "setor": "Setor"
            })[["Login", "Nome", "Perfil", "Cargo", "Setor"]]

            with st.expander("🔎 Filtros"):
                col1, col2 = st.columns(2)
                login_filtro = col1.selectbox("Login", ["Todos"] + sorted(df["Login"].unique()))
                nome_filtro = col2.selectbox("Nome", ["Todos"] + sorted(df["Nome"].unique()))
                col3, col4 = st.columns(2)
                perfil_filtro = col3.selectbox("Perfil", ["Todos"] + sorted(df["Perfil"].unique()))
                cargo_filtro = col4.selectbox("Cargo", ["Todos"] + sorted(df["Cargo"].unique()))
                setor_filtro = st.selectbox("Setor", ["Todos"] + sorted(df["Setor"].unique()))

                if login_filtro != "Todos":
                    df = df[df["Login"] == login_filtro]
                if nome_filtro != "Todos":
                    df = df[df["Nome"] == nome_filtro]
                if perfil_filtro != "Todos":
                    df = df[df["Perfil"] == perfil_filtro]
                if cargo_filtro != "Todos":
                    df = df[df["Cargo"] == cargo_filtro]
                if setor_filtro != "Todos":
                    df = df[df["Setor"] == setor_filtro]

            st.dataframe(
                df.style.set_properties(**{
                    'background-color': '#2d2d2d' if st.session_state.get("tema") == "Escuro" else '#ffffff',
                    'color': '#ffffff' if st.session_state.get("tema") == "Escuro" else '#000000',
                }),
                use_container_width=True
            )

            if "relatorio_usuarios_pronto" not in st.session_state:
                st.session_state["relatorio_usuarios_pronto"] = False

            if st.button("📊 Preparar Relatório"):
                with st.spinner("Preparando o relatório..."):
                    for i in range(101):
                        time.sleep(0.005)
                        st.progress(i)
                    st.session_state["relatorio_usuarios_pronto"] = True

            if st.session_state["relatorio_usuarios_pronto"]:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Usuários")
                buffer.seek(0)
                st.success("✅ Relatório pronto para download.")
                st.download_button("⬇️ Baixar Excel", buffer, "usuarios_grupomax.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        else:
            st.info("ℹ️ Nenhum usuário cadastrado.")





### Seção: Unidades

def secao_unidades():
    aplicar_tema()
    st.header("🏢 Gerenciamento de Unidades")
    aba_unid = botoes_abas_horizontais("unidades", ["Registrar", "Editar", "Relatório"])

    for campo in ["nome_unidade", "cnpj_unidade", "rua_unidade", "numero_unidade", "cep_unidade"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    if "msg_sucesso_unidade" in st.session_state:
        st.success("Unidade adicionada com sucesso!")
        del st.session_state["msg_sucesso_unidade"]

    # REGISTRAR UNIDADE
    if aba_unid == "Registrar":
        st.subheader("Registrar Nova Unidade")
        with st.form("form_unidade"):
            nome = st.text_input("Nome Filial*", key="nome_unidade")
            cnpj = st.text_input("CNPJ*", key="cnpj_unidade")
            rua = st.text_input("Rua/Av*", key="rua_unidade")
            numero = st.text_input("Número*", key="numero_unidade")
            cep = st.text_input("CEP*", key="cep_unidade")
            submitted = st.form_submit_button("Cadastrar Unidade")
            st.text("* Campos Obrigatorios")

        if submitted:
            if nome and cnpj and rua and numero and cep:
                adicionar_unidade(nome, cnpj, rua, numero, cep)
                st.session_state["msg_sucesso_unidade"] = True
                for campo in ["nome_unidade", "cnpj_unidade", "rua_unidade", "numero_unidade", "cep_unidade"]:
                    st.session_state.pop(campo, None)
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")

    # EDITAR UNIDADE
    elif aba_unid == "Editar":
        st.subheader("Editar ou Excluir Unidades")
        unidades = listar_unidades()
        if not unidades:
            st.info("Nenhuma unidade cadastrada.")
        else:
            opcoes = {f"{u['nome']} ({u['cnpj']})": u for u in unidades}
            escolha = st.selectbox("Selecione uma unidade para editar", [""] + list(opcoes.keys()))
            if escolha:
                id_, nome, cnpj, rua, numero, cep = opcoes[escolha]['id'], opcoes[escolha]['nome'], opcoes[escolha]['cnpj'], opcoes[escolha]['rua'], opcoes[escolha]['numero'], opcoes[escolha]['cep']
                with st.expander(f"Editar unidade: {nome}", expanded=True):
                    with st.form(f"form_editar_unidade_{id_}"):
                        novo_nome = st.text_input("Nome", value=nome, key=f"nome_{id_}")
                        novo_cnpj = st.text_input("CNPJ", value=cnpj, key=f"cnpj_{id_}")
                        nova_rua = st.text_input("Rua", value=rua, key=f"rua_{id_}")
                        novo_numero = st.text_input("Número", value=numero, key=f"numero_{id_}")
                        novo_cep = st.text_input("CEP", value=cep, key=f"cep_{id_}")
                        if st.form_submit_button("Salvar Alterações"):
                            if novo_nome and novo_cnpj and nova_rua and novo_numero and novo_cep:
                                editar_unidade(id_, novo_nome, novo_cnpj, nova_rua, novo_numero, novo_cep)
                                st.success("Unidade editada com sucesso!")
                                st.rerun()
                            else:
                                st.error("Preencha todos os campos obrigatórios.")
                st.markdown("---")
                st.markdown("### 🗑️ Excluir Unidade")
                excluir_opcoes = {f"{u['nome']} ({u['cnpj']})": u['id'] for u in unidades}
                excluir_escolha = st.selectbox("Selecione para excluir", [""] + list(excluir_opcoes.keys()))
                if excluir_escolha:
                    if st.button("Confirmar Exclusão"):
                        excluir_unidade(excluir_opcoes[excluir_escolha])
                        st.warning("Unidade excluída com sucesso!")
                        st.rerun()

    # RELATÓRIO DE UNIDADES
    elif aba_unid == "Relatório":
        st.subheader("Relatório de Unidades")
        unidades = listar_unidades()
        if unidades:
            df = pd.DataFrame(unidades)

            if not df.empty:
                df = df.rename(columns={
                    "nome": "Nome",
                    "cnpj": "CNPJ",
                    "rua": "Rua",
                    "numero": "Número",
                    "cep": "CEP"
                })

                colunas = ["Nome", "CNPJ", "Rua", "Número", "CEP"]
                df = df[colunas]

                # Filtros dinâmicos
                with st.expander("🔎 Filtros"):
                    col1, col2 = st.columns(2)
                    nome_filtro = col1.selectbox("Filtrar por Nome", ["Todos"] + sorted(df["Nome"].unique().tolist()))
                    cnpj_filtro = col2.selectbox("Filtrar por CNPJ", ["Todos"] + sorted(df["CNPJ"].unique().tolist()))

                    if nome_filtro != "Todos":
                        df = df[df["Nome"] == nome_filtro]
                    if cnpj_filtro != "Todos":
                        df = df[df["CNPJ"] == cnpj_filtro]

                st.dataframe(
            df.style.set_properties(**{
                'background-color': '#2d2d2d' if st.session_state.get("tema") == "Escuro" else '#ffffff',
                'color': '#ffffff' if st.session_state.get("tema") == "Escuro" else '#000000',
            }),
            use_container_width=True
                )

                # Exportar para Excel
                if "relatorio_unidades_pronto" not in st.session_state:
                    st.session_state["relatorio_unidades_pronto"] = False

                if st.button("📊 Preparar Relatório de Unidades"):
                    st.session_state["relatorio_unidades_pronto"] = False
                    with st.spinner("Preparando o relatório..."):
                        bar = st.progress(0, text="Gerando relatório... 0%")
                        for i in range(101):
                            time.sleep(0.01)
                            bar.progress(i, text=f"Gerando relatório... {i}%")
                        st.session_state["relatorio_unidades_pronto"] = True

                if st.session_state["relatorio_unidades_pronto"]:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Unidades")
                    buffer.seek(0)
                    st.success("✅ Relatório de unidades pronto.")
                    st.download_button("⬇️ Baixar Excel", buffer, "unidades_grupomax.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            else:
                st.warning("Erro ao gerar DataFrame das unidades.")
        else:
            st.info("Nenhuma unidade cadastrada.")


### Seção: Ocorrências
def secao_ocorrencias(usuario):
    aplicar_tema()
    st.header("📄 Gerenciamento de Ocorrências")
    aba_oco = botoes_abas_horizontais("ocorrencias", ["Registrar", "Editar", "Relatório"])

    # Inicializa campos
    for campo in ["descricao", "unidade_solicitante", "usuario_solicitante", "tecnico_responsavel", "status_atividade", "observacao"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    if "msg_sucesso_ocorrencia" in st.session_state:
        st.success("Ocorrência registrada com sucesso!")
        del st.session_state["msg_sucesso_ocorrencia"]

    if aba_oco == "Registrar":
        st.subheader("Registrar Nova Ocorrência")

        # Se solicitado, limpa os campos antes de renderizar o formulário
        if st.session_state.get("limpar_ocorrencia", False):
            for campo in ["descricao", "unidade_solicitante", "usuario_solicitante", "tecnico_responsavel", "status_atividade", "observacao"]:
                st.session_state[campo] = ""
            st.session_state["limpar_ocorrencia"] = False  # reseta o gatilho

        unidades = listar_unidades()
        unidades_disp = [""] + [u['nome'] for u in unidades]

        tecnicos = listar_usuarios()
        tecnicos_disp = [""] + [t['login'] for t in tecnicos]

        with st.form("form_ocorrencia"):
            descricao = st.text_input("Titulo Ocorrencia*", value=st.session_state["descricao"], key="descricao")
            unidade_solicitante = st.selectbox("Unidade Solicitante*", unidades_disp, index=unidades_disp.index(st.session_state["unidade_solicitante"]) if st.session_state["unidade_solicitante"] in unidades_disp else 0, key="unidade_solicitante")
            usuario_solicitante = st.selectbox("Usuário Solicitante*", tecnicos_disp, index=tecnicos_disp.index(st.session_state["usuario_solicitante"]) if st.session_state["usuario_solicitante"] in tecnicos_disp else 0, key="usuario_solicitante")
            tecnico_responsavel = st.selectbox("Técnico Responsável*", tecnicos_disp, index=tecnicos_disp.index(st.session_state["tecnico_responsavel"]) if st.session_state["tecnico_responsavel"] in tecnicos_disp else 0, key="tecnico_responsavel")
            status_atividade = st.selectbox("Status*", ["", "Pendente", "Resolvida"], index=["", "Pendente", "Resolvida"].index(st.session_state["status_atividade"]) if st.session_state["status_atividade"] else 0, key="status_atividade")
            observacao = st.text_area("Descrição*", value=st.session_state["observacao"], key="observacao")
            submitted = st.form_submit_button("Registrar")
            st.text("* Campos Obrigatórios")

        if submitted:
            if all([
                    st.session_state["descricao"],
                    st.session_state["unidade_solicitante"],
                    st.session_state["usuario_solicitante"],
                    st.session_state["tecnico_responsavel"],
                    st.session_state["status_atividade"]
                ]):

                adicionar_ocorrencia(
                    unidade_solicitante=st.session_state["unidade_solicitante"],
                    usuario_solicitante=st.session_state["usuario_solicitante"],
                    descricao=st.session_state["descricao"],
                    tecnico_responsavel=st.session_state["tecnico_responsavel"],
                    status_atividade=st.session_state["status_atividade"],
                    observacao=st.session_state["observacao"],
                )

                st.session_state["msg_sucesso_ocorrencia"] = True
                st.session_state["limpar_ocorrencia"] = True  # 🔁 ativa limpeza na próxima renderização
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")


    #EDITAR OCORRENCIAS
    elif aba_oco == "Editar":
        st.subheader("Editar ou Excluir Ocorrências")

        ocorrencias = listar_ocorrencias()
        if not ocorrencias:
            st.info("Nenhuma ocorrência cadastrada.")
            return

        df = pd.DataFrame(ocorrencias)

        if not df.empty:
            df = df.rename(columns={
                "id": "ID",
                "data_registro": "Data",
                "usuario_solicitante": "Solicitante",
                "unidade_solicitante": "Unidade",
                "descricao": "Descrição",
                "tecnico_responsavel": "Técnico",
                "status_atividade": "Status",
                "observacao": "Observação"
            })

            # Filtros dinâmicos
            with st.expander("🔎 Filtros"):
                col1, col2 = st.columns(2)
                unidade_filtro = col1.selectbox("Unidade", ["Todos"] + sorted(df["Unidade"].dropna().unique().tolist()))
                status_filtro = col2.selectbox("Status", ["Todos"] + sorted(df["Status"].dropna().unique().tolist()))
                col3, col4 = st.columns(2)
                tecnico_filtro = col3.selectbox("Técnico Responsável", ["Todos"] + sorted(df["Técnico"].dropna().unique().tolist()))
                solicitante_filtro = col4.selectbox("Solicitante", ["Todos"] + sorted(df["Solicitante"].dropna().unique().tolist()))

                data_inicio = st.date_input("Data Início")
                data_fim = st.date_input("Data Fim")

                if unidade_filtro != "Todos":
                    df = df[df["Unidade"] == unidade_filtro]
                if status_filtro != "Todos":
                    df = df[df["Status"] == status_filtro]
                if tecnico_filtro != "Todos":
                    df = df[df["Técnico"] == tecnico_filtro]
                if solicitante_filtro != "Todos":
                    df = df[df["Solicitante"] == solicitante_filtro]
                if data_inicio and data_fim:
                    df["Data"] = pd.to_datetime(df["Data"]).dt.date
                    df = df[(df["Data"] >= data_inicio) & (df["Data"] <= data_fim)]

            # Aplica os filtros no dataframe original
            ocorrencias_filtradas = df.to_dict(orient="records")
        else:
            ocorrencias_filtradas = []

        if not ocorrencias_filtradas:
            st.warning("Nenhuma ocorrência encontrada com os filtros aplicados.")
        else:
            opcoes = {f"{o['Descrição']} - {o['Status']}": o for o in ocorrencias_filtradas}
            escolha = st.selectbox("Selecione uma ocorrência para editar", [""] + list(opcoes.keys()))
            if escolha:
                ocorrencia = opcoes[escolha]
                with st.form(f"form_editar_ocorrencia_{ocorrencia['ID']}"):
                    descricao = st.text_input("Descrição", ocorrencia["Descrição"])

                    unidades = listar_unidades()
                    unidades_disp = [u['nome'] for u in unidades]
                    unidade_solicitante = st.selectbox("Unidade Solicitante", unidades_disp, index=unidades_disp.index(ocorrencia["Unidade"]))

                    tecnicos = listar_usuarios()
                    tecnicos_disp = [t['login'] for t in tecnicos]
                    usuario_solicitante = st.selectbox("Usuário Solicitante", tecnicos_disp, index=tecnicos_disp.index(ocorrencia["Solicitante"]))
                    tecnico_responsavel = st.selectbox("Técnico Responsável", tecnicos_disp, index=tecnicos_disp.index(ocorrencia["Técnico"]))

                    status = st.selectbox("Status", ["Pendente", "Resolvida"], index=["Pendente", "Resolvida"].index(ocorrencia["Status"]))
                    observacao = st.text_area("Observação", ocorrencia["Observação"])

                    if st.form_submit_button("Salvar Alterações"):
                        editar_ocorrencia(
                            id_ocorrencia=ocorrencia["ID"],
                            nova_descricao=descricao,
                            novo_status=status,
                            nova_observacao=observacao
                        )
                        st.success("Ocorrência atualizada com sucesso!")
                        st.rerun()

                if st.button("🗑️ Excluir Ocorrência"):
                    excluir_ocorrencia(ocorrencia["ID"])
                    st.warning("Ocorrência excluída com sucesso!")
                    st.rerun()



    elif aba_oco == "Relatório":
        st.subheader("Relatório de Ocorrências")
        ocorrencias = listar_ocorrencias()
        if ocorrencias:
            df = pd.DataFrame(ocorrencias)

            if not df.empty:
                df = df.rename(columns={
                    "id": "ID",
                    "data_registro": "Data",
                    "usuario_solicitante": "Solicitante",
                    "unidade_solicitante": "Unidade",
                    "descricao": "Descrição",
                    "tecnico_responsavel": "Técnico",
                    "status_atividade": "Status",
                    "dias_pendentes": "Dias Pendentes",
                    "observacao": "Observação"
                })

                colunas = ["ID", "Data", "Solicitante", "Unidade", "Descrição", "Técnico", "Status", "Dias Pendentes", "Observação"]
                df = df[colunas]

                # Filtros dinâmicos
                with st.expander("🔎 Filtros"):
                    col1, col2 = st.columns(2)
                    unidade_filtro = col1.selectbox("Unidade", ["Todos"] + sorted(df["Unidade"].dropna().unique().tolist()))
                    status_filtro = col2.selectbox("Status", ["Todos"] + sorted(df["Status"].dropna().unique().tolist()))
                    col3, col4 = st.columns(2)
                    tecnico_filtro = col3.selectbox("Técnico", ["Todos"] + sorted(df["Técnico"].dropna().unique().tolist()))
                    solicitante_filtro = col4.selectbox("Solicitante", ["Todos"] + sorted(df["Solicitante"].dropna().unique().tolist()))

                    # Filtro por data
                    datas_unicas = sorted(df["Data"].dropna().unique().tolist())
                    data_inicio = st.date_input("Data Início", value=None)
                    data_fim = st.date_input("Data Fim", value=None)

                    # Aplica filtros
                    if unidade_filtro != "Todos":
                        df = df[df["Unidade"] == unidade_filtro]
                    if status_filtro != "Todos":
                        df = df[df["Status"] == status_filtro]
                    if tecnico_filtro != "Todos":
                        df = df[df["Técnico"] == tecnico_filtro]
                    if solicitante_filtro != "Todos":
                        df = df[df["Solicitante"] == solicitante_filtro]

                    # Filtra por intervalo de data, se ambos definidos
                    if data_inicio and data_fim:
                        df = df[df["Data"].apply(lambda d: data_inicio.strftime("%Y-%m-%d") <= d <= data_fim.strftime("%Y-%m-%d"))]

                st.dataframe(
            df.style.set_properties(**{
                'background-color': '#2d2d2d' if st.session_state.get("tema") == "Escuro" else '#ffffff',
                'color': '#ffffff' if st.session_state.get("tema") == "Escuro" else '#000000',
            }),
            use_container_width=True
                )

                # Exportar para Excel
                if "relatorio_ocorrencias_pronto" not in st.session_state:
                    st.session_state["relatorio_ocorrencias_pronto"] = False

                if st.button("📊 Preparar Relatório de Ocorrências"):
                    st.session_state["relatorio_ocorrencias_pronto"] = False
                    with st.spinner("Preparando o relatório..."):
                        bar = st.progress(0, text="Gerando relatório... 0%")
                        for i in range(101):
                            time.sleep(0.01)
                            bar.progress(i, text=f"Gerando relatório... {i}%")
                        st.session_state["relatorio_ocorrencias_pronto"] = True

                if st.session_state["relatorio_ocorrencias_pronto"]:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Ocorrências")
                    buffer.seek(0)
                    st.success("✅ Relatório de ocorrências pronto.")
                    st.download_button("⬇️ Baixar Excel", buffer, "ocorrencias_grupomax.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            else:
                st.warning("Erro ao gerar DataFrame das ocorrências.")
        else:
            st.info("Nenhuma ocorrência cadastrada.")


def secao_logs():
    aplicar_tema()
    st.header("🧾 Logs do Sistema")

    # 🔁 Carrega dados
    docs = db.collection("logs_auditoria").order_by("momento", direction="DESCENDING").get()
    if not docs:
        st.info("Nenhum log registrado ainda.")
        return

    logs = []
    for doc in docs:
        d = doc.to_dict()
        logs.append({
            "Usuário": d.get("usuario", ""),
            "Perfil": d.get("perfil", ""),
            "Ação": d.get("acao", ""),
            "Alvo": d.get("alvo", ""),
            "Detalhes": d.get("detalhes", ""),
            "Momento": d.get("momento", "")
        })

    df = pd.DataFrame(logs)
    df["Momento"] = pd.to_datetime(df["Momento"])

    # 🔎 Filtros
    with st.expander("🔍 Filtros"):
        col1, col2 = st.columns(2)
        usuario_filtro = col1.selectbox("Filtrar por Usuário", ["Todos"] + sorted(df["Usuário"].unique()))
        acao_filtro = col2.selectbox("Filtrar por Ação", ["Todos"] + sorted(df["Ação"].unique()))

        col3, col4 = st.columns(2)
        perfil_filtro = col3.selectbox("Filtrar por Perfil", ["Todos"] + sorted(df["Perfil"].unique()))
        datas = df["Momento"].dt.date
        data_inicio = col4.date_input("De", value=datas.min())
        data_fim = st.date_input("Até", value=datas.max())

        if usuario_filtro != "Todos":
            df = df[df["Usuário"] == usuario_filtro]
        if acao_filtro != "Todos":
            df = df[df["Ação"] == acao_filtro]
        if perfil_filtro != "Todos":
            df = df[df["Perfil"] == perfil_filtro]

        df = df[(df["Momento"].dt.date >= data_inicio) & (df["Momento"].dt.date <= data_fim)]

    st.dataframe(
            df.style.set_properties(**{
                'background-color': '#2d2d2d' if st.session_state.get("tema") == "Escuro" else '#ffffff',
                'color': '#ffffff' if st.session_state.get("tema") == "Escuro" else '#000000',
            }),
                use_container_width=True
                    )

    # 📥 Exportar para Excel
    if "relatorio_logs_pronto" not in st.session_state:
        st.session_state["relatorio_logs_pronto"] = False

    if st.button("📊 Preparar Relatório de Logs"):
        st.session_state["relatorio_logs_pronto"] = False
        with st.spinner("Preparando o relatório..."):
            bar = st.progress(0, text="Gerando relatório... 0%")
            for i in range(101):
                time.sleep(0.01)
                bar.progress(i, text=f"Gerando relatório... {i}%")
            st.session_state["relatorio_logs_pronto"] = True

    if st.session_state["relatorio_logs_pronto"]:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Logs")
        buffer.seek(0)
        st.success("✅ Relatório de logs pronto.")
        st.download_button("⬇️ Baixar Excel", buffer, "logs_auditoria.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


         


