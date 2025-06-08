"""
Utilidades comunes para el sistema de IR
"""
import pickle
import json
from typing import Dict

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

def get_doc_text_by_id(doc_id, doc_texts):
    """
    Devuelve el texto del documento a partir de su doc_id usando el diccionario doc_texts cargado en memoria.
    """
    return doc_texts.get(doc_id, "[No se ha encontrado texto]")