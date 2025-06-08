# preprocesamiento.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Descargar recursos (solo si no están ya descargados)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text: str):
    """
    Realiza preprocesamiento: minúsculas, tokenización, stopwords, lematización
    Solo usa NLTK. Devuelve lista de tokens procesados.
    """
    if not text:
        return []
    # Minúsculas
    text = text.lower()
    # Tokenizar
    tokens = word_tokenize(text)
    # Eliminar stopwords y tokens no alfabéticos
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    # Lematización
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens
