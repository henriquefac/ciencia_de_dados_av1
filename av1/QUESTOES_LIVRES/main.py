import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data_path = Path(
    r"C:\Users\pedro\Desktop\Faculdade\ciencia_de_dados_av1\files\data\MICRODADOS_ENEM_2023.csv")
df = pd.read_csv(data_path, sep=";", encoding="latin1", low_memory=False)

def plot_hist_with_tukey(ax, data, title, color, xlabel, ylabel, use_log_scale=False):
    if not data.empty:
        data_cleaned = data.dropna()
        if data_cleaned.empty:
            return

        data_cleaned.hist(bins=50, ax=ax, edgecolor='black', color=color, alpha=0.7, log=use_log_scale)
        
        q1 = data_cleaned.quantile(0.25)
        q3 = data_cleaned.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        mean_val = data_cleaned.mean()
        
        ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Média: {mean_val:.2f}')
        ax.axvline(lower_bound, color='purple', linestyle='dashed', linewidth=2, label=f'Lim. Inf. Tukey: {lower_bound:.2f}')
        ax.axvline(upper_bound, color='purple', linestyle='dashed', linewidth=2, label=f'Lim. Sup. Tukey: {upper_bound:.2f}')
        ax.legend()
    else:
        ax.set_title(title + "\n(Sem dados suficientes)")
        
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel + (" (Escala Log)" if use_log_scale else ""))


