"""
Modelos de recuperación: TF-IDF y BM25
"""
import math
from typing import List, Tuple, Dict
from collections import defaultdict
from .utils import load_index
from .preprocesamiento import preprocess_text  # Usamos tu función de preprocesamiento

class RetrievalSystem:
    """Sistema de recuperación con TF-IDF y BM25"""

    def __init__(self, index_path: str = "data/index.pkl"):
        """
        Inicializa el sistema de recuperación

        Args:
            index_path: Ruta al archivo del índice
        """
        self._load_index(index_path)

    def _load_index(self, index_path: str):
        """Carga el índice desde disco"""
        try:
            index_data = load_index(index_path)
            self.inverted_index = index_data['inverted_index']
            self.doc_lengths = index_data['doc_lengths']
            self.doc_count = index_data['doc_count']
            self.avg_doc_length = index_data['avg_doc_length']
            print(f"Índice cargado: {self.doc_count} documentos, {len(self.inverted_index)} términos")
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el índice en {index_path}. Ejecuta primero indexer.py")

    def tfidf_search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """
        Búsqueda usando TF-IDF con similitud coseno

        Args:
            query: Consulta de texto
            k: Número de documentos a retornar

        Returns:
            Lista de (doc_id, score) ordenada por relevancia
        """
        query_terms = preprocess_text(query)  # ¡Aquí usamos lematización!
        if not query_terms:
            return []

        # Calcular vector de consulta
        query_vector = self._calculate_query_tfidf_vector(query_terms)

        # Calcular scores para todos los documentos candidatos
        doc_scores = defaultdict(float)
        doc_norms = defaultdict(float)

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            # IDF del término
            df = len(self.inverted_index[term])
            idf = math.log(self.doc_count / df)

            for doc_id, tf in self.inverted_index[term]:
                # TF-IDF del documento
                tfidf_doc = tf * idf

                # Producto punto para similitud coseno
                doc_scores[doc_id] += query_vector[term] * tfidf_doc
                doc_norms[doc_id] += tfidf_doc ** 2

        # Normalizar scores (similitud coseno)
        query_norm = math.sqrt(sum(score ** 2 for score in query_vector.values()))

        for doc_id in doc_scores:
            doc_norm = math.sqrt(doc_norms[doc_id])
            if doc_norm > 0 and query_norm > 0:
                doc_scores[doc_id] = doc_scores[doc_id] / (doc_norm * query_norm)

        # Ordenar y retornar top-k
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs[:k]

    def bm25_search(self, query: str, k: int = 10, k1: float = 1.5, b: float = 0.75) -> List[Tuple[str, float]]:
        """
        Búsqueda usando BM25

        Args:
            query: Consulta de texto
            k: Número de documentos a retornar
            k1: Parámetro de saturación de término
            b: Parámetro de normalización de longitud

        Returns:
            Lista de (doc_id, score) ordenada por relevancia
        """
        query_terms = preprocess_text(query)  # ¡Aquí usamos lematización!
        if not query_terms:
            return []

        doc_scores = defaultdict(float)

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            # IDF del término
            df = len(self.inverted_index[term])
            idf = math.log((self.doc_count - df + 0.5) / (df + 0.5))

            for doc_id, tf in self.inverted_index[term]:
                # Longitud del documento
                doc_length = self.doc_lengths.get(doc_id, 0)

                # BM25 score
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_length / self.avg_doc_length))

                bm25_component = idf * (numerator / denominator)
                doc_scores[doc_id] += bm25_component

        # Ordenar y retornar top-k
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs[:k]

    def _calculate_query_tfidf_vector(self, query_terms: List[str]) -> Dict[str, float]:
        """Calcula el vector TF-IDF de la consulta"""
        # Frecuencias de términos en la consulta
        term_freq = defaultdict(int)
        for term in query_terms:
            term_freq[term] += 1

        # Calcular TF-IDF para cada término de la consulta
        query_vector = {}
        for term, tf in term_freq.items():
            if term in self.inverted_index:
                df = len(self.inverted_index[term])
                idf = math.log(self.doc_count / df)
                query_vector[term] = tf * idf
            else:
                query_vector[term] = 0

        return query_vector
