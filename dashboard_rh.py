# ==========================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard Nova Casa - Case Técnico", layout="wide")

# ==========================================
# 1. CARREGAMENTO E LIMPEZA DOS DADOS
# ==========================================
@st.cache_data # O Streamlit guarda isso na memória para ficar rápido
def carregar_dados():
    # Caminho do seu arquivo (garanta que o nome está igualzinho ao arquivo salvo no seu PC)
    caminho_arquivo = 'CASE INDICADORES.xlsx'
    
    # 1.1 Lendo as abas de indicadores mensais
    # Vamos pular a primeira linha (skiprows=1) porque ela contém o título "ABSENTEISMO 2025" que atrapalha o cabeçalho real
    df_absenteismo = pd.read_excel(caminho_arquivo, sheet_name='ABSENTEISMO', skiprows=1)
    df_turnover = pd.read_excel(caminho_arquivo, sheet_name='TURNOVER', skiprows=1)
    
    # 1.2 Lendo e unificando as abas de Desligamentos
    # Criamos uma lista com os nomes exatos das abas de estados
    abas_desligados = [' DESLIGADOS DF', 'DESLIGADOS GO', 'DESLIGADOS MG', 'DESLIGAS PA', 'DESLIGADOS BA', 'DESLIGAMENTOS MA']
    
    lista_dfs = [] # Lista vazia para guardar os pedaços de dados de cada estado
    
    for aba in abas_desligados:
        try:
            # Lê a aba específica
            df_estado = pd.read_excel(caminho_arquivo, sheet_name=aba)
            
            # Adicionamos uma coluna para saber de qual estado veio essa informação
            # Pegamos as duas últimas letras do nome da aba (ex: "DF" de " DESLIGADOS DF")
            df_estado['UF'] = aba[-2:] 
            
            # Guarda na nossa lista
            lista_dfs.append(df_estado)
        except Exception as e:
            st.error(f"Erro ao ler a aba {aba}. Verifique se o nome está correto no Excel.")
    
    # Junta todos os pedaços (estados) num único DataFrame gigante!
    df_desligados = pd.concat(lista_dfs, ignore_index=True)
    
    # 1.3 Limpeza e Transformação
    # Convertendo as colunas de data (texto) para o formato DateTime (Data)
    df_desligados['DATAADMISSAO'] = pd.to_datetime(df_desligados['DATAADMISSAO'], errors='coerce')
    df_desligados['DATADEMISSAO'] = pd.to_datetime(df_desligados['DATADEMISSAO'], errors='coerce')
    
    # Engenharia de Recursos (Feature Engineering): Calculando o Tempo de Casa em dias
    df_desligados['TEMPO_CASA_DIAS'] = (df_desligados['DATADEMISSAO'] - df_desligados['DATAADMISSAO']).dt.days
    
    return df_absenteismo, df_turnover, df_desligados

# Executando a função
df_absenteismo, df_turnover, df_desligados = carregar_dados()

# ==========================================
# TESTE DO PASSO 1 (Visualizando se deu certo)
# ==========================================
st.title("🚧 Teste da Fase 1 - Dados Unificados")


st.subheader("Base de Dados de Desligamentos (Unificados)")
st.dataframe(df_desligados, height=300) # Mostra a tabela completa com barra de rolagem vertical

# 2. BARRA LATERAL (FILTROS)
# ==========================================
st.sidebar.title("Filtros")
st.sidebar.markdown("Use os filtros abaixo para explorar os dados.")

# Extrai todos os Estados (UF) únicos da base para criar as opções do filtro
ufs = df_desligados['UF'].dropna().unique().tolist()
# Cria o botão de múltipla escolha. O 'default=ufs' faz com que todos venham marcados no início
uf_selecionada = st.sidebar.multiselect("Selecione o Estado (UF):", options=ufs, default=ufs)

# Aplica o filtro selecionado nas três tabelas simultaneamente
df_desl_filtrado = df_desligados[df_desligados['UF'].isin(uf_selecionada)]
df_turn_filtrado = df_turnover[df_turnover['UF'].isin(uf_selecionada)]
df_abs_filtrado = df_absenteismo[df_absenteismo['UF'].isin(uf_selecionada)]

# ==========================================
# 3. KPIs E MÉTRICAS PRINCIPAIS
# ==========================================
st.title("📊 Dashboard Analítico - Nova Casa Distribuidora")
st.markdown("Visão Estratégica de Gente & Gestão focada em Retenção e Turnover.")
st.divider()

# Cálculos Matemáticos para os indicadores
total_desligamentos = len(df_desl_filtrado)

