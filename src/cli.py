"""
Interfaz de línea de comandos para consultas interactivas
"""
import sys
from .retrieval import RetrievalSystem

class SearchCLI:
    """Interfaz de línea de comandos para búsquedas"""
    
    def __init__(self):
        try:
            self.retrieval_system = RetrievalSystem()
            print("Sistema de recuperación cargado correctamente")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def run(self):
        """Ejecuta la interfaz interactiva"""
        print("\n" + "="*60)
        print("SISTEMA DE RECUPERACIÓN DE INFORMACIÓN - TREC CAR")
        print("="*60)
        print("Comandos disponibles:")
        print("  - Escribe una consulta para buscar")
        print("  - 'quit' o 'exit' para salir")
        print("  - 'help' para mostrar esta ayuda")
        print("="*60)
        
        while True:
            try:
                query = input("\nConsulta > ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit']:
                    print("¡Hasta luego!")
                    break
                
                if query.lower() == 'help':
                    self._show_help()
                    continue
                
                self._process_query(query)
                
            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"Error procesando consulta: {e}")
    
    def _process_query(self, query: str):
        """Procesa una consulta y muestra resultados"""
        print(f"\nBuscando: '{query}'")
        print("-" * 50)
        
        # Búsqueda con TF-IDF
        print("\n📊 RESULTADOS TF-IDF:")
        tfidf_results = self.retrieval_system.tfidf_search(query, k=10)
        self._display_results(tfidf_results, "TF-IDF")
        
        # Búsqueda con BM25
        print("\n🎯 RESULTADOS BM25:")
        bm25_results = self.retrieval_system.bm25_search(query, k=10)
        self._display_results(bm25_results, "BM25")
    
    def _display_results(self, results: list, method: str):
        """Muestra los resultados de búsqueda"""
        if not results:
            print(f"  No se encontraron resultados con {method}")
            return
        
        for i, (doc_id, score) in enumerate(results, 1):
            print(f"  {i:2d}. Doc: {doc_id[:50]:<50} Score: {score:.4f}")
    
    def _show_help(self):
        """Muestra ayuda detallada"""
        print("\n" + "="*60)
        print("AYUDA - Sistema de Recuperación de Información")
        print("="*60)
        print("Este sistema utiliza el corpus TREC CAR car/v1.5/test200")
        print("\nAlgoritmos implementados:")
        print("  • TF-IDF con similitud coseno")
        print("  • BM25 (k1=1.5, b=0.75)")
        print("\nEjemplos de consultas:")
        print("  • 'machine learning algorithms'")
        print("  • 'neural networks deep learning'")
        print("  • 'information retrieval systems'")
        print("="*60)

def main():
    """Función principal de la CLI"""
    cli = SearchCLI()
    cli.run()

if __name__ == "__main__":
    main()