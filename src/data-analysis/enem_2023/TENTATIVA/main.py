import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
#from scipy.stats import ttest_ind
from config import Config

data_path = Config.get_path_dir_data()["MICRODADOS_ENEM_2023.parquet"]
df = pd.read_parquet(data_path)

# Removendo valores nulos
notas_mt = df['NU_NOTA_MT'].dropna()


def first_question():
    plt.figure(figsize=(10, 5))
    plt.hist(notas_mt, bins=30, color="blue", edgecolor="black", alpha=0.7)

    plt.xlabel("Nota Matemática")
    plt.ylabel("Frequência")
    plt.title("Distribuição das Notas de Matemática no Enem 2023")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.boxplot(notas_mt, vert=False, patch_artist=True,
                boxprops=dict(facecolor="blue", alpha=0.5))
    plt.title("Boxplot das Notas de Matemática no Enem 2023")
    plt.xlabel("Nota Matemática")
    plt.show()


def second_question():
    mesma_cidade = df[df["SG_UF_ESC"] ==
                      df["SG_UF_PROVA"]]["NU_NOTA_MT"].dropna()
    outra_cidade = df[df["SG_UF_ESC"] !=
                      df["SG_UF_PROVA"]]["NU_NOTA_MT"].dropna()

    plt.figure(figsize=(10, 5))
    plt.boxplot([mesma_cidade, outra_cidade], labels=[
                "Mesma Cidade", "Outra Cidade"], patch_artist=True)
    plt.title("Notas de Matemática por Local da Prova")
    plt.ylabel("Nota de Matemática")
    plt.xlabel("Local da Prova")
    plt.show()


def third_question():
    competencias = ["NU_NOTA_COMP1", "NU_NOTA_COMP2",
                    "NU_NOTA_COMP3", "NU_NOTA_COMP4", "NU_NOTA_COMP5"]
    medias = df[competencias].mean()

    plt.figure(figsize=(10, 5))
    plt.bar(medias.index, medias.values, color="blue", alpha=0.7)
    plt.title("Média das Competências da Redação")
    plt.ylabel("Média da Nota")
    plt.xlabel("Competência")
    plt.show()


def fourth_question():
    df_filtered = df[["Q006", "NU_NOTA_MT"]].dropna()
    df_filtered["Q006"] = df_filtered["Q006"].astype("category").cat.codes

    plt.figure(figsize=(10, 5))
    plt.scatter(df_filtered["Q006"],
                df_filtered["NU_NOTA_MT"], alpha=0.5, color="blue")
    plt.xlabel("Faixa de Renda (Codificada)")
    plt.ylabel("Nota de Matemática")
    plt.title("Relação entre Renda Familiar e Nota de Matemática")
    plt.grid()
    plt.show()


def fifth_question():
    df["tem_carro_moto"] = df["Q011"].isin(["B", "C"])
    presenca = df.groupby("tem_carro_moto")[
        "TP_PRESENCA_MT"].value_counts(normalize=True).unstack()

    plt.figure(figsize=(10, 5))
    presenca.plot(kind="bar", stacked=True, color=["blue", "red"])
    plt.title("Taxa de Presença na Prova de Matemática")
    plt.xlabel("Possui Carro/Moto na Família")
    plt.ylabel("Proporção")
    plt.legend(["Faltou", "Presente"])
    plt.show()


def sixth_question():
    df["idade_grupo"] = df["TP_FAIXA_ETARIA"]

    plt.figure(figsize=(10, 5))
    df.boxplot(column="NU_NOTA_MT", by="idade_grupo", grid=False)
    plt.title("Distribuição das Notas de Matemática por Faixa Etária")
    plt.xlabel("Faixa Etária")
    plt.ylabel("Nota de Matemática")
    plt.suptitle("")
    plt.show()


def seventh_question():
    df["NU_ACERTOS_MT"] = (df["TX_RESPOSTAS_MT"] ==
                           df["TX_GABARITO_MT"]).sum(axis=1)
    acertos_notas = df.groupby("NU_ACERTOS_MT")["NU_NOTA_MT"].mean()

    plt.figure(figsize=(10, 5))
    plt.plot(acertos_notas.index, acertos_notas.values,
             marker="o", linestyle="-", color="blue")
    plt.title("Nota Média de Matemática vs. Número de Acertos")
    plt.xlabel("Número de Acertos")
    plt.ylabel("Nota Média")
    plt.grid()
    plt.show()


