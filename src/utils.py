"""
Utilidades comunes para el sistema de IR
"""
import re
import pickle
import json
from typing import List, Dict, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK si no están disponibles
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextProcessor:
    """Procesador de texto para tokenización y normalización"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def tokenize_and_normalize(self, text: str) -> List[str]:
        """
        Tokeniza y normaliza texto
        
        Args:
            text: Texto a procesar
            
        Returns:
            Lista de tokens normalizados
        """
        if not text:
            return []
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales excepto espacios
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Filtrar stopwords y tokens muy cortos
        tokens = [token for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return tokens

def save_index(index_data: Dict, filepath: str) -> None:
    """Guarda el índice en disco"""
    with open(filepath, 'wb') as f:
        pickle.dump(index_data, f)

def load_index(filepath: str) -> Dict:
    """Carga el índice desde disco"""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def save_results(results: Dict, filepath: str) -> None:
    """Guarda resultados de evaluación"""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)