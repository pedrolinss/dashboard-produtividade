import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard de Produtividade",
    page_icon="📊",
    layout="wide",
)

st.title("Dashboard de Produtividade")

st.caption(
    "Acompanhe atividades, horas registradas e evolução da produtividade ao longo do tempo."
)

if st.session_state.get("atividade_registrada"):
    st.success("Atividade registrada com sucesso.")
    st.session_state["atividade_registrada"] = False

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

st.sidebar.divider()
st.sidebar.subheader("Nova atividade")

with st.sidebar.form(
    "form_nova_atividade",
    clear_on_submit=True
):
    nova_data = st.date_input(
        "Data da atividade",
        value=pd.Timestamp.today().date()
    )

    nova_atividade = st.text_input(
        "Atividade"
    )

    nova_categoria = st.selectbox(
        "Categoria",
        categorias
    )

    novas_horas = st.number_input(
        "Horas",
        min_value=0.5,
        max_value=12.0,
        value=1.0,
        step=0.5
    )

    novo_status = st.selectbox(
        "Status",
        ["Concluído", "Em andamento"]
    )

    registrar = st.form_submit_button(
        "Registrar atividade"
    )

if registrar:
    if not nova_atividade.strip():
        st.sidebar.error("Informe o nome da atividade.")

    else:
        novo_registro = pd.DataFrame([
            {
                "data": pd.to_datetime(nova_data),
                "atividade": nova_atividade.strip(),
                "categoria": nova_categoria,
                "horas": novas_horas,
                "status": novo_status,
            }
        ])

        dados_atualizados = pd.concat(
            [dados, novo_registro],
            ignore_index=True
        )

        dados_atualizados.to_csv(
            "data/atividades.csv",
            index=False,
            date_format="%Y-%m-%d"
        )

        st.session_state["atividade_registrada"] = True
        st.rerun()

# Aplica os filtros

if len(periodo) == 2:
    inicio = pd.to_datetime(periodo[0])
    fim = pd.to_datetime(periodo[1])
else:
    inicio = pd.to_datetime(periodo[0])
    fim = inicio

dados_filtrados = dados[
    dados["categoria"].isin(categorias_selecionadas)
    & dados["status"].isin(status_selecionados)
    & (dados["data"] >= inicio)
    & (dados["data"] <= fim)
]

if dados_filtrados.empty:
    st.warning("Nenhuma atividade encontrada para os filtros selecionados.")
    st.stop()

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

st.subheader("Visão geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Horas registradas", total_horas)
col2.metric("Atividades", total_atividades)
col3.metric("Concluídas", concluidas)
col4.metric("Taxa de conclusão", f"{taxa_conclusao:.0f}%")

# Gráfico
horas_por_categoria = (
    dados_filtrados.groupby("categoria")["horas"]
    .sum()
    .sort_values(ascending=False)
)

horas_por_dia = (
    dados_filtrados.groupby("data")["horas"]
    .sum()
    .sort_index()
)

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.write("### Horas por categoria")
    st.bar_chart(horas_por_categoria)


with col_grafico2:
    st.write("### Horas por dia")
    st.line_chart(horas_por_dia)

# Tabela
st.divider()
st.subheader("Atividades registradas")

dados_exibicao = dados_filtrados.copy()

dados_exibicao["data"] = (
    dados_exibicao["data"].dt.strftime("%d/%m/%Y")
)

dados_exibicao = dados_exibicao.rename(
    columns={
        "data": "Data",
        "atividade": "Atividade",
        "categoria": "Categoria",
        "horas": "Horas",
        "status": "Status",
    }
)

csv_filtrado = dados_exibicao.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="Baixar dados filtrados",
    data=csv_filtrado,
    file_name="atividades_filtradas.csv",
    mime="text/csv"
)

st.dataframe(
    dados_exibicao,
    hide_index=True,
    width="stretch"
)