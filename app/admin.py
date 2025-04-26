import streamlit as st
import pandas as pd
from app.und_db import adicionar_unidade, listar_unidades, editar_unidade, excluir_unidade
from app.oco_db import adicionar_ocorrencia, listar_ocorrencias, editar_ocorrencia, excluir_ocorrencia
from app.user_db import adicionar_usuario, listar_usuarios, editar_usuario, excluir_usuario, alterar_senha_usuario, conectar
from datetime import datetime, date
from app.dashboard_admin import painel_dashboard_admin
#from .admin import secao_usuarios, secao_unidades, secao_ocorrencias

def painel_admin(usuario):
    from .admin import secao_usuarios, secao_unidades, secao_ocorrencias
    if st.session_state.perfil != "admin":
        st.error("⛔ Acesso restrito! Você não tem permissão para acessar esta área.")
        return

    st.markdown("## 🎛️ Painel Administrativo")

    # Menu com botões estilizados
    menu_opcoes = {
        "Dashboard": "📊 Dashboard",
        "Usuarios": "👥 Usuários",
        "Unidades": "🏢 Unidades",
        "Ocorrencias": "📄 Ocorrências"
    }

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dashboard_btn = st.button(menu_opcoes["Dashboard"])
    with col2:
        usuarios_btn = st.button(menu_opcoes["Usuarios"])
    with col3:
        unidades_btn = st.button(menu_opcoes["Unidades"])
    with col4:
        ocorrencias_btn = st.button(menu_opcoes["Ocorrencias"])

    # Estado da seção ativa
    if "admin_secao" not in st.session_state:
        st.session_state["admin_secao"] = "Dashboard"
    if dashboard_btn:
        st.session_state["admin_secao"] = "Dashboard"
    elif usuarios_btn:
        st.session_state["admin_secao"] = "Usuarios"
    elif unidades_btn:
        st.session_state["admin_secao"] = "Unidades"
    elif ocorrencias_btn:
        st.session_state["admin_secao"] = "Ocorrencias"

    # Carregamento da seção ativa
    secao = st.session_state["admin_secao"]
    st.markdown("---")

    if secao == "Dashboard":
        painel_dashboard_admin()
    elif secao == "Usuarios":
        secao_usuarios()
    elif secao == "Unidades":
        secao_unidades()
    elif secao == "Ocorrencias":
        secao_ocorrencias(usuario)



