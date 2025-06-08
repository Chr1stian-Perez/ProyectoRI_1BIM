import sys
from colorama import Fore, Style, init
from .retrieval import RetrievalSystem
from .utils import get_doc_text_by_id # Importa la función para recuperar el texto

# Inicializar colorama correctamente
init(autoreset=True, convert=True)
class SearchCLI:
    """Interfaz de línea de comandos para búsquedas"""
    def __init__(self):
        try:
            self.retrieval_system = RetrievalSystem()
            print(Fore.GREEN + "✔ Sistema de recuperación cargado correctamente")
        except FileNotFoundError as e:
            print(Fore.RED + f"✖ Error: {e}")
            sys.exit(1)

    def run(self):
        """Ejecuta la interfaz interactiva"""

        # Mensaje de bienvenida visible y colorido
        print(Fore.YELLOW + "\n" + "═" * 65)
        print(Fore.WHITE + Style.BRIGHT + "╔═════════════════════════════════════════════════════════════╗")
        print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN – TREC CAR" + Fore.WHITE + "   ║")
        print("╚═════════════════════════════════════════════════════════════╝")
        print(Fore.YELLOW + "═" * 65)

        print(Fore.CYAN + Style.BRIGHT + "\nComandos disponibles:")
        print(Fore.WHITE + "  • Escribe una consulta para buscar")
        print("  • 'quit' o 'exit' para salir")
        print("  • 'help' para mostrar esta ayuda")
        print(Fore.YELLOW + "═" * 65)

        while True:
            try:
                query = input(Fore.BLUE + Style.BRIGHT + "\nConsulta > " + Style.RESET_ALL).strip()

                if not query:
                    continue

                if query.lower() in ['quit', 'exit']:
                    print(Fore.GREEN + "👋 ¡Hasta luego!")
                    break

                if query.lower() == 'help':
                    self._show_help()
                    continue

                self._process_query(query)

            except KeyboardInterrupt:
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(Fore.RED + f"⚠️  Error procesando consulta: {e}")

    def _process_query(self, query: str):
        """Procesa una consulta y muestra resultados"""
        print(Fore.MAGENTA + f"\n🔎 Buscando: '{query}'")
        print(Fore.LIGHTBLACK_EX + "─" * 50)

        # TF-IDF
        print(Fore.CYAN + "\n📊 RESULTADOS TF-IDF:")
        tfidf_results = self.retrieval_system.tfidf_search(query, k=10)
        self._display_results(tfidf_results)

        # BM25
        print(Fore.MAGENTA + "\n🎯 RESULTADOS BM25:")
        bm25_results = self.retrieval_system.bm25_search(query, k=10)
        self._display_results(bm25_results)

    def _display_results(self, results: list):
        """Muestra el ranking, el doc_id, los primeros 50 caracteres del texto y el score"""
        if not results:
            print(Fore.RED + "  ⚠️  No se encontraron resultados.")
            return

        print(Fore.YELLOW + f"\n{'#':>2}  {'DocID':<45} {'Texto':<53} {'Score':>8}")
        print(Fore.YELLOW + "-" * 110)
        for i, (doc_id, score) in enumerate(results, 1):
            doc_text = get_doc_text_by_id(doc_id, self.retrieval_system.doc_texts)
            resumen = doc_text[:50].replace('\n', ' ') if doc_text else "[Sin texto]"
            print(
                Fore.YELLOW + f"{i:2d}. " +
                Fore.WHITE + f"{doc_id[:45]:<45} " +
                Fore.LIGHTBLUE_EX + f"{resumen:<53}" +
                Fore.GREEN + f"{score:8.4f}"
            )

    def _show_help(self):
        """Muestra ayuda detallada"""
        print(Fore.YELLOW + "\n" + "═" * 65)
        print(Fore.CYAN + "📘 AYUDA - Sistema de Recuperación de Información")
        print(Fore.YELLOW + "═" * 65)
        print(Fore.WHITE + "Este sistema utiliza el corpus TREC CAR car/v1.5/test200")
        print("\nAlgoritmos implementados:")
        print(Fore.GREEN + "  • TF-IDF con similitud coseno")
        print("  • BM25 (k1=1.5, b=0.75)")
        print("\nEjemplos de consultas:")
        print(Fore.BLUE + "  • 'machine learning algorithms'")
        print("  • 'neural networks deep learning'")
        print("  • 'information retrieval systems'")
        print(Fore.YELLOW + "═" * 65)

def main():
    """Función principal de la CLI"""
    cli = SearchCLI()
    cli.run()

if __name__ == "__main__":
    main()