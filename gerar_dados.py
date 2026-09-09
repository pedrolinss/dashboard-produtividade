import random
from datetime import datetime, timedelta

import pandas as pd

categorias = [
    "Projeto",
    "Estudo",
    "Reunião",
    "Desenvolvimento",
    "Administrativo",
]

atividades = {
    "Projeto": [
        "Documentação",
        "Revisão de requisitos",
        "Planejamento de atividades",
    ],
    "Estudo": [
        "Estudo de Python",
        "Leitura de documentação",
        "Estudo de pandas",
    ],
    "Reunião": [
        "Reunião de alinhamento",
        "Reunião de acompanhamento",
    ],
    "Desenvolvimento": [
        "Desenvolvimento do dashboard",
        "Correção de código",
        "Implementação de funcionalidade",
    ],
    "Administrativo": [
        "Organização de tarefas",
        "Atualização de documentação",
    ],
}

random.seed(42)

registros = []

data_final = datetime(2026, 9, 9)
data_inicial = data_final - timedelta(days=20)

data_atual = data_inicial

while data_atual <= data_final:

    if data_atual.weekday() < 5:

        quantidade_atividades = random.randint(2, 4)

        for _ in range(quantidade_atividades):

            categoria = random.choice(categorias)

            atividade = random.choice(
                atividades[categoria]
            )

            horas = random.choice([
                0.5,
                1.0,
                1.5,
                2.0,
            ])

            status = random.choice([
                "Concluído",
                "Concluído",
                "Concluído",
                "Em andamento",
            ])

            registros.append({
                "data": data_atual.strftime("%Y-%m-%d"),
                "atividade": atividade,
                "categoria": categoria,
                "horas": horas,
                "status": status,
            })

    data_atual += timedelta(days=1)

df = pd.DataFrame(registros)

print(df.head())
print()
print(f"Total de registros: {len(df)}")
print()
print(df["categoria"].value_counts())
print()
print(df["status"].value_counts())

df.to_csv(
    "data/atividades.csv",
    index=False,
    encoding="utf-8"
)

print()
print("Arquivo data/atividades.csv gerado com sucesso.")