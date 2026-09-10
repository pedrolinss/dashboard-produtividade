# Dashboard de Produtividade

Dashboard interativo desenvolvido em Python para registro, acompanhamento e análise de atividades e produtividade.

## Funcionalidades

- Cadastro de novas atividades
- Filtros por categoria, status e período
- Indicadores de:
  - horas registradas
  - total de atividades
  - atividades concluídas
  - taxa de conclusão
- Gráfico de horas por categoria
- Gráfico de horas por dia
- Tabela detalhada das atividades
- Exportação dos dados filtrados em CSV
- Tratamento de filtros sem resultados
- Geração de dados fictícios para demonstração

## Tecnologias

- Python
- pandas
- Streamlit

## Estrutura do projeto

```text
dashboard-produtividade/
├── data/
│   └── atividades.csv
├── app.py
├── gerar_dados.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Executando localmente

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

## Dados de demonstração

Para recriar a base fictícia utilizada no projeto:

```bash
python gerar_dados.py
```

## Status

Versão 1.0 concluída.