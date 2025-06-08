"""
Construcción del índice invertido con preprocesamiento (lematización NLTK)
y límite de documentos a indexar
"""
import os
import sys
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import ir_datasets
from .utils import save_index
from .preprocesamiento import preprocess_text  # Importa la función de lematización

class InvertedIndexBuilder:
    """Constructor del índice invertido"""

    def __init__(self):
        self.inverted_index = defaultdict(list)  # {término: [(doc_id, tf), ...]}
        self.doc_lengths = {}  # {doc_id: longitud}
        self.doc_count = 0
        self.total_doc_length = 0
        self.doc_texts = {}  

    def build_index(self, dataset_name: str = "car/v1.5/test200", max_docs: int = 3500000):
        """
        Construye el índice invertido desde el dataset TREC CAR,
        limitando la cantidad de documentos a indexar.

        Args:
            dataset_name: Nombre del dataset
            max_docs: Número máximo de documentos a procesar
        """
        print(f"Cargando dataset {dataset_name}...")
        dataset = ir_datasets.load(dataset_name)

        print(f"Construyendo índice invertido con lematización (NLTK)... (máx {max_docs} documentos)")

        for doc in dataset.docs_iter():
            if self.doc_count >= max_docs:
                print(f"Límite de {max_docs} documentos alcanzado. Deteniendo el indexado.")
                break
            self._process_document(doc.doc_id, doc.text)

            if self.doc_count % 1000 == 0 and self.doc_count > 0:
                print(f"Procesados {self.doc_count} documentos...")

        # Calcular longitud promedio de documentos
        self.avg_doc_length = self.total_doc_length / self.doc_count if self.doc_count > 0 else 0

        print(f"Índice construido: {self.doc_count} documentos, {len(self.inverted_index)} términos únicos")
        print(f"Longitud promedio de documento: {self.avg_doc_length:.2f}")

    def _process_document(self, doc_id: str, text: str):
        """Procesa un documento individual con preprocesamiento (lematización)"""
        tokens = preprocess_text(text)  # Lematización y preprocesamiento
        if not tokens:
            return
        self.doc_texts[doc_id] = text  # GUARDA EL TEXTO DEL DOC

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
            'total_doc_length': self.total_doc_length,
            'doc_texts': self.doc_texts  #GUARDA EL DICCIONARIO
        }

        save_index(index_data, filepath)
        print(f"Índice guardado en {filepath}")

def main():
    """Función principal para construcción del índice"""
    builder = InvertedIndexBuilder()
    # número máximo de documentos
    builder.build_index(max_docs=3500000)
    builder.save_index()

if __name__ == "__main__":
    main()
