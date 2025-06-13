import streamlit as st
from app.temas import aplicar_tema
from app.user_db import buscar_nome_por_email
from app.components.contato_feedback import contato_feedback

def menu_lateral_colaborador():
    aplicar_tema()

    opcoes = {
        "Ocorrencias": "📄 Minhas Ocorrências",
        "Registrar Ocorrencias": "📝 Registrar Ocorrência",
        "Contato": "💬 Fale com o Desenvolvedor",
        "Sair": "🚪 Sair"
    }

    # === CSS estilo botão ===
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
            background-color: #005050 !important;
            box-shadow: 0 0 6px #00dddd66;
        }
        .sair-btn {
            display: block;
            background-color: #cc0000;
            color: white;
            padding: 12px 16px;
            text-align: center;
            border: none;
            border-radius: 10px;
            margin: 20px auto;
            font-size: 16px;
            font-weight: bold;
            width: 90%;
            transition: 0.2s;
        }
        .sair-btn:hover {
            background-color: #a80000;
            transform: scale(1.03);
        }
        </style>
    """, unsafe_allow_html=True)

    if "colab_secao" not in st.session_state:
        st.session_state["colab_secao"] = "Ocorrencias"

    # === Info do usuário logado ===
    st.sidebar.markdown("""
        <div style="text-align: center;">
            <img src="https://i.postimg.cc/Df5wFvD9/Design-sem-nome-2023-03-17-T165226-578.png" width="100">
        </div>
    """, unsafe_allow_html=True)
    nome = buscar_nome_por_email(st.session_state.usuario)

    st.sidebar.markdown(f"""
        <div style='color: white; text-align: center; font-weight: bold; margin-top: 10px;'>
            👋 Olá, {nome}<br>
            <span style='font-size:13px; color:#bbb;'>Perfil: COLABORADOR</span>
        </div>
    """, unsafe_allow_html=True)

    # === Tema claro/escuro ===
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("☀️ Claro", use_container_width=True):
            st.session_state["tema"] = "Claro"
    with col2:
        if st.button("🌙 Escuro", use_container_width=True):
            st.session_state["tema"] = "Escuro"

    st.sidebar.markdown("---")

    # === Botões do menu, exceto "Sair" ===
    for chave, label in opcoes.items():
        if chave == "Sair":
            continue
        estilo = "custom-button"
        if st.session_state["colab_secao"] == chave:
            estilo += " custom-button-active"
        clicked = st.sidebar.button(label, key=f"btn_colab_{chave}", use_container_width=True)
        if clicked:
            st.session_state["colab_secao"] = chave

    # === Botão sair customizado ===
    if st.sidebar.button("🚪 Sair", key="btn_sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # === SUPORTE COM WHATSAPP, E-MAIL E COPIAR ===
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; margin-top: 50px;'>
        <h4 style='display: inline-block;
            background-color:;
            color: white;
            padding: 8px 16px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
            font-size: 20px;
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
            font-size: 18px;
            transition: 0.2s;;'>👨🏾‍💻 Airton Pereira</h4>
    </div>
    """, unsafe_allow_html=True)  

    if st.session_state.get("colab_secao") == "Contato":
        contato_feedback()

    return st.session_state["colab_secao"]
