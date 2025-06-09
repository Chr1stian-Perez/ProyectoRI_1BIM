import sys
from colorama import Fore, Style, init
from .retrieval import RetrievalSystem
from .utils import get_doc_text_by_id  # Utilidad para recuperar texto completo de un documento por ID

# Inicializa colorama para aplicar estilos ANSI compatibles en todas las plataformas
init(autoreset=True, convert=True)

class SearchCLI:
    """
    Interfaz de línea de comandos para realizar búsquedas interactivas
    sobre el índice construido a partir del corpus TREC CAR.
    """

    def __init__(self):
        """
        Inicializa el sistema de recuperación.
        Verifica que el índice y documentos estén cargados correctamente.
        """
        try:
            self.retrieval_system = RetrievalSystem()
            print(Fore.GREEN + "✔ Sistema de recuperación cargado correctamente")
        except FileNotFoundError as e:
            # Si no se encuentra el índice o los datos, se termina el programa con mensaje de error.
            print(Fore.RED + f"✖ Error: {e}")
            sys.exit(1)

    def run(self):
        """
        Ejecuta el bucle interactivo de consulta.
        Permite al usuario ingresar consultas y recibir resultados por consola.
        """
        # Presentación visual del sistema
        print(Fore.YELLOW + "\n" + "═" * 65)
        print(Fore.WHITE + Style.BRIGHT + "╔═════════════════════════════════════════════════════════════╗")
        print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN – TREC CAR" + Fore.WHITE + "   ║")
        print("╚═════════════════════════════════════════════════════════════╝")
        print(Fore.YELLOW + "═" * 65)

        # Instrucciones básicas
        print(Fore.CYAN + Style.BRIGHT + "\nComandos disponibles:")
        print(Fore.WHITE + "  • Escribe una consulta para buscar")
        print("  • 'quit' o 'exit' para salir")
        print("  • 'help' para mostrar esta ayuda")
        print(Fore.YELLOW + "═" * 65)

        # Bucle principal de interacción
        while True:
            try:
                query = input(Fore.BLUE + Style.BRIGHT + "\nConsulta > " + Style.RESET_ALL).strip()

                if not query:
                    continue  # Si el usuario no escribe nada, simplemente repite el prompt

                if query.lower() in ['quit', 'exit']:
                    print(Fore.GREEN + "👋 ¡Hasta luego!")
                    break

                if query.lower() == 'help':
                    self._show_help()
                    continue

                # Procesa la consulta ingresada
                self._process_query(query)

            except KeyboardInterrupt:
                # Permite salir con Ctrl+C
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                # Captura errores inesperados en tiempo de ejecución
                print(Fore.RED + f"⚠️  Error procesando consulta: {e}")

    def _process_query(self, query: str):
        """
        Realiza la búsqueda usando dos algoritmos (TF-IDF y BM25)
        y muestra los resultados por consola.
        """
        print(Fore.MAGENTA + f"\n🔎 Buscando: '{query}'")
        print(Fore.LIGHTBLACK_EX + "─" * 50)

        # Resultados con TF-IDF
        print(Fore.CYAN + "\n📊 RESULTADOS TF-IDF:")
        tfidf_results = self.retrieval_system.tfidf_search(query, k=10)
        self._display_results(tfidf_results)

        # Resultados con BM25
        print(Fore.MAGENTA + "\n🎯 RESULTADOS BM25:")
        bm25_results = self.retrieval_system.bm25_search(query, k=10)
        self._display_results(bm25_results)

    def _display_results(self, results: list):
        """
        Formatea e imprime los resultados de búsqueda.
        Muestra: posición, ID del documento, fragmento de texto y score.
        """
        if not results:
            print(Fore.RED + "  ⚠️  No se encontraron resultados.")
            return

        # Cabecera de la tabla de resultados
        print(Fore.YELLOW + f"\n{'#':>2}  {'DocID':<45} {'Texto':<53} {'Score':>8}")
        print(Fore.YELLOW + "-" * 110)

        for i, (doc_id, score) in enumerate(results, 1):
            # Extrae un fragmento del texto asociado al doc_id (si está disponible)
            doc_text = get_doc_text_by_id(doc_id, self.retrieval_system.doc_texts)
            resumen = doc_text[:50].replace('\n', ' ') if doc_text else "[Sin texto]"

            # Imprime el resultado con colores diferenciados
            print(
                Fore.YELLOW + f"{i:2d}. " +
                Fore.WHITE + f"{doc_id[:45]:<45} " +
                Fore.LIGHTBLUE_EX + f"{resumen:<53}" +
                Fore.GREEN + f"{score:8.4f}"
            )

    def _show_help(self):
        """
        Muestra información sobre el sistema, algoritmos y ejemplos de uso.
        """
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
    """
    Punto de entrada para ejecutar la interfaz CLI.
    """
    cli = SearchCLI()
    cli.run()

# Permite que el script se ejecute directamente
if __name__ == "__main__":
    main()