# Verifica se a tabela não está vazia para evitar erro de divisão por zero
if total_desligamentos > 0:
    tempo_medio_dias = df_desl_filtrado['TEMPO_CASA_DIAS'].mean()
    
    if pd.isna(tempo_medio_dias):
        texto_tempo_casa = "0 meses e 0 dias"
    else:
        meses_int = int(tempo_medio_dias // 30)
        dias_int = int(round(tempo_medio_dias % 30))
        texto_tempo_casa = f"{meses_int} meses e {dias_int} dias"

    principal_motivo = df_desl_filtrado['MOTIVO'].mode()[0] # Pega o motivo que mais se repete (Moda)
else:
    texto_tempo_casa = "0 meses e 0 dias"
    principal_motivo = "Sem dados"

# Dividindo a tela em 3 colunas para os KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📉 Total de Desligamentos", total_desligamentos)
with col2:
    st.metric("⏳ Tempo Médio de Casa", texto_tempo_casa)
with col3:
    st.metric("⚠️ Principal Motivo de Saída", principal_motivo)

st.divider()

# ==========================================
# 4. CONSTRUÇÃO DOS GRÁFICOS (PLOTLY)
# ==========================================
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Tendência de Turnover em 2025")
    
    # EXPLICAÇÃO DIDÁTICA: 
    # A sua planilha de Turnover tem os meses nas colunas (formato "largo").
    # Os gráficos precisam dos meses nas linhas (formato "longo"). 
    # O comando pd.melt() faz essa mágica de "achatar" as colunas de meses!
    df_turn_longo = df_turn_filtrado.melt(id_vars='UF', var_name='Mês', value_name='Taxa')
    
    # Criando gráfico de linha
    fig_turnover = px.line(df_turn_longo, x='Mês', y='Taxa', color='UF', markers=True)
    
    # Formata o eixo Y para exibir como porcentagem (ex: 5.5%)
    fig_turnover.update_layout(yaxis_tickformat='.1%')
    
    st.plotly_chart(fig_turnover, use_container_width=True, key="grafico_turnover")

with col_grafico2:
    st.subheader("Análise: Por que estão saindo?")
    
    # Conta quantos desligamentos ocorreram por cada motivo
    contagem_motivos = df_desl_filtrado['MOTIVO'].value_counts().reset_index()
    contagem_motivos.columns = ['Motivo', 'Quantidade']
    
    # Cria gráfico de barras horizontal (melhor para ler textos longos)
    fig_motivos = px.bar(contagem_motivos, x='Quantidade', y='Motivo', orientation='h',
                         color='Quantidade', color_continuous_scale='Blues')
    
    # Ordena as barras do maior para o menor
    fig_motivos.update_layout(yaxis={'categoryorder':'total ascending'}) 
    st.plotly_chart(fig_motivos, use_container_width=True, key="grafico_motivos")
st.divider()

# ==========================================
# 5. GRÁFICOS ADICIONAIS (Absenteísmo e Tipo de Demissão)
# ==========================================
col_grafico3, col_grafico4 = st.columns(2)

with col_grafico3:
    st.subheader("Tendência de Absenteísmo em 2025")
    
    # Assim como no Turnover, precisamos "achatar" a tabela de Absenteísmo
    # transformando as colunas de meses em linhas
    df_abs_longo = df_abs_filtrado.melt(id_vars='UF', var_name='Mês', value_name='Taxa')
    
    # Criando o gráfico de linha
    fig_abs = px.line(df_abs_longo, x='Mês', y='Taxa', color='UF', markers=True)
    
    # Formata o eixo Y para exibir como porcentagem (ex: 5.5%)
    fig_abs.update_layout(yaxis_tickformat='.1%')
    
    st.plotly_chart(fig_abs, use_container_width=True, key="grafico_abs")

with col_grafico4:
    st.subheader("Distribuição por Tipo de Demissão")
    
    # Na sua base, a coluna 'DEM' guarda se foi Justa Causa, Pedido de Desligamento, etc.
    # Vamos contar quantas ocorrências de cada tipo existem
    contagem_dem = df_desl_filtrado['DEM'].value_counts().reset_index()
    contagem_dem.columns = ['Tipo de Demissão', 'Quantidade']
    
    # Criando um gráfico de rosca (Donut chart)
    fig_dem = px.pie(contagem_dem, names='Tipo de Demissão', values='Quantidade', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_dem, use_container_width=True, key="grafico_dem")

st.divider()

# ==========================================
# 6. ANÁLISE DE FUNÇÕES/CARGOS
# ==========================================
st.subheader("Cargos com Maior Volume de Desligamentos")
st.markdown("Top 10 funções que mais geram rotatividade na empresa.")

# Conta a quantidade de desligamentos por função e pega os 10 maiores
contagem_funcoes = df_desl_filtrado['FUNCAO'].value_counts().reset_index()
contagem_funcoes.columns = ['Função', 'Quantidade']
top_10_funcoes = contagem_funcoes.head(10)

# Gráfico de barras horizontais com gradiente de cor avermelhada (para sinalizar alerta)
fig_funcoes = px.bar(top_10_funcoes, x='Quantidade', y='Função', orientation='h',
                     color='Quantidade', color_continuous_scale='Reds',
                     text_auto=True)

# Garante que a maior barra fique no topo
fig_funcoes.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_funcoes, use_container_width=True, key="grafico_funcoes")