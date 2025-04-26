# app/dashboard_admin.py
import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, datetime
from app.oco_db import listar_ocorrencias

def painel_dashboard_admin():
    st.header("📊 Painel de Indicadores - Admin")

    ocorrencias = listar_ocorrencias()

    if not ocorrencias:
        st.warning("Nenhuma ocorrência registrada.")
        return

    # Montar dados
    dados = []
    for o in ocorrencias:
        id_, data, unidade, solicitante, descricao, tecnico, status, _, observacao = o
        dias = (date.today() - datetime.strptime(data, "%Y-%m-%d").date()).days if status == "Pendente" else ""
        dados.append({
            "Data": data,
            "Unidade": unidade,
            "Solicitante": solicitante,
            "Técnico": tecnico,
            "Status": status,
            "Dias Pendentes": dias,
            "Descrição": descricao,
            "Observações": observacao or ""
        })

    df = pd.DataFrame(dados)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Dias Pendentes"] = pd.to_numeric(df["Dias Pendentes"], errors="coerce")  # 👈 Corrige o erro

    # 🔔 Alerta para pendências críticas (>7 dias)
    criticas = df[(df["Status"] == "Pendente") & (df["Dias Pendentes"] > 7)]
    if not criticas.empty:
        st.warning(f"⚠️ {len(criticas)} ocorrência(s) estão pendentes há mais de 7 dias! Verifique na aba 📄 Ocorrências.")

    # Filtro por período
    st.markdown("### 🗓️ Filtros por Período")

    col1, col2 = st.columns(2)
    data_min = df["Data"].min().date()
    data_max = df["Data"].max().date()

    data_inicial = col1.date_input("De", value=data_min, min_value=data_min, max_value=data_max)
    data_final = col2.date_input("Até", value=data_max, min_value=data_min, max_value=data_max)

    df_filtrado = df[(df["Data"].dt.date >= data_inicial) & (df["Data"].dt.date <= data_final)]

    # KPIs
    total = len(df_filtrado)
    pendentes = (df_filtrado["Status"] == "Pendente").sum()
    resolvidas = (df_filtrado["Status"] == "Resolvida").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Ocorrências", total)
    col2.metric("🕓 Pendentes", pendentes)
    col3.metric("✅ Resolvidas", resolvidas)

    if df_filtrado.empty:
        st.warning("Nenhuma ocorrência no período selecionado.")
        return

    # Função auxiliar para gráfico com Altair
    def grafico_barras(df_, campo, titulo):
        contagem = df_[campo].value_counts().reset_index()
        contagem.columns = [campo, "Total"]
        grafico = alt.Chart(contagem).mark_bar().encode(
            x=alt.X(f"{campo}:N", axis=alt.Axis(labelAngle=0)),
            y="Total:Q",
            tooltip=[campo, "Total"]
        )
        texto = grafico.mark_text(
            align="center",
            baseline="bottom",
            dy=-5
        ).encode(text="Total:Q")

        st.subheader(titulo)
        st.altair_chart(grafico + texto, use_container_width=True)

    # Gráficos com Altair
    grafico_barras(df_filtrado, "Status", "📈 Distribuição por Status")
    grafico_barras(df_filtrado, "Unidade", "📍 Ocorrências por Unidade")
    grafico_barras(df_filtrado, "Técnico", "👨‍🔧 Ocorrências por Técnico")
