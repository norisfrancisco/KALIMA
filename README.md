# Análise Climatológica de Precipitação para Chimoio, Moçambique

## 📖 Visão Geral

Este repositório contém os scripts e a metodologia para a análise de dados de precipitação em Chimoio, Moçambique, cobrindo o período de 1981 a 2025. O objetivo principal deste trabalho é realizar um pré-processamento robusto, um controle de qualidade e uma análise estatística e visual dos dados de chuva, comparando as observações recentes com a normal climatológica da região.

Este projeto serve como um exemplo de um fluxo de trabalho completo em agrometeorologia, desde a aquisição de dados de satélite até a geração de visualizações prontas para publicação.

## 🛰️ Aquisição e Processamento de Dados

Os dados de precipitação foram obtidos através da API do **Google Earth Engine (GEE)**, garantindo acesso a séries temporais consistentes e de alta qualidade.

1.  **Geometria da Área de Estudo:** A área de análise não se baseia num único ponto, mas sim no polígono oficial da unidade administrativa **"Cidade de Chimoio"**. Esta geometria foi extraída do dataset **FAO GAUL (Global Administrative Unit Layers)**, garantindo que a precipitação calculada seja representativa de toda a área.

2.  **Dados de Precipitação:** Utilizou-se o dataset **CHIRPS Daily (Climate Hazards Group InfraRed Precipitation with Station data)**, que combina dados de satélite com observações de estações. Este produto é amplamente validado e recomendado para estudos climáticos em África.

3.  **Agregação Mensal:** Os dados diários do CHIRPS foram agregados para totais mensais através de uma função de soma (`sum()`), criando uma série temporal mensal robusta, que é a base para toda a análise.

## 🔬 Análise e Visualização

O script principal (`KALIMA.py`) realiza um controle de qualidade, calcula estatísticas descritivas, analisa tendências e gera as seguintes visualizações de alta qualidade:

* **Precipitação vs. Climatologia:** Compara a precipitação do ano mais recente com a normal climatológica (1995-2024), incluindo a faixa de variação normal (percentis 25-75).

 ![Gráfico de Precipitação vs Climatologia](graficos/1_precipitacao_vs_climatologia_variacao.png)

* **Gráfico de Anomalias:** Mostra o desvio (em mm) da precipitação de cada mês do ano mais recente em relação à média climatológica.

    ![Gráfico de Anomalias](graficos/2_precipitacao_anomalia_mensal.png)

* **Série Temporal (1981-2025):** Mostra a evolução da precipitação mensal ao longo de todo o período.

    ![Série Temporal Mensal](grafalos/precip_timeseries_completa.png)

* **Precipitação Anual e Tendência:** Gráfico de barras com a precipitação total de cada ano e a linha de tendência.

    ![Gráfico de Tendência Anual](graficos/4_precip_tendencia_anual.png)

## 🚀 Como Usar

1.  **Pré-requisitos:** É necessário ter o Python 3 e as bibliotecas listadas no arquivo `requirements.txt`.
2.  **Autenticação:** Para o script de download de dados (`1_download_dados_gee.py`), é preciso ter uma conta no Google Earth Engine e autenticá-la.
3.  **Execução:** Siga as instruções nos scripts para baixar os dados e, em seguida, executar a análise.

## 📊 Resultados

Todos os gráficos e tabelas de resultados são salvos automaticamente na pasta de saída especificada nos scripts.