def eighth_question():
    questoes_certas = df[["TX_RESPOSTAS_MT", "TX_GABARITO_MT"]].dropna()
    dificuldade = (questoes_certas["TX_RESPOSTAS_MT"]
                   == questoes_certas["TX_GABARITO_MT"]).mean()

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(dificuldade)), dificuldade, color="blue", alpha=0.7)
    plt.title("Taxa de Acerto por Questão de Matemática")
    plt.xlabel("Questão")
    plt.ylabel("Taxa de Acerto")
    plt.show()

# first_question()

# second_question()

# third_question()

# ERRADASSA
# fourth_question()

# fifth_question()

# sixth_question()

# ERRADASSA
# seventh_question()

# ERRADASSA
# eighth_question()


def free_first_question():
    df_filtered = df[['TP_DEPENDENCIA_ADM_ESC', 'Q006', 'NU_NOTA_MT', 'NU_NOTA_LC',
             'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']]

    df_filtered['TIPO_ESCOLA'] = df_filtered['TP_DEPENDENCIA_ADM_ESC'].apply(
        lambda x: 'Privada' if x == 4 else ('Pública' if x in [1, 2, 3] else 'Sem info'))

    alta_renda = list("PQRSTUVWXYZ")
    baixa_renda = list("ABCD")
    df_filtered['CLASSE_RENDA'] = df_filtered['Q006'].apply(
        lambda x: 'Alta' if x in alta_renda else ('Baixa' if x in baixa_renda else 'Média'))

    # Ignorando notas 0 (leia-se: ausentes)
    col_notas = ['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']
    for col in col_notas:
        df_filtered = df_filtered[df_filtered[col] > 0]

    df_filtered['NOTA_MEDIA'] = df_filtered[col_notas].mean(axis=1)

    # Filtrar os dois grupos da análise
    grupo_publica_alta = df_filtered[(df_filtered['TIPO_ESCOLA'] == 'Pública') & (df_filtered['CLASSE_RENDA'] == 'Alta')]
    grupo_privada_baixa = df_filtered[(df_filtered['TIPO_ESCOLA'] == 'Privada') & (df_filtered['CLASSE_RENDA'] == 'Baixa')]

    # Qntd de alunos
    qtd_pub_alta = len(grupo_publica_alta)
    qtd_priv_baixa = len(grupo_privada_baixa)


    #Análise unicamente pela renda
    grupo_alta_renda = df_filtered[df_filtered['CLASSE_RENDA'] == 'Alta']['NOTA_MEDIA']
    grupo_baixa_renda = df_filtered[df_filtered['CLASSE_RENDA'] == 'Baixa']['NOTA_MEDIA']

    plt.figure(figsize=(8,6))
    plt.boxplot([grupo_alta_renda, grupo_baixa_renda],
                labels=['Alta Renda', 'Baixa Renda'],
                patch_artist=True,
                boxprops=dict(facecolor='green'),
                medianprops=dict(color='black'))
    plt.title('Comparação de Notas por Renda')
    plt.ylabel('Nota Média')
    plt.grid(True)
    plt.show()

    #Análise pelo tipo de escola (pública ou privada)
    grupo_publica = df_filtered[df_filtered['TIPO_ESCOLA'] == 'Pública']['NOTA_MEDIA']
    grupo_privada = df_filtered[df_filtered['TIPO_ESCOLA'] == 'Privada']['NOTA_MEDIA']

    plt.figure(figsize=(8,6))
    plt.boxplot([grupo_publica, grupo_privada],
                labels=['Escola Pública', 'Escola Privada'],
                patch_artist=True,
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='black'))
    plt.title('Comparação de Notas por Tipo de Escola')
    plt.ylabel('Nota Média')
    plt.grid(True)
    plt.show()

    # Gráfico agrupando Baixa renda e escola privada x Alta renda e escola pública
    plt.figure(figsize=(10,6))
    plt.boxplot([grupo_publica_alta['NOTA_MEDIA'], grupo_privada_baixa['NOTA_MEDIA']],
                labels=['Pública + Alta Renda', 'Privada + Baixa Renda'],
                patch_artist=True,
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='red'))
    plt.title('Comparação de Notas Médias - ENEM')
    plt.ylabel('Nota Média Geral')
    plt.grid(True)
    plt.show()

