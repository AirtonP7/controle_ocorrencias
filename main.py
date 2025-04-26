import streamlit as st
#st.set_page_config(page_title="Controle de Ocorrências", layout="centered")

from app.db import criar_tabelas
from app.login import render_app



def main():
    criar_tabelas()
    render_app()

if __name__ == "__main__":
    main()