import pandas as pd
import streamlit as st

st.title("Dashboard de Produtividade")

dados = pd.read_csv("data/atividades.csv")

dados["data"] = pd.to_datetime(dados["data"])

# Filtros
st.sidebar.header("Filtros")

categorias = dados["categoria"].unique()

categorias_selecionadas = st.sidebar.multiselect(
    "Categoria",
    categorias,
    default=categorias
)

status_disponiveis = dados["status"].unique()

status_selecionados = st.sidebar.multiselect(
    "Status",
    status_disponiveis,
    default=status_disponiveis
)

data_inicial = dados["data"].min()
data_final = dados["data"].max()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)

# Aplica os filtros

inicio = pd.to_datetime(periodo[0])
fim = pd.to_datetime(periodo[1])

dados_filtrados = dados[
    dados["categoria"].isin(categorias_selecionadas)
    & dados["status"].isin(status_selecionados)
    & (dados["data"] >= inicio)
    & (dados["data"] <= fim)
]

# KPIs
total_horas = dados_filtrados["horas"].sum()
total_atividades = len(dados_filtrados)

concluidas = len(
    dados_filtrados[
        dados_filtrados["status"] == "Concluído"
    ]
)

if total_atividades > 0:
    taxa_conclusao = (concluidas / total_atividades) * 100
else:
    taxa_conclusao = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Horas registradas", total_horas)
col2.metric("Atividades", total_atividades)
col3.metric("Concluídas", concluidas)
col4.metric("Taxa de conclusão", f"{taxa_conclusao:.0f}%")

# Gráfico
st.write("### Horas por categoria")

horas_por_categoria = (
    dados_filtrados.groupby("categoria")["horas"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(horas_por_categoria)

st.write("### Horas por dia")

horas_por_dia = (
    dados_filtrados.groupby("data")["horas"]
    .sum()
    .sort_index()
)

horas_por_dia.index = horas_por_dia.index.strftime("%d/%m/%Y")

st.line_chart(horas_por_dia)

# Tabela
st.write("### Atividades registradas")

dados_exibicao = dados_filtrados.copy()

dados_exibicao["data"] = (
    dados_exibicao["data"].dt.strftime("%d/%m/%Y")
)

st.dataframe(dados_exibicao)