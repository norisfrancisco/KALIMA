# =============================================================================
# SCRIPT DE ANÁLISE COMPLETA DE PRECIPITAÇÃO
# Versão: v.1.0
# Autor: Francisco Noris
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import os

# --- CONFIGURAÇÃO ---
file_path = ".json"
output_folder = ""
os.makedirs(output_folder, exist_ok=True)

# --- CARREGAMENTO DOS DADOS ---
print("--- Carregando os Dados ---")
try:
    df_precip = pd.read_json(file_path, orient='index')
    df_precip.columns = ['PRECIP_mm_monthly']
    df_precip.index = pd.to_datetime(df_precip.index)
    df_precip.index.name = 'DATE'
    print("✅ Arquivo de precipitação carregado com sucesso.")
except FileNotFoundError:
    print(f"❌ ERRO: O arquivo '{file_path}' não foi encontrado.")
    exit()
except ValueError as e:
    print(f"❌ ERRO ao ler o arquivo JSON. Verifique o formato do arquivo: {e}")
    exit()

# --- CÁLCULOS PRINCIPAIS ---
print("\n--- Realizando Cálculos Principais ---")

# 1. Definir o período de referência
ref_start_year = 1995
ref_end_year = 2024
ref_period = df_precip.loc[f'{ref_start_year}':f'{ref_end_year}']
print(f"✅ Período de referência definido: {ref_start_year}-{ref_end_year}")

# 2. Calcular a climatologia com a média e os percentis (25% e 75%)
climatologia = ref_period.groupby(ref_period.index.month).agg(
    clima_mean=('PRECIP_mm_monthly', 'mean'),
    clima_p25=('PRECIP_mm_monthly', lambda x: np.percentile(x, 25)),
    clima_p75=('PRECIP_mm_monthly', lambda x: np.percentile(x, 75))
)
climatologia.index = climatologia.index.map(lambda m: pd.to_datetime(f'2000-{m}-01').strftime('%b'))
print("✅ Climatologia média mensal e percentis calculados.")

# 3. Pegar os dados "observados" do último ano disponível para plotar as barras
this_year = df_precip.index.year.max()
observado = df_precip.loc[f'{this_year}'].copy()
observado.index = observado.index.map(lambda d: d.strftime('%b'))
print(f"✅ Dados do último ano disponível ({this_year}) para plotagem obtidos.")

# 4. Encontrar os valores para o mês a ser destacado (o mais recente nos dados)
latest_month_data = df_precip.tail(1)
if not latest_month_data.empty:
    mes_destaque_date = latest_month_data.index[0]
    mes_destaque = mes_destaque_date.strftime('%b')
    valor_mes = latest_month_data['PRECIP_mm_monthly'].iloc[0]
    climatologia_mes_destaque = climatologia.loc[mes_destaque, 'clima_mean']

    if climatologia_mes_destaque != 0:
        percentual_diferenca = ((valor_mes - climatologia_mes_destaque) / climatologia_mes_destaque) * 100
    else:
        percentual_diferenca = float('inf') if valor_mes > 0 else 0
    print(f"✅ Dados para o mês de destaque ({mes_destaque} {mes_destaque_date.year}) obtidos.")
else:
    print("❌ ERRO: Não há dados suficientes para o último mês para destaque.")
    mes_destaque, valor_mes, percentual_diferenca, climatologia_mes_destaque = [None] * 4

# --- GERAÇÃO DOS GRÁFICOS ---
print("\n--- Gerando gráficos aprimorados ---")
print(f"-> Usando o ano '{this_year}' para 'Observado' e '{ref_start_year}-{ref_end_year}' para 'Climatologia'.")


