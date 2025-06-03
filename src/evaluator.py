"""
Sistema de evaluación usando métricas estándar de IR
"""
import ir_datasets
from typing import Dict, List, Tuple
from .retrieval import RetrievalSystem
from .utils import save_results

class IREvaluator:
    """Evaluador del sistema de IR usando métricas estándar"""
    
    def __init__(self, dataset_name: str = "car/v1.5/test200"):
        self.dataset_name = dataset_name
        self.dataset = ir_datasets.load(dataset_name)
        self.retrieval_system = RetrievalSystem()
        
        # Cargar consultas y qrels
        self.queries = {q.query_id: q.text for q in self.dataset.queries_iter()}
        self.qrels = self._load_qrels()
        
        print(f"Cargadas {len(self.queries)} consultas")
        print(f"Cargados {len(self.qrels)} grupos de relevancia")
    
    def _load_qrels(self) -> Dict[str, Dict[str, int]]:
        """Carga los juicios de relevancia del dataset"""
        qrels = {}
        for qrel in self.dataset.qrels_iter():
            if qrel.query_id not in qrels:
                qrels[qrel.query_id] = {}
            qrels[qrel.query_id][qrel.doc_id] = qrel.relevance
        return qrels
    
    def evaluate_all_queries(self) -> Dict:
        """Evalúa todas las consultas con ambos métodos"""
        print("\nIniciando evaluación completa del sistema...")
        print("="*60)
        
        results = {
            'tfidf': {'precision': {}, 'recall': {}, 'map': 0},
            'bm25': {'precision': {}, 'recall': {}, 'map': 0},
            'summary': {}
        }
        
        tfidf_aps = []  # Average Precisions para MAP
        bm25_aps = []
        
        evaluated_queries = 0
        
        for query_id, query_text in self.queries.items():
            if query_id not in self.qrels:
                continue  # Skip queries sin qrels
            
            print(f"Evaluando consulta {evaluated_queries + 1}/{len(self.qrels)}: {query_id}")
            
            # Obtener resultados
            tfidf_results = self.retrieval_system.tfidf_search(query_text, k=100)
            bm25_results = self.retrieval_system.bm25_search(query_text, k=100)
            
            # Evaluar TF-IDF
            tfidf_metrics = self._evaluate_query(tfidf_results, self.qrels[query_id])
            results['tfidf']['precision'][query_id] = tfidf_metrics['precision']
            results['tfidf']['recall'][query_id] = tfidf_metrics['recall']
            tfidf_aps.append(tfidf_metrics['average_precision'])
            
            # Evaluar BM25
            bm25_metrics = self._evaluate_query(bm25_results, self.qrels[query_id])
            results['bm25']['precision'][query_id] = bm25_metrics['precision']
            results['bm25']['recall'][query_id] = bm25_metrics['recall']
            bm25_aps.append(bm25_metrics['average_precision'])
            
            evaluated_queries += 1
        
        # Calcular MAP
        results['tfidf']['map'] = sum(tfidf_aps) / len(tfidf_aps) if tfidf_aps else 0
        results['bm25']['map'] = sum(bm25_aps) / len(bm25_aps) if bm25_aps else 0
        
        # Calcular métricas promedio
        results['summary'] = self._calculate_summary(results, evaluated_queries)
        
        self._display_results(results)
        return results
    
    def _evaluate_query(self, retrieved_docs: List[Tuple[str, float]], 
                       relevant_docs: Dict[str, int]) -> Dict:
        """Evalúa una consulta individual"""
        if not retrieved_docs:
            return {'precision': [0]*10, 'recall': [0]*10, 'average_precision': 0}
        
        # Documentos relevantes (relevance > 0)
        relevant_set = set(doc_id for doc_id, rel in relevant_docs.items() if rel > 0)
        
        if not relevant_set:
            return {'precision': [0]*10, 'recall': [0]*10, 'average_precision': 0}
        
        # Calcular precision y recall en diferentes puntos de corte
        precisions = []
        recalls = []
        relevant_retrieved = 0
        
        # Para calcular Average Precision
        precision_at_relevant = []
        
        for i, (doc_id, score) in enumerate(retrieved_docs[:100], 1):
            if doc_id in relevant_set:
                relevant_retrieved += 1
                precision_at_relevant.append(relevant_retrieved / i)
            
            precision = relevant_retrieved / i
            recall = relevant_retrieved / len(relevant_set)
            
            # Guardar métricas en puntos específicos (cada 10 docs)
            if i % 10 == 0:
                precisions.append(precision)
                recalls.append(recall)
        
        # Calcular Average Precision
        average_precision = sum(precision_at_relevant) / len(relevant_set) if precision_at_relevant else 0
        
        return {
            'precision': precisions,
            'recall': recalls,
            'average_precision': average_precision
        }
    
    def _calculate_summary(self, results: Dict, num_queries: int) -> Dict:
        """Calcula métricas resumidas"""
        summary = {}
        
        for method in ['tfidf', 'bm25']:
            # Promedio de precision y recall en diferentes cortes
            avg_precisions = []
            avg_recalls = []
            
            for k in range(10):  # Para cada punto de corte (10, 20, ..., 100)
                precisions_at_k = [precs[k] for precs in results[method]['precision'].values()]
                recalls_at_k = [recs[k] for recs in results[method]['recall'].values()]
                
                avg_precisions.append(sum(precisions_at_k) / len(precisions_at_k))
                avg_recalls.append(sum(recalls_at_k) / len(recalls_at_k))
            
            summary[method] = {
                'avg_precision': avg_precisions,
                'avg_recall': avg_recalls,
                'map': results[method]['map']
            }
        
        return summary
    
    def _display_results(self, results: Dict):
        """Muestra los resultados de evaluación"""
        print("\n" + "="*80)
        print("RESULTADOS DE EVALUACIÓN - SISTEMA DE IR")
        print("="*80)
        
        print(f"\nDataset: {self.dataset_name}")
        print(f"Consultas evaluadas: {len(results['tfidf']['precision'])}")
        
        print("\n📊 MÉTRICAS PROMEDIO:")
        print("-" * 50)
        
        # MAP
        print(f"Mean Average Precision (MAP):")
        print(f"  TF-IDF: {results['tfidf']['map']:.4f}")
        print(f"  BM25:   {results['bm25']['map']:.4f}")
        
        # Precision y Recall promedio en diferentes cortes
        print(f"\nPrecision promedio:")
        for i, k in enumerate(range(10, 101, 10)):
            tfidf_p = results['summary']['tfidf']['avg_precision'][i]
            bm25_p = results['summary']['bm25']['avg_precision'][i]
            print(f"  P@{k:3d}: TF-IDF={tfidf_p:.4f}, BM25={bm25_p:.4f}")
        
        print(f"\nRecall promedio:")
        for i, k in enumerate(range(10, 101, 10)):
            tfidf_r = results['summary']['tfidf']['avg_recall'][i]
            bm25_r = results['summary']['bm25']['avg_recall'][i]
            print(f"  R@{k:3d}: TF-IDF={tfidf_r:.4f}, BM25={bm25_r:.4f}")
        
        # Comparación de métodos
        print(f"\n🏆 COMPARACIÓN:")
        print("-" * 30)
        better_method = "BM25" if results['bm25']['map'] > results['tfidf']['map'] else "TF-IDF"
        print(f"Mejor método por MAP: {better_method}")
        
        print("="*80)
    
    def save_results(self, results: Dict, filepath: str = "results/evaluation_results.json"):
        """Guarda los resultados de evaluación"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        save_results(results, filepath)
        print(f"\nResultados guardados en: {filepath}")

def main():
    """Función principal del evaluador"""
    evaluator = IREvaluator()
    results = evaluator.evaluate_all_queries()
    evaluator.save_results(results)

if __name__ == "__main__":
    main()