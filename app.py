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
    api_url = 'https://functionappdecria.azurewebsites.net/api/predictnlpdecria'
    headers = {'x-functions-key': 'valuedecria'}
    response = requests.post(api_url, json={'data': text_input}, headers=headers)
    
    # Display the classification result
    if response.status_code == 200:
        # print(response)
        # print(response.text)
        result = response.text
        # result = response.json()
        st.write('## Resultado da classificação do chamado:')
        st.markdown(f'O chamado foi classificado como: <span style="color:green"><b>{result}</b></span>', unsafe_allow_html=True)
    else:
        st.write('## Erro')
        st.write('Não foi possível classificar o texto. Por favor, tente novamente.')
        # Print error
        st.write(response.text)