# Gráfico 1: Precipitação vs. Climatologia (com faixa de variação)
if not observado.empty and not climatologia.empty:
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12, 'axes.labelsize': 14, 'axes.titlesize': 16})
    
    fig, ax = plt.subplots(figsize=(14, 8))

    sns.barplot(x=observado.index, y='PRECIP_mm_monthly', data=observado,
                     color='dodgerblue', label=f'Observado ({this_year})', zorder=2, ax=ax)

    ax.fill_between(climatologia.index, climatologia['clima_p25'], climatologia['clima_p75'], 
                    color='gray', alpha=0.2, label='Variação Normal (P25-P75)', zorder=1)

    ax.plot(climatologia.index, climatologia['clima_mean'], 
            color='red', marker='o', linewidth=2.5, label=f'Climatologia Média ({ref_start_year}–{ref_end_year})', zorder=3)

    if mes_destaque and valor_mes is not None:
        meses_labels = [m.strftime('%b') for m in pd.date_range('2000-01-01', periods=12, freq='MS')]
        try:
            pos_destaque = meses_labels.index(mes_destaque)
            ax.plot(pos_destaque, valor_mes, marker='D', markersize=10, color='gold', zorder=5, 
                    markeredgecolor='black', markeredgewidth=1.5)

            if percentual_diferenca is not None and percentual_diferenca != float('inf'):
                texto_anotacao = f"{valor_mes:.1f} mm\n({percentual_diferenca:+.1f}%)"
            else:
                texto_anotacao = f"{valor_mes:.1f} mm\n(Infinito%)"

            ax.annotate(texto_anotacao, xy=(pos_destaque, valor_mes), xytext=(0, 20), 
                        textcoords='offset points', ha='center',
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5))
        except ValueError:
            print(f"⚠️ ATENÇÃO: O mês de destaque '{mes_destaque}' não foi encontrado nos rótulos do eixo X.")

    ax.set_title(f'Chimoio — Precipitação Mensal vs Climatologia ({ref_start_year}–{ref_end_year})', pad=20)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Precipitação Total (mm)')
    ax.set_xticklabels([m.strftime('%b') for m in pd.date_range('2000-01-01', periods=12, freq='MS')])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=0)
    ax.legend(loc='upper right', frameon=True)
    
    file_name = "1_precipitacao_vs_climatologia_variacao.png"
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)
    plt.close()
    print(f"✅ Gráfico '{file_name}' salvo na pasta '{output_folder}'.")
else:
    print("❌ ERRO: Não há dados suficientes para gerar o gráfico 1.")

# Gráfico 2: Gráfico de Anomalias (Precipitação vs. Climatologia)
if not observado.empty and not climatologia.empty:
    fig, ax = plt.subplots(figsize=(14, 8))
    
    anomalias = observado['PRECIP_mm_monthly'] - climatologia['clima_mean']
    
    cores = anomalias.apply(lambda x: 'dodgerblue' if x >= 0 else 'firebrick')
    
    meses_ordem = ['Jan', 'Fev', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    anomalias_ordenadas = anomalias.reindex(meses_ordem)

    sns.barplot(x=anomalias_ordenadas.index, y=anomalias_ordenadas.values, palette=cores.tolist(), ax=ax, zorder=2)
    
    ax.axhline(0, color='black', linewidth=1.5, linestyle='-', zorder=3)
    
    if mes_destaque and valor_mes is not None:
        anomalia_mes_destaque = anomalias.loc[mes_destaque]
        ax.plot(mes_destaque, anomalia_mes_destaque, marker='D', markersize=10, color='gold', zorder=5, 
                markeredgecolor='black', markeredgewidth=1.5)
        
        if percentual_diferenca is not None and percentual_diferenca != float('inf'):
            texto_anomalia = f"{anomalia_mes_destaque:+.1f} mm\n({percentual_diferenca:+.1f}%)"
        elif percentual_diferenca == float('inf'):
            texto_anomalia = f"{anomalia_mes_destaque:+.1f} mm\n(Infinito%)"
        else:
            texto_anomalia = f"{anomalia_mes_destaque:+.1f} mm"

        ax.annotate(texto_anomalia, xy=(mes_destaque, anomalia_mes_destaque), xytext=(0, 20), 
                    textcoords='offset points', ha='center',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5))

    ax.set_title(f'Chimoio — Anomalia da Precipitação Mensal ({this_year}) vs. Climatologia ({ref_start_year}–{ref_end_year})', pad=20)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Anomalia de Precipitação (mm)')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=0)
    
    file_name = "2_precipitacao_anomalia_mensal.png"
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, file_name), dpi=300)
    plt.close()
    print(f"✅ Gráfico '{file_name}' salvo na pasta '{output_folder}'.")
else:
    print("❌ ERRO: Não há dados suficientes para gerar o gráfico 2.")

print("\n✅ Análise e visualização concluídas com sucesso.")
