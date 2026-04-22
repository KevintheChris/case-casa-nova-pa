# 📊 Case Técnico: People Analytics - Nova Casa Distribuidora

Este repositório contém a solução desenvolvida para o case técnico do processo seletivo para a posição de **Analista de People Analytics** na Nova Casa Distribuidora.

O objetivo do projeto é extrair, organizar e analisar dados de Gente e Gestão para fornecer insights estratégicos à diretoria, focando em indicadores de **Turnover, Absenteísmo e Retenção**.

## 🚀 O Diferencial da Solução: Automação com Python

**Por que Python?**
- **Escalabilidade:** Capacidade de processar grandes volumes de dados de múltiplas fontes sem perda de performance.
- **Automação:** O código realiza a unificação automática de diversas abas regionais (DF, GO, MG, PA, BA, MA), eliminando o trabalho manual de consolidação.
- **Flexibilidade:** Permite a criação de métricas customizadas, como o cálculo de *Tenure* (Tempo de Casa) e análises preditivas futuras.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.12
- **Manipulação de Dados:** Pandas
- **Dashboard Interativo:** Streamlit
- **Visualização de Dados:** Plotly (Gráficos dinâmicos)

## 📈 Principais Insights Gerados
A análise foi estruturada considerando não apenas os números absolutos, mas a proporcionalidade das operações:

1.  **Concentração Operacional:** Identificamos que o volume de desligamentos é maior nas funções de **Auxiliar de Operação Logística** e nas regiões de **DF, GO e MG**. Isso reflete o maior headcount (volume de funcionários) nessas áreas, tornando-as prioritárias para investimentos em programas de retenção devido ao alto custo de reposição.
2.  **Binômio Turnover x Absenteísmo:** As regiões de GO e MG apresentam picos simultâneos de faltas e saídas, sugerindo a necessidade de intervenção em Clima Organizacional ou capacitação de lideranças locais.
3.  **Fuga de Talentos:** A principal causa de saída voluntária ("Melhor oportunidade de emprego") indica um sinal de alerta para a competitividade salarial e plano de carreira frente ao mercado logístico.
4.  **Anomalias Detectadas:** O dashboard revelou um pico atípico de turnover no Maranhão (MA) entre Agosto e Setembro, permitindo uma investigação rápida sobre eventos específicos naquela unidade.

## 📂 Estrutura do Projeto
- `dashboard_rh.py`: Código-fonte da aplicação Streamlit.
- `requirements.txt`: Lista de bibliotecas necessárias para rodar o projeto.
- `CASE INDICADORES.xlsx`: Base de dados original utilizada na análise.

## ⚙️ Como Executar o Projeto Localmente
1. Certifique-se de ter o Python instalado.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
3. Execute o Dashboard:
   ```bash
     streamlit run dashboard_rh.py

---
⚠️ **Aviso de Confidencialidade e Privacidade (LGPD)**
*Como este projeto foi desenvolvido especificamente como um case técnico corporativo, contendo simulações de indicadores estratégicos de RH, este repositório ficará público apenas temporariamente para a avaliação da equipe recrutadora. Em respeito às boas práticas de Governança de Dados e diretrizes de privacidade, o repositório será alterado para o modo **Privado** logo após o encerramento desta etapa do processo seletivo.*
