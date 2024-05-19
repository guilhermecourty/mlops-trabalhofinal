import streamlit as st
import requests

# Title and project explanation
st.set_page_config(page_title='CLOUD TOPIC MODELING', layout='wide')
st.title('CLOUD TOPIC MODELING')

# Project explanation
st.write("A QuantumFinance tem um canal de atendimento via chat e precisa classificar os assuntos dos atendimentos para melhorar as tratativas dos chamados dos clientes. O canal recebe textos abertos dos clientes relatando o problema e/ou dúvida e depois é direcionado para alguma área especialista no assunto para uma melhor tratativa.")

# Participants section
st.write('#### Participantes')
st.write('Rafael Henrique Siqueira Silva - RM348359')
st.write('Guilherme Moura - RM349452')
st.write('Carlo Ferrari - RM348003')
st.write('Vinicius Araujo - RM349721')

# Input field for user to enter text
st.write('## Descreva seu problema:')
text_input = st.text_area('', height=200)

# Button to trigger text classification
if st.button('Classificar atendimento'):
    # Make a request to your API for text classification
    api_url = 'http://your_api_url_here'
    response = requests.post(api_url, json={'text': text_input})
    
    # Display the classification result
    if response.status_code == 200:
        result = response.json()['result']
        st.write('## Resultado da classificação do chamado:')
        st.write(f'O chamado foi classificado como: **{result}**')
    else:
        st.write('## Erro')
        st.write('Não foi possível classificar o texto. Por favor, tente novamente.')
