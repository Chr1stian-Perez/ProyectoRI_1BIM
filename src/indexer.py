"""
Construcción del índice invertido
"""
import os
import sys
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import ir_datasets
from .utils import TextProcessor, save_index

class InvertedIndexBuilder:
    """Constructor del índice invertido"""
    
    def __init__(self):
        self.processor = TextProcessor()
        self.inverted_index = defaultdict(list)  # {término: [(doc_id, tf), ...]}
        self.doc_lengths = {}  # {doc_id: longitud}
        self.doc_count = 0
        self.total_doc_length = 0
    
    def build_index(self, dataset_name: str = "car/v1.5/test200"):
        """
        Construye el índice invertido desde el dataset TREC CAR
        
        Args:
            dataset_name: Nombre del dataset
        """
        print(f"Cargando dataset {dataset_name}...")
        dataset = ir_datasets.load(dataset_name)
        
        print("Construyendo índice invertido...")
        
        for doc in dataset.docs_iter():
            self._process_document(doc.doc_id, doc.text)
            
            if self.doc_count % 1000 == 0:
                print(f"Procesados {self.doc_count} documentos...")
        
        # Calcular longitud promedio de documentos
        self.avg_doc_length = self.total_doc_length / self.doc_count if self.doc_count > 0 else 0
        
        print(f"Índice construido: {self.doc_count} documentos, {len(self.inverted_index)} términos únicos")
        print(f"Longitud promedio de documento: {self.avg_doc_length:.2f}")
    
    def _process_document(self, doc_id: str, text: str):
        """Procesa un documento individual"""
        tokens = self.processor.tokenize_and_normalize(text)
        
        if not tokens:
            return
        
        # Contar frecuencias de términos
        term_frequencies = Counter(tokens)
        doc_length = len(tokens)
        
        # Actualizar índice invertido
        for term, tf in term_frequencies.items():
            self.inverted_index[term].append((doc_id, tf))
        
        # Guardar longitud del documento
        self.doc_lengths[doc_id] = doc_length
        self.total_doc_length += doc_length
        self.doc_count += 1
    
    def save_index(self, filepath: str = "data/index.pkl"):
        """Guarda el índice en disco"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        index_data = {
            'inverted_index': dict(self.inverted_index),
            'doc_lengths': self.doc_lengths,
            'doc_count': self.doc_count,
            'avg_doc_length': self.avg_doc_length,
            'total_doc_length': self.total_doc_length
        }
        
        save_index(index_data, filepath)
        print(f"Índice guardado en {filepath}")

def main():
    """Función principal para construcción del índice"""
    builder = InvertedIndexBuilder()
    builder.build_index()
    builder.save_index()

if __name__ == "__main__":
    main()