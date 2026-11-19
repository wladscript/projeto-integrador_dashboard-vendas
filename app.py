import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

dados = pd.read_csv("dados.csv", encoding="utf-8")
dados.columns = dados.columns.str.strip()
dados["Data"] = pd.to_datetime(dados["Data"], format="%d/%m/%Y")
dados["Mês"] = dados["Data"].dt.strftime("%Y-%m")

st.title("Dashboard de Vendas — Loja de Informática")

opcoes_categoria = ["Todas"] + sorted(dados["Categoria"].unique().tolist())
categoria_selecionada = st.selectbox("Selecione a Categoria", opcoes_categoria)

if categoria_selecionada == "Todas":
    dados_filtrados = dados
else:
    dados_filtrados = dados[dados["Categoria"] == categoria_selecionada]

col_kpi1, col_kpi2 = st.columns(2)
faturamento_total = dados_filtrados["Faturamento"].sum()
quantidade_total = dados_filtrados["Quantidade"].sum()

col_kpi1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col_kpi2.metric("Quantidade Vendida", f"{quantidade_total:,} un.".replace(",", "."))

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Evolução Mensal do Faturamento (R$)")
    vendas_mes = dados_filtrados.groupby("Mês")["Faturamento"].sum()
    st.line_chart(vendas_mes)

with col2:
    st.subheader("Faturamento por Produto (R$)")
    vendas_produto = dados_filtrados.groupby("Produto")["Faturamento"].sum().sort_values(ascending=False)
    st.bar_chart(vendas_produto)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Faturamento por Categoria (R$)")
    fat_categoria = dados_filtrados.groupby("Categoria")["Faturamento"].sum().sort_values(ascending=False)
    st.bar_chart(fat_categoria)

with col4:
    st.subheader("Quantidade Vendida por Categoria (un.)")
    qtd_categoria = dados_filtrados.groupby("Categoria")["Quantidade"].sum().sort_values(ascending=False)
    st.bar_chart(qtd_categoria)

st.subheader("Tabela de Dados Filtrados")
st.dataframe(dados_filtrados.drop(columns=["Mês"]), use_container_width=True)