### Seção: Usuários
def secao_usuarios():
    st.header("👥 Gerenciamento de Usuários")
    aba = st.radio("", ["Registrar", "Editar", "Relatório"], horizontal=True, label_visibility="collapsed")

    for campo in ["new_login", "new_senha", "new_nome", "new_perfil", "new_cargo", "new_setor"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    if "msg_sucesso_usuario" in st.session_state:
        st.success("Usuário cadastrado com sucesso!")
        del st.session_state["msg_sucesso_usuario"]

    # REGISTRAR NOVO USUÁRIO
    if aba == "Registrar":
        st.subheader("Registrar Novo Usuário")
        with st.form("form_usuario"):
            login = st.text_input("Login", key="new_login")
            senha = st.text_input("Senha", type="password", key="new_senha")
            nome = st.text_input("Nome completo", key="new_nome")
            perfil = st.selectbox("Perfil", ["", "admin", "colaborador"], key="new_perfil")
            cargo = st.text_input("Cargo", key="new_cargo")
            setor = st.text_input("Setor", key="new_setor")
            submitted = st.form_submit_button("Cadastrar Usuário")

        if submitted:
            if login and senha and nome and perfil:
                adicionar_usuario(login, senha, nome, perfil, cargo, setor)
                st.session_state["msg_sucesso_usuario"] = True
                for campo in ["new_login", "new_senha", "new_nome", "new_perfil", "new_cargo", "new_setor"]:
                    st.session_state.pop(campo, None)
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")

    # EDITAR USUÁRIO
    elif aba == "Editar":
        st.subheader("Editar ou Excluir Usuários")

        usuarios = listar_usuarios()
        if not usuarios:
            st.info("Nenhum usuário cadastrado.")
        else:
            usuarios_opcoes = {f"{u[1]} - {u[2]} ({u[3]})": u for u in usuarios}
            escolha = st.selectbox("Selecione um usuário para editar", [""] + list(usuarios_opcoes.keys()))

            if escolha:
                user = usuarios_opcoes[escolha]
                id_, login, nome, perfil, cargo, setor = user

                with st.expander(f"Editar usuário: {nome}", expanded=True):
                    with st.form(f"form_editar_usuario_{id_}"):
                        novo_login = st.text_input("Login", value=login, key=f"login_{id_}")
                        novo_nome = st.text_input("Nome completo", value=nome, key=f"nome_{id_}")
                        novo_perfil = st.selectbox("Perfil", ["admin", "colaborador"], index=["admin", "colaborador"].index(perfil), key=f"perfil_{id_}")
                        novo_cargo = st.text_input("Cargo", value=cargo, key=f"cargo_{id_}")
                        novo_setor = st.text_input("Setor", value=setor, key=f"setor_{id_}")

                        nova_senha = st.text_input("Nova senha (opcional)", type="password", key=f"senha_{id_}") if st.session_state.get("perfil") == "admin" else None

                        if st.form_submit_button("Salvar Alterações"):
                            editar_usuario(id_, novo_login, novo_nome, novo_perfil, novo_cargo, novo_setor)
                            if nova_senha:
                                alterar_senha_usuario(id_, nova_senha)

                            for campo in [f"login_{id_}", f"nome_{id_}", f"perfil_{id_}", f"cargo_{id_}", f"setor_{id_}", f"senha_{id_}"]:
                                st.session_state.pop(campo, None)

                            st.success("Usuário editado com sucesso!")
                            st.rerun()

            st.markdown("---")
            st.markdown("### 🗑️ Excluir Usuário")
            excluir_opcoes = {f"{u[1]} - {u[2]} ({u[3]})": u[0] for u in usuarios}
            usuario_excluir = st.selectbox("Selecione um usuário para excluir", [""] + list(excluir_opcoes.keys()))
            if usuario_excluir:
                if st.button("Confirmar Exclusão"):
                    excluir_usuario(excluir_opcoes[usuario_excluir])
                    st.warning("Usuário excluído com sucesso!")
                    st.rerun()

    # RELATÓRIO DE USUÁRIOS
    elif aba == "Relatório":
        st.subheader("Relatório de Usuários")
        usuarios = listar_usuarios()
        if usuarios:
            df = pd.DataFrame(usuarios, columns=["ID", "Login", "Nome", "Perfil", "Cargo", "Setor"])
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

            # Exportar para Excel
            #csv = df.drop(columns=["ID"]).to_csv(index=False).encode("utf-8")
            #st.download_button(
                #label="📥 Exportar para Excel",
                #data=csv,
                #file_name="usuarios_grupomax.xlsx",
                #mime="text/csv"
            #)

            # Salva como arquivo Excel
            with pd.ExcelWriter("usuarios_grupomax.xlsx", engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Dados")

            # Lê o conteúdo para ser disponibilizado no botão
            with open("usuarios_grupomax.xlsx", "rb") as file:
                excel_data = file.read()

            st.download_button(
                label="📥 Exportar para Excel",
                data=excel_data,
                file_name="usuarios_grupomax.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
        else:
            st.info("Nenhum usuário cadastrado.")



### Seção: Unidades

def secao_unidades():
    st.header("🏢 Gerenciamento de Unidades")
    aba = st.radio("", ["Registrar", "Editar", "Relatório"], horizontal=True, label_visibility="collapsed")

    for campo in ["nome_unidade", "cnpj_unidade", "rua_unidade", "numero_unidade", "cep_unidade"]:
        if campo not in st.session_state:
            st.session_state[campo] = ""

    if "msg_sucesso_unidade" in st.session_state:
        st.success("Unidade adicionada com sucesso!")
        del st.session_state["msg_sucesso_unidade"]

    # REGISTRAR UNIDADE
    if aba == "Registrar":
        st.subheader("Registrar Nova Unidade")
        with st.form("form_unidade"):
            nome = st.text_input("Nome", key="nome_unidade")
            cnpj = st.text_input("CNPJ", key="cnpj_unidade")
            rua = st.text_input("Rua", key="rua_unidade")
            numero = st.text_input("Número", key="numero_unidade")
            cep = st.text_input("CEP", key="cep_unidade")
            submitted = st.form_submit_button("Cadastrar Unidade")

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
    elif aba == "Editar":
        st.subheader("Editar ou Excluir Unidades")
        unidades = listar_unidades()
        if not unidades:
            st.info("Nenhuma unidade cadastrada.")
        else:
            opcoes = {f"{u[1]} ({u[2]})": u for u in unidades}
            escolha = st.selectbox("Selecione uma unidade para editar", [""] + list(opcoes.keys()))

            if escolha:
                id_, nome, cnpj, rua, numero, cep = opcoes[escolha]
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
            excluir_opcoes = {f"{u[1]} ({u[2]})": u[0] for u in unidades}
            excluir_escolha = st.selectbox("Selecione para excluir", [""] + list(excluir_opcoes.keys()))
            if excluir_escolha:
                if st.button("Confirmar Exclusão"):
                    excluir_unidade(excluir_opcoes[excluir_escolha])
                    st.warning("Unidade excluída com sucesso!")
                    st.rerun()

    # RELATÓRIO DE UNIDADES
    elif aba == "Relatório":
        st.subheader("Relatório de Unidades")
        unidades = listar_unidades()

        if not unidades:
            st.info("Nenhuma unidade cadastrada.")
        else:
            df = pd.DataFrame(unidades, columns=["ID", "Nome", "CNPJ", "Rua", "Número", "CEP"])
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

            # Exportar para Excel real (.xlsx)
            from io import BytesIO
            buffer = BytesIO()

            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.drop(columns=["ID"]).to_excel(writer, index=False, sheet_name="Unidades")

            st.download_button(
                label="📥 Exportar para Excel",
                data=buffer.getvalue(),
                file_name="unidades_grupomax.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )





### Seção: Ocorrências

def secao_ocorrencias(usuario_logado):
    st.header("📄 Ocorrências")

    aba = st.radio("Menu", ["Registrar", "Editar", "Relatório"], horizontal=True, label_visibility="collapsed")

    # REGISTRAR OCORRÊNCIA
    if aba == "Registrar":
        st.subheader("📝 Registrar Nova Ocorrência")

        unidades = listar_unidades()
        unidades_disp = [""] + [u[1] for u in unidades]  # Adiciona opção vazia

        tecnico_resp = listar_usuarios()
        tecnico_disp = [""] + [u[1] for u in tecnico_resp]  # Adiciona opção vazia

        with st.form("form_nova_ocorrencia"):
            descricao = st.text_input("Descrição da Ocorrência", key="desc_oco_colab")
            #solicitante = st.text_input("Solicitante", key="user_oco_colab")
            solicitante = st.selectbox("Solicitante", tecnico_disp, key="user_oco_colab")
            unidade = st.selectbox("Unidade", unidades_disp, key="unid_oco_colab")
            status = st.selectbox("Status da Atividade", ["", "Pendente", "Resolvida"], key="status_oco_colab")
            observacao = st.text_area("Observações", key="obs_oco_colab")
            submitted = st.form_submit_button("Registrar Ocorrência")

        if submitted:
            if descricao and solicitante and unidade and status:
                adicionar_ocorrencia(
                    unidade_solicitante=unidade,
                    usuario_solicitante=solicitante,
                    descricao=descricao,
                    tecnico_responsavel=usuario_logado,
                    status_atividade=status,
                    observacao=observacao
                )

                # Limpa campos após envio
                for campo in ["desc_oco_colab", "user_oco_colab", "unid_oco_colab", "status_oco_colab", "obs_oco_colab"]:
                    st.session_state.pop(campo, None)
                    st.session_state[campo] = ""

                st.success("Ocorrência registrada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos obrigatórios.")

    # EDITAR OCORRÊNCIA
    elif aba == "Editar":
        st.subheader("✏️ Editar Ocorrências Pendentes")
        ocorrencias = listar_ocorrencias()

        if not ocorrencias:
            st.info("Nenhuma ocorrência cadastrada.")
            return

        # Filtrar base por permissões
        if st.session_state.perfil == "admin":
            base_editaveis = [o for o in ocorrencias if o[6] == "Pendente"]


        else:
            base_editaveis = [o for o in ocorrencias if o[5] == usuario_logado and o[6] == "Pendente"]

        if not base_editaveis:
            st.info("Nenhuma ocorrência pendente disponível para edição.")
            return

        # Prepara DataFrame
        dados = []
        for ocorr in base_editaveis:
            id_, data_registro, unidade, usuario, descricao, tecnico, status, dias_pendentes, observacao = ocorr
            dias_calc = (date.today() - datetime.strptime(data_registro, "%Y-%m-%d").date()).days
            dados.append({
                "ID": id_,
                "Data": data_registro,
                "Solicitante": usuario,
                "Unidade": unidade,
                "Descrição": descricao,
                "Técnico": tecnico,
                "Status": status,
                "Dias Pendentes": dias_calc,
                "Observações": observacao or ""
            })

        df = pd.DataFrame(dados)

        # Filtros
        st.markdown("### 🔍 Filtros")
        option_all = "Todos"
        col1, col2 = st.columns(2)
        solicitantes = [option_all] + sorted(df["Solicitante"].dropna().unique())
        unidades = [option_all] + sorted(df["Unidade"].dropna().unique())
        tecnicos = [option_all] + sorted(df["Técnico"].dropna().unique())

        filtro_solicitante = col1.selectbox("Solicitante", solicitantes)
        filtro_unidade = col2.selectbox("Unidade", unidades)

        col3, col4 = st.columns(2)
        filtro_tecnico = col3.selectbox("Técnico", tecnicos)

        data_inicio = col3.date_input("Data Início", value=min(df["Data"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())))
        data_fim = col4.date_input("Data Fim", value=max(df["Data"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())))

        # Aplicar filtros
        df_filtrado = df.copy()
        if filtro_solicitante != option_all:
            df_filtrado = df_filtrado[df_filtrado["Solicitante"] == filtro_solicitante]
        if filtro_unidade != option_all:
            df_filtrado = df_filtrado[df_filtrado["Unidade"] == filtro_unidade]
        if filtro_tecnico != option_all:
            df_filtrado = df_filtrado[df_filtrado["Técnico"] == filtro_tecnico]
        if data_inicio and data_fim:
            df_filtrado = df_filtrado[
                (df_filtrado["Data"] >= data_inicio.strftime("%Y-%m-%d")) &
                (df_filtrado["Data"] <= data_fim.strftime("%Y-%m-%d"))
            ]

        # Mostrar ocorrências e permitir edição
        if df_filtrado.empty:
            st.warning("Nenhuma ocorrência pendente com os filtros selecionados.")
        else:
            for _, row in df_filtrado.iterrows():
                with st.form(f"editar_{row['ID']}"):
                    st.markdown(f"**{row['Descrição']}** - {row['Unidade']} ({row['Data']})")
                    novo_status = st.selectbox("Status", ["Pendente", "Resolvida"], index=0, key=f"status_{row['ID']}")
                    nova_obs = st.text_area("Observações", value=row["Observações"], key=f"obs_{row['ID']}")
                    salvar = st.form_submit_button("Salvar Alterações")

                    if salvar:
                        editar_ocorrencia(row["ID"], row["Descrição"], novo_status, nova_obs)
                        st.success("Ocorrência atualizada com sucesso!")
                        st.rerun()



    # RELATÓRIO
    elif aba == "Relatório":
        st.subheader("📊 Relatório de Ocorrências")
        ocorrencias = listar_ocorrencias()
        if not ocorrencias:
            st.info("Nenhuma ocorrência cadastrada.")
            return

        # Monta DataFrame
        dados = []
        for ocorr in ocorrencias:
            id_, data_registro, unidade, usuario, descricao, tecnico, status, dias_pendentes, observacao = ocorr
            dias_calc = (date.today() - datetime.strptime(data_registro, "%Y-%m-%d").date()).days if status == "Pendente" else ""
            dados.append({
                "ID": id_,
                "Data": data_registro,
                "Solicitante": usuario,
                "Unidade": unidade,
                "Descrição": descricao,
                "Técnico": tecnico,
                "Status": status,
                "Dias Pendentes": dias_calc,
                "Observações": observacao or ""
            })

        df = pd.DataFrame(dados)

        # Padronização da opção "Todos"
        option_all = "Todos"

        # Filtros
        st.markdown("### 🔍 Filtros")
        col1, col2 = st.columns(2)
        solicitantes = [option_all] + sorted(df["Solicitante"].dropna().unique())
        unidades = [option_all] + sorted(df["Unidade"].dropna().unique())
        status_opcoes = [option_all] + sorted(df["Status"].dropna().unique())
        tecnicos = [option_all] + sorted(df["Técnico"].dropna().unique())

        filtro_solicitante = col1.selectbox("Solicitante", solicitantes)
        filtro_unidade = col2.selectbox("Unidade", unidades)

        col3, col4 = st.columns(2)
        filtro_status = col3.selectbox("Status", status_opcoes)
        filtro_tecnico = col4.selectbox("Técnico", tecnicos)

        col_data_inicio, col_data_fim = st.columns(2)
        data_inicio = col_data_inicio.date_input(
            "Data Início",
            value=min(df["Data"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date()))
        )
        data_fim = col_data_fim.date_input(
            "Data Fim",
            value=max(df["Data"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date()))
        )

        # Aplicar filtros
        df_filtrado = df.copy()
        if filtro_solicitante != option_all:
            df_filtrado = df_filtrado[df_filtrado["Solicitante"] == filtro_solicitante]
        if filtro_unidade != option_all:
            df_filtrado = df_filtrado[df_filtrado["Unidade"] == filtro_unidade]
        if filtro_status != option_all:
            df_filtrado = df_filtrado[df_filtrado["Status"] == filtro_status]
        if filtro_tecnico != option_all:
            df_filtrado = df_filtrado[df_filtrado["Técnico"] == filtro_tecnico]
        if data_inicio and data_fim:
            df_filtrado = df_filtrado[
                (df_filtrado["Data"] >= data_inicio.strftime("%Y-%m-%d")) &
                (df_filtrado["Data"] <= data_fim.strftime("%Y-%m-%d"))
            ]

        # Exibir tabela
        st.markdown("### 📋 Resultados")
        st.dataframe(df_filtrado.drop(columns=["ID"]), use_container_width=True)

        # Exportar para Excel
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_filtrado.drop(columns=["ID"]).to_excel(writer, index=False, sheet_name="Ocorrências")

        st.download_button(
            label="📥 Exportar para Excel",
            data=buffer.getvalue(),
            file_name="ocorrencias_grupomax.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
