import azure.functions as func
import logging
import json
import joblib
from azure.storage.blob import BlobClient
from io import BytesIO
import os
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import wordnet, stopwords

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="predictnlpdecria")
def predictnlpdecria(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

        logs = []
        req_body = req.get_json()
        
        # Set up Azure Blob Storage client using SAS URL
        bestpicklemodel = os.environ["bestmodelpickle"]
        tfidf = os.environ["tfidfpickle"]
        
        # Load the model
        blob_client = BlobClient.from_blob_url(bestpicklemodel)
        model_stream = BytesIO(blob_client.download_blob().readall())
        best_model = joblib.load(model_stream)
        logs.append("carregou modelo")

        # Load the Vectorizer
        blob_client = BlobClient.from_blob_url(tfidf)
        model_stream = BytesIO(blob_client.download_blob().readall())
        tfidf_vectorizer = joblib.load(model_stream)
        logs.append("carregou vetorizador")
        
        # Preprocessing
        input_data = req_body.get('data')
        preprocessed_text = preprocess_text(input_data)
        X_tfidf = tfidf_vectorizer.transform([preprocessed_text])
        logs.append("preprocessou")

        # Make prediction
        prediction = best_model.predict(X_tfidf)
        logs.append(f"predizeu")
        
        response = prediction[0] if prediction else "Outros"

        return func.HttpResponse(
            response,
            status_code=200
        )

    except ValueError as e:
        return func.HttpResponse(
            "The following error occurred: " + str(e) + ". Logs: " + ", ".join(logs),
            status_code=500
        )


# Função de pré-processamento para texto: limpeza, tokenização e lematização
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Mapeia tag POS para o primeiro caractere que lemmatize() aceita"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def preprocess_text(text):
    """Tokenização e lematização"""
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove números
    text = re.sub(r'\W+', ' ', text)  # Remove caracteres especiais
    tokens = nltk.word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in tokens]
    return ' '.join(lemmatized)