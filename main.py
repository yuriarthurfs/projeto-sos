import streamlit as st
import boto3
from datetime import datetime, timezone
import pandas as pd

#Inicializa sessão do Boto3
session = boto3.Session(
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_DEFAULT_REGION"]
)

#Inicializa DynamoDB
dynamodb = session.resource('dynamodb')
tabela = dynamodb.Table('QueriesSugestoes')

st.set_page_config(page_title="Análise de Queries SQL", layout="wide")
st.title("🔍 Painel de Análise de Queries SQL com Gemini")

#Puxa os dados do DynamoDB
with st.spinner("Carregando queries do DynamoDB..."):
    response = tabela.scan()
    items = response.get('Items', [])

#Converte para DataFrame
df = pd.DataFrame(items)

#Converte timestamp para datetime (caso necessário)
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

#Filtros
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data inicial", datetime.now().date())
with col2:
    data_fim = st.date_input("Data final", datetime.now().date())

#Aplica filtro de data
if 'timestamp' in df.columns:
    df = df[
        (df['timestamp'].dt.date >= data_inicio) &
        (df['timestamp'].dt.date <= data_fim)
    ]

st.write(f"🔢 {len(df)} queries encontradas entre {data_inicio} e {data_fim}")

#Mostra a tabela
if not df.empty:
    st.dataframe(df[['timestamp', 'query', 'suggestion']], use_container_width=True)
else:
    st.warning("Nenhuma query encontrada nesse período.")