free_first_question()


def analise_tempo_conclusao():
    mapa_conclusao = {
        1: 'Concluiu EM',
        2: 'Conclui em 2023',
        3: 'Conclui após 2023',
        4: 'Não cursa'
    }

    mapa_renda = {
        'A': 'Nenhuma renda',
        'B': 'Até R$ 1.320',
        'C': 'R$ 1.320 - R$ 1.980',
        'D': 'R$ 1.980 - R$ 2.640',
        'E': 'R$ 2.640 - R$ 3.300',
        'F': 'R$ 3.300 - R$ 3.960',
        'G': 'R$ 3.960 - R$ 5.280',
        'H': 'R$ 5.280 - R$ 6.600',
        'I': 'R$ 6.600 - R$ 7.920',
        'J': 'R$ 7.920 - R$ 9.240',
        'K': 'R$ 9.240 - R$ 10.560',
        'L': 'R$ 10.560 - R$ 11.880',
        'M': 'R$ 11.880 - R$ 13.200',
        'N': 'R$ 13.200 - R$ 15.840',
        'O': 'R$ 15.840 - R$ 19.800',
        'P': 'R$ 19.800 - R$ 26.400',
        'Q': 'Acima de R$ 26.400',
    }

    df_validos = df[
        df['NU_NOTA_MT'].notnull() &
        df['TP_ST_CONCLUSAO'].notnull() &
        df['Q006'].notnull()
    ].copy()

    df_validos['SITUACAO_EM'] = df_validos['TP_ST_CONCLUSAO'].map(mapa_conclusao)
    df_validos['FAIXA_RENDA'] = df_validos['Q006'].map(mapa_renda)

    df_grouped = df_validos.groupby(['FAIXA_RENDA', 'SITUACAO_EM'])['NU_NOTA_MT'].mean().unstack()

    ordem_renda = list(mapa_renda.values())
    df_grouped = df_grouped.reindex(ordem_renda)

    plt.figure(figsize=(16, 8))
    width = 0.2
    x = np.arange(len(df_grouped.index))

    for i, coluna in enumerate(df_grouped.columns):
        plt.bar(x + i * width, df_grouped[coluna], width=width, label=coluna)

    plt.xticks(x + width * 1.5, df_grouped.index, rotation=45, ha='right')
    plt.xlabel('Faixa de Renda Familiar')
    plt.ylabel('Nota média em Matemática')
    plt.title('Nota Média de Matemática por Faixa de Renda e Situação no Ensino Médio')
    plt.legend(title='Situação no EM')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def analise_rural_urbano():
    dependencia_dict = {
        1: 'Federal',
        2: 'Estadual',
        3: 'Municipal',
        4: 'Privada'
    }

    localizacao_dict = {
        1: 'Urbana',
        2: 'Rural'
    }

    df['TP_DEPENDENCIA_ADM_ESC'] = df['TP_DEPENDENCIA_ADM_ESC'].map(dependencia_dict)
    df['TP_LOCALIZACAO_ESC'] = df['TP_LOCALIZACAO_ESC'].map(localizacao_dict)

    contagem = pd.crosstab(df['TP_LOCALIZACAO_ESC'], df['TP_DEPENDENCIA_ADM_ESC'])

    percentual = contagem.div(contagem.sum(axis=1), axis=0) * 100

    percentual.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20c')
    plt.title('Distribuição percentual do tipo de escola por localização')
    plt.xlabel('Localização da escola')
    plt.ylabel('Percentual (%)')
    plt.legend(title='Tipo de escola', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(axis='y')

    df_filtrado = df[df['NU_NOTA_MT'].notnull()]

    media_por_local = df_filtrado.groupby('TP_LOCALIZACAO_ESC')['NU_NOTA_MT'].mean().sort_values()

    plt.figure(figsize=(6, 4))
    media_por_local.plot(kind='bar', color='skyblue')
    plt.title('Nota média de Matemática por localização da escola')
    plt.xlabel('Localização da escola')
    plt.ylabel('Nota média')
    plt.grid(axis='y')
    plt.tight_layout()

    plt.show()

analise_rural_urbano()