#O tipo de escola afeta a nota dos alunos em matemática? Isso pode evidenciar a disparidade de notas no ambiente rural e urbano?
def first_question():
    var_names_escola_local = ['TP_ESCOLA', 'TP_LOCALIZACAO_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'NU_NOTA_MT']

    df_escola_local = df[var_names_escola_local].copy()
    df_escola_local.dropna(subset=['NU_NOTA_MT', 'TP_ESCOLA', 'TP_LOCALIZACAO_ESC', 'TP_DEPENDENCIA_ADM_ESC'], inplace=True)
    df_escola_local = df_escola_local[df_escola_local['NU_NOTA_MT'] > 0]

    tipo_escola_map = {
        1: 'Não Respondeu',
        2: 'Pública',
        3: 'Privada'
    }
    localizacao_map = {
        1: 'Urbana',
        2: 'Rural'
    }
    dependencia_map = {
        1: 'Federal',
        2: 'Estadual',
        3: 'Municipal',
        4: 'Privada'
    }

    df_escola_local['TP_ESCOLA_DESC'] = df_escola_local['TP_ESCOLA'].map(tipo_escola_map)
    df_escola_local['TP_LOCALIZACAO_ESC_DESC'] = df_escola_local['TP_LOCALIZACAO_ESC'].map(localizacao_map)
    df_escola_local['TP_DEPENDENCIA_ADM_ESC_DESC'] = df_escola_local['TP_DEPENDENCIA_ADM_ESC'].map(dependencia_map)

    df_escola_local_filtrado = df_escola_local[df_escola_local['TP_ESCOLA'].isin([2, 3])]

    media_notas = df_escola_local_filtrado.groupby(['TP_LOCALIZACAO_ESC_DESC', 'TP_DEPENDENCIA_ADM_ESC_DESC'])['NU_NOTA_MT'].mean().unstack()
    std_notas = df_escola_local_filtrado.groupby(['TP_LOCALIZACAO_ESC_DESC', 'TP_DEPENDENCIA_ADM_ESC_DESC'])['NU_NOTA_MT'].std().unstack()

    fig, axes_bar_box = plt.subplots(1, 2, figsize=(18, 7))

    media_notas.plot(kind='bar', ax=axes_bar_box[0], colormap='viridis')
    axes_bar_box[0].set_title('Nota Média de Matemática por Localização e Tipo de Escola')
    axes_bar_box[0].set_xlabel('Localização da Escola')
    axes_bar_box[0].set_ylabel('Nota Média de Matemática')
    axes_bar_box[0].legend(title='Dependência Administrativa')
    axes_bar_box[0].grid(axis='y', linestyle='--')
    axes_bar_box[0].tick_params(axis='x', rotation=0)

    df_escola_local_filtrado.boxplot(column='NU_NOTA_MT', by=['TP_LOCALIZACAO_ESC_DESC', 'TP_DEPENDENCIA_ADM_ESC_DESC'], 
        ax=axes_bar_box[1], figsize=(10,6), grid=False, rot=20)
    axes_bar_box[1].set_title('Distribuição das Notas de Matemática por Localização e Tipo de Escola')
    axes_bar_box[1].set_xlabel('Localização e Tipo de Escola')
    axes_bar_box[1].set_ylabel('Nota de Matemática')
    fig.suptitle('')

    plt.tight_layout()
    plt.show()

    fig_hist, axes_hist = plt.subplots(2, 2, figsize=(15, 12), sharex=True)

    plot_hist_with_tukey(axes_hist[0,0],
                        df_escola_local_filtrado[(df_escola_local_filtrado['TP_LOCALIZACAO_ESC_DESC'] == 'Urbana') &
                                                    (df_escola_local_filtrado['TP_DEPENDENCIA_ADM_ESC_DESC'] == 'Privada')]['NU_NOTA_MT'],
                        'Privada - Urbana', 'skyblue', 'Nota de Matemática', 'Frequência', use_log_scale=True)

    plot_hist_with_tukey(axes_hist[0,1],
                        df_escola_local_filtrado[(df_escola_local_filtrado['TP_LOCALIZACAO_ESC_DESC'] == 'Rural') &
                                                    (df_escola_local_filtrado['TP_DEPENDENCIA_ADM_ESC_DESC'] == 'Privada')]['NU_NOTA_MT'],
                        'Privada - Rural', 'salmon', 'Nota de Matemática', 'Frequência', use_log_scale=True)

    plot_hist_with_tukey(axes_hist[1,0],
                        df_escola_local_filtrado[(df_escola_local_filtrado['TP_LOCALIZACAO_ESC_DESC'] == 'Urbana') &
                                                    (df_escola_local_filtrado['TP_DEPENDENCIA_ADM_ESC_DESC'].isin(['Federal', 'Estadual', 'Municipal']))]['NU_NOTA_MT'],
                        'Pública (Total) - Urbana', 'lightgreen', 'Nota de Matemática', 'Frequência', use_log_scale=True)

    plot_hist_with_tukey(axes_hist[1,1],
                        df_escola_local_filtrado[(df_escola_local_filtrado['TP_LOCALIZACAO_ESC_DESC'] == 'Rural') &
                                                    (df_escola_local_filtrado['TP_DEPENDENCIA_ADM_ESC_DESC'].isin(['Federal', 'Estadual', 'Municipal']))]['NU_NOTA_MT'],
                        'Pública (Total) - Rural', 'gold', 'Nota de Matemática', 'Frequência', use_log_scale=True)

    fig_hist.suptitle('Distribuição das Notas de Matemática por Tipo e Localização da Escola (Escala Log no Eixo Y)', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

first_question()

#Como a escolha da língua estrangeira (TP_LINGUA) se relaciona com as notas em Linguagens e Códigos (NU_NOTA_LC)
def second_question():
    var_names_q2 = ['TP_LINGUA', 'NU_NOTA_LC']

    df_q2 = df[var_names_q2].copy()
    df_q2.dropna(inplace=True)
    df_q2 = df_q2[df_q2['NU_NOTA_LC'] > 0]

    tp_lingua_map = {
        0: 'Inglês',
        1: 'Espanhol'
    }
    df_q2['TP_LINGUA_DESC'] = df_q2['TP_LINGUA'].map(tp_lingua_map)

    media_notas_q2 = df_q2.groupby('TP_LINGUA_DESC')['NU_NOTA_LC'].mean().sort_values(ascending=False)

    plt.figure(figsize=(8, 6))
    media_notas_q2.plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Nota Média em Linguagens e Códigos por Língua Estrangeira Escolhida')
    plt.xlabel('Língua Estrangeira')
    plt.ylabel('Nota Média em Linguagens e Códigos')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    ingles_notas_lc = df_q2[df_q2['TP_LINGUA_DESC'] == 'Inglês']['NU_NOTA_LC']
    espanhol_notas_lc = df_q2[df_q2['TP_LINGUA_DESC'] == 'Espanhol']['NU_NOTA_LC']

    plot_hist_with_tukey(axes[0], ingles_notas_lc, 'Linguagens e Códigos - Optantes por Inglês', 'skyblue', 'Notas de Linguagens e Códigos', 'Frequência')
    plot_hist_with_tukey(axes[1], espanhol_notas_lc, 'Linguagens e Códigos - Optantes por Espanhol', 'salmon', 'Notas de Linguagens e Códigos', 'Frequência')

    fig.suptitle('Distribuição das Notas de Linguagens e Códigos por Língua Estrangeira', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

second_question()

def third_question():
    df_q3 = df[['NU_NOTA_MT', 'TP_ESTADO_CIVIL', 'TP_FAIXA_ETARIA']].dropna()
    df_q3 = df_q3[df_q3['NU_NOTA_MT'] > 0]

    estado_civil_map = {
        1: 'Solteiro(a)',
        2: 'Casado(a)/Companheiro(a)'
    }
    faixa_etaria_map = {
        'Até 25 anos': range(1, 11),
        '26 a 40 anos': range(11, 14),
        'Mais de 40 anos': range(14, 21)
    }

    df_q3 = df_q3[df_q3['TP_ESTADO_CIVIL'].isin(estado_civil_map.keys())]

    df_q3['Estado Civil'] = df_q3['TP_ESTADO_CIVIL'].map(estado_civil_map)

    def classificar_faixa(cod):
        for faixa, codigos in faixa_etaria_map.items():
            if cod in codigos:
                return faixa
    df_q3['Faixa Etária'] = df_q3['TP_FAIXA_ETARIA'].apply(classificar_faixa)

    palette = {
        'Solteiro(a)': '#1f77b4',
        'Casado(a)/Companheiro(a)': '#ff7f0e'
    }

    fig, axs = plt.subplots(2, 3, figsize=(18, 10), sharey=True)
    axs = axs.flatten()

    i = 0
    for estado, cor in palette.items():
        for faixa in faixa_etaria_map.keys():
            ax = axs[i]
            subset = df_q3[(df_q3['Estado Civil'] == estado) & (df_q3['Faixa Etária'] == faixa)]

            ax.hist(subset['NU_NOTA_MT'], bins=40, color=cor, edgecolor='black', log=True)
            
            ax.set_title(f'{estado} - {faixa}', fontsize=14)
            ax.set_xlabel('Nota de Matemática', fontsize=12)
            ax.set_ylabel('Frequência (escala log)', fontsize=12)
            i += 1

    plt.suptitle('Distribuição das Notas de Matemática por Estado Civil e Faixa Etária', fontsize=18, y=1.02)
    plt.tight_layout()
    plt.show()
    
third_question()