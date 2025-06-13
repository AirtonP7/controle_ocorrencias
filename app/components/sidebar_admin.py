import streamlit as st
from app.temas import aplicar_tema
from app.user_db import buscar_nome_por_email
from app.components.contato_feedback import contato_feedback


def menu_lateral_admin():
    aplicar_tema()

    opcoes = {
        "Dashboard": "📊 Dashboard",
        "Usuarios": "👥 Usuários",
        "Unidades": "🏢 Unidades",
        "Ocorrencias": "📄 Ocorrências",
        "RedefinirSenha": "🔑 Resetar Senha",
        "Logs": "🧾 Logs",
        "Contato": "💬 Fale com o Desenvolvedor",
        "Sair": "🚪 Sair"
    }

    # === CSS ===
    st.sidebar.markdown("""
        <style>
        .custom-button {
            background-color: #1a1a1a;
            color: white;
            padding: 10px 16px;
            margin: 5px 0;
            border: none;
            border-radius: 10px;
            text-align: left;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.2s ease;
        }
        .custom-button:hover {
            background-color: #333333;
            transform: scale(1.02);
        }
        .custom-button-active {
            background-color: #008080 !important;
            box-shadow: 0 0 8px #00ffff66;
        }
        </style>
    """, unsafe_allow_html=True)

    if "admin_secao" not in st.session_state:
        st.session_state["admin_secao"] = "Dashboard"

    # === INFORMAÇÕES DO USUÁRIO ===
    st.sidebar.markdown("""
    <div style="text-align: center;">
        <img src="https://i.postimg.cc/Df5wFvD9/Design-sem-nome-2023-03-17-T165226-578.png" width="100">
    </div>
    """, unsafe_allow_html=True)

    nome = buscar_nome_por_email(st.session_state.usuario)

    st.sidebar.markdown(f"""
        <div style='color: white; text-align: center; font-weight: bold; margin-top: 10px;'>
            👋 Olá, {nome}<br>
            <span style='font-size:13px; color:#bbb;'>Perfil: {st.session_state.perfil.upper()}</span>
        </div>
    """, unsafe_allow_html=True)



    # === BOTÕES DE TEMA ===
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("☀️ Claro", use_container_width=True):
            st.session_state["tema"] = "Claro"
    with col2:
        if st.button("🌙 Escuro", use_container_width=True):
            st.session_state["tema"] = "Escuro"

    st.sidebar.markdown("---")

    # === BOTÕES DE MENU ===
    for chave, label in opcoes.items():
        estilo = "custom-button"
        if st.session_state["admin_secao"] == chave:
            estilo += " custom-button-active"
        clicked = st.sidebar.button(label, key=f"btn_{chave}", use_container_width=True)
        if clicked:
            st.session_state["admin_secao"] = chave

    # === SUPORTE COM WHATSAPP, E-MAIL E COPIAR ===
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h4 style='display: inline-block;
                background-color:;
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                font-size: 18px;
                transition: 0.2s;;'>💻 Desenvolvidor Por:</h4>
        </div>  
                         
        <div style='text-align: center; margin-top: 0px;'>
            <h4 style='display: inline-block;
                background-color: #000000;
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                font-size: 15px;
                transition: 0.2s;;'>👨🏾‍💻 Airton Pereira</h4>
        </div>
    """, unsafe_allow_html=True)  


    if st.session_state.get("admin_secao") == "Contato":
        contato_feedback()

    return st.session_state["admin_secao"]

