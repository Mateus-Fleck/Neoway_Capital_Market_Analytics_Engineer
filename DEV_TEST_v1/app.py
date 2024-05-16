import streamlit as st
import yfinance as yf
import pandas as pd
from plotly import graph_objs as go

# Carregar dados das ações
def pegar_dados_acoes():
    path = './data/acoes.csv'
    return pd.read_csv(path, delimiter=';')

# Função para baixar dados da ação online
def pegar_valores_online(sigla_acao, start_date, end_date):
    df = yf.download(sigla_acao, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

# Função para calcular os principais resultados do último dia
def calcular_principais_resultados(df_valores):
    ultimo_dia = df_valores.iloc[-1]
    resultados = {
        'Preço de Abertura': ultimo_dia['Open'],
        'Preço de Fechamento': ultimo_dia['Close'],
        'Preço Máximo': ultimo_dia['High'],
        'Preço Mínimo': ultimo_dia['Low']
    }
    return resultados

# Função para criar os cards personalizados
def criar_card(title, value):
    # Define os estilos base para os cards
    card_style = 'border: 2px solid {}; border-radius: 5px; padding: 15px; margin-right: 10px; flex: 1; background-color: {}; color: #ffffff; margin-bottom: 10px;'
    value_style = 'font-size: 24px; margin-bottom: 5px;'
    title_style = 'font-size: 18px; color: #ffffff;'

    # Define as cores de fundo para os diferentes tipos de cards
    if title == 'Preço de Abertura':
        value_style += 'color: #FFFFFF;' 
        card_style = card_style.format('#cccccc', '#333333')
    elif title == 'Preço de Fechamento':
        card_style = card_style.format('#00b0e6', '#333333')
        value_style += 'color: #00b0e6;'
    elif title == 'Preço Máximo':
        card_style = card_style.format('#008000', '#333333')
        value_style += 'color: green;'
    elif title == 'Preço Mínimo':
        card_style = card_style.format('#ff0000', '#333333')
        value_style += 'color: red;'

    # Cria o conteúdo do card com os estilos definidos
    card_content = f"""
        <div style="{card_style}">
            <div style="{value_style}">{value:.2f}</div>
            <div style="{title_style}">{title}</div>
        </div>
    """
    return card_content


st.title('Análise de ações')

# Sidebar com opções de ações e tipo de gráfico
st.sidebar.header('Escolha a ação')
df = pegar_dados_acoes()
acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', ['Escolher Todos'] + list(acao))
tipo_grafico = st.sidebar.radio("Selecione o tipo de gráfico:", ('Candlestick', 'Linha'))

# Filtrar data de início e fim da pesquisa
start_date = st.sidebar.date_input("Data de início:", pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("Data de fim:", pd.to_datetime('today'))

# Seleção da ação
if nome_acao_escolhida != 'Escolher Todos':
    df_acao = df[df['snome'] == nome_acao_escolhida]
    acao_escolhida = df_acao.iloc[0]['sigla_acao'] + '.SA'
    
    # Baixar dados da ação
    df_valores = pegar_valores_online(acao_escolhida, start_date, end_date)

    # Calcular e exibir principais resultados do último dia em cards personalizados
    st.subheader('Principais resultados do último dia')
    resultados = calcular_principais_resultados(df_valores)
    
    # Criar contêiner flexível para os cards
    st.markdown('<div style="display: flex;">', unsafe_allow_html=True)
    for chave, valor in resultados.items():
        # Adicionar cada card ao contêiner flexível
        st.markdown(criar_card(chave, valor), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Criar o gráfico
    st.subheader('Gráfico de preços da ação '+ acao_escolhida)
    if tipo_grafico == 'Candlestick':
        fig = go.Figure(data=[go.Candlestick(x=df_valores['Date'],
                                             open=df_valores['Open'],
                                             high=df_valores['High'],
                                             low=df_valores['Low'],
                                             close=df_valores['Close'])])
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_valores['Date'], 
                                 y=df_valores['Close'], 
                                 name='Preço de Fechamento',
                                 line_color='blue'))
    st.plotly_chart(fig)

    # Tabela de valores
    st.subheader('Tabela de valores - ' + acao_escolhida)
    st.write(df_valores.tail(10))

else:
    st.write("Por favor, escolha uma ação na barra lateral.")
