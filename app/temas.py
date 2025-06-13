import streamlit as st

def aplicar_tema():
    tema = st.session_state.get("tema", "Claro")

    if tema == "Escuro":
        primaryColor = "#0E1117"
        backgroundColor = "#000000"
        secondaryBackgroundColor = "#262730"
        textColor = "#FAFAFA"
    else:  # Tema Claro refinado
        primaryColor = "#E6F0FA"               
        backgroundColor =  "#008080"
        secondaryBackgroundColor = "#E0E7F0"  
        textColor = "#1C1C1C"                  

    st.markdown(
        f"""
        <style>
            .main {{
                background-color: {backgroundColor};
                color: {textColor};
            }}
            .stApp {{
                background-color: {backgroundColor};
            }}
            div[data-testid="stSidebar"] {{
                background-color: {secondaryBackgroundColor};
                color: {textColor};
            }}
            div[data-testid="stHeader"] {{
                background-color: {secondaryBackgroundColor};
            }}
            .css-18ni7ap.e8zbici2 {{
                background-color: {secondaryBackgroundColor};
                color: {textColor};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
