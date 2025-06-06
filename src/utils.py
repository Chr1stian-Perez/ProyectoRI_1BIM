"""
Utilidades comunes para el sistema de IR
"""
import pickle
import json
from typing import Dict
import ir_datasets  # Para la función de recuperación de texto por ID

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

