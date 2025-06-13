import streamlit as st

def botoes_abas_horizontais(chave, opcoes, estilo="abas"):
    colunas = st.columns(len(opcoes))
    if f"aba_{chave}" not in st.session_state:
        st.session_state[f"aba_{chave}"] = opcoes[0]

    for i, opcao in enumerate(opcoes):
        is_selected = st.session_state[f"aba_{chave}"] == opcao
        btn_label = f"✅ {opcao}" if is_selected else opcao

        if colunas[i].button(btn_label, key=f"{chave}_{opcao}"):
            st.session_state[f"aba_{chave}"] = opcao

    return st.session_state[f"aba_{chave}"]
