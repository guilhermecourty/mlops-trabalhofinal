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

# Sidebar for category selection
st.sidebar.header("Precisa de ajuda?")
category = st.sidebar.selectbox(
    "Categorias exemplo",
    ["Escolha uma Categoria",
    "Hipotecas / Empréstimos",
    "Roubo / Relatório de disputa",
    "Serviços de conta bancária"
    ]
)

def display_example(text, background_color="#f0f2f6", text_color="#333"):
    """
    Display the example text in a styled bubble.
    Args:
    - text: The example text to display.
    - background_color: The background color of the bubble.
    - text_color: The text color.
    """
    html = f"""
    <div style='background-color: {background_color}; border-radius: 10px; padding: 10px; margin: 10px 0;'>
    <p style='color: {text_color}; margin:0;'>{text}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Example texts mapped to categories
example_texts = {
    "Hipotecas / Empréstimos": "Estou tentando refinanciar minha hipoteca há meses, mas não \
        consigo obter uma taxa de juros satisfatória. Preciso de orientação sobre como proceder \
            para conseguir uma melhor oferta.",
    "Roubo / Relatório de disputa": "Meu cartão de crédito foi clonado e observei transações \
        não autorizadas. Como posso contestar essas cobranças e obter um novo cartão com segurança \
            reforçada?",
    "Serviços de conta bancária": "Houve um problema com a transferência que tentei fazer para outra \
        conta. O valor foi debitado da minha conta, mas o destinatário não recebeu o dinheiro. \
            Preciso de ajuda urgente para resolver essa questão."
}

# Main area: Displaying the example based on selection
st.header("Exemplo de texto para ser Predito")
if category and category != "Escolha uma Categoria":
    st.write(f"Exemplo para **{category}**:")
    display_example(example_texts[category])
else:
    st.write("Seleciona uma Categoria de Chamados para ver o texto de exemplo.")