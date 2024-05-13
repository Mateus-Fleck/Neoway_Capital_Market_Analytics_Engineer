import streamlit as st
import yfinance as yf
from datetime import data
import pandas as pd
import numpy as np
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

DATA_INICIO = '2023-05-10'
DATA_FIM = date.today().strftime('%Y-%m-%d')

st.title('Análise de ações')

# Create the sidebar 
st.sidebar.header('Escolha a ação')

n_dias = st.slider('Quantos dias de previsão?', 1, 365)

def pegar_dados_acoes():
    path:'C:/Neoway/Neoway_Capital_Market_Analytics_Engineer/DEV_TEST_01/data/acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = pegar_dados_acoes()
    
acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)

