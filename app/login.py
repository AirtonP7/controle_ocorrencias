import streamlit as st
from app.auth import login
from app.admin import painel_admin
from app.colaborador import painel_colaborador

def render_app():

    if "usuario" not in st.session_state:
        #Carregar GIF.
        #st.markdown("![Alt Text](https://i.postimg.cc/RZ2rcKww/sem-fundo-assign-15578482-unscreen.gif)")

        st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://i.postimg.cc/DZyc0Ym6/fone-de-ouvido-removebg-preview.png' alt='' width='20%'>
        <p></p>
    </div>
    """,
    unsafe_allow_html=True
)
        login()

     # Rodapé com versão e copyright
        st.markdown("""
         <div style='text-align: center; margin-top: 100px; font-size: 18px; color: gray;'>
            <p>V 1.0.0</p>
             <p>Copyright © Airton Pereira 2025</p>
            </div>
                """, unsafe_allow_html=True)



    else:
        with st.sidebar:
            # Logo
            st.image("https://i.postimg.cc/Df5wFvD9/Design-sem-nome-2023-03-17-T165226-578.png", width=120)
            #st.markdown("---")

            # Nome do usuário
            st.markdown("## 👨🏾‍💼 **Bem Vindo(a)!**")
            st.markdown(
                f"<div style='font-size:25px; font-weight:bold; color:#ffffff'>{st.session_state.usuario}</div>",
                unsafe_allow_html=True
            )

            # Nome do projeto
            st.markdown("### 🏬 <span style='font-size:20px; color:#7F8C8D;'>GRUPO MAX</span><br><span style='font-size:15px;'>Controle de Ocorrências</span>", unsafe_allow_html=True)
            #st.markdown("---")

            # Botão sair
            if st.button("🚪🏃🏾‍♂️ Sair"):
                st.session_state.clear()
                st.rerun()

            # Suporte técnico no final da sidebar
            st.markdown("---")
            st.markdown("#### 👨🏾‍💻 Suporte Técnico")
            st.markdown("""
                📱 [WhatsApp](https://wa.me/5585985762890)  
                📧 [airtonpereiradev@gmail.com](mailto:airtonpereiradev@gmail.com)
            """)
            #st.markdown("---")

        # Painel fora da sidebar
        if st.session_state.perfil == "admin":
            painel_admin(st.session_state.usuario)
        else:
            painel_colaborador(st.session_state.usuario)

