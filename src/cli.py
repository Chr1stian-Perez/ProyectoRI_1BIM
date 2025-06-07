import sys
from colorama import Fore, Style, init
from .retrieval import RetrievalSystem  # Módulo que implementa los algoritmos de búsqueda (TF-IDF, BM25)

# =======================================
# 🎨 Inicialización de Colorama
# =======================================
# Colorama permite agregar colores en terminales de forma multiplataforma (Windows, Unix, etc.)
# autoreset=True: reinicia el estilo después de cada print
# convert=True: convierte códigos ANSI para terminales que lo necesitan (como Windows CMD)
init(autoreset=True, convert=True)

# =======================================
# 🧩 Clase principal: SearchCLI
# =======================================
class SearchCLI:
    """
    Interfaz de línea de comandos (CLI) que permite hacer búsquedas sobre el corpus TREC CAR
    usando dos algoritmos de recuperación de información: TF-IDF y BM25.
    """

    def __init__(self):
        """
        Inicializa la instancia del sistema de recuperación.
        Si no se encuentra el índice, se muestra un error y el sistema finaliza.
        """
        try:
            self.retrieval_system = RetrievalSystem()  # Instancia del sistema de búsqueda (carga índices)
            print(Fore.GREEN + "✔ Sistema de recuperación cargado correctamente")
        except FileNotFoundError as e:
            # El índice no existe (probablemente no se ha generado aún)
            print(Fore.RED + f"✖ Error: {e}")
            sys.exit(1)  # Finalizar la ejecución del programa

    def run(self):
        """
        Ejecuta el menú interactivo en consola, permitiendo al usuario ingresar consultas,
        pedir ayuda, o salir del sistema.
        """
        # ======================
        # 🖼️ Banner de bienvenida
        # ======================
        print(Fore.YELLOW + "\n" + "═" * 65)
        print(Fore.WHITE + Style.BRIGHT + "╔═════════════════════════════════════════════════════════════╗")
        print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN – TREC CAR" + Fore.WHITE + "   ║")
        print("╚═════════════════════════════════════════════════════════════╝")
        print(Fore.YELLOW + "═" * 65)

        # ======================
        # 🧭 Mostrar comandos disponibles
        # ======================
        print(Fore.CYAN + Style.BRIGHT + "\nComandos disponibles:")
        print(Fore.WHITE + "  • Escribe una consulta para buscar")
        print("  • 'quit' o 'exit' para salir")
        print("  • 'help' para mostrar esta ayuda")
        print(Fore.YELLOW + "═" * 65)

        # ======================
        # 🔁 Bucle principal de la CLI
        # ======================
        while True:
            try:
                # Leer y limpiar la consulta ingresada
                query = input(Fore.BLUE + Style.BRIGHT + "\nConsulta > " + Style.RESET_ALL).strip()

                if not query:
                    continue  # Ignorar si el usuario no escribe nada

                if query.lower() in ['quit', 'exit']:
                    # Salida voluntaria del sistema
                    print(Fore.GREEN + "👋 ¡Hasta luego!")
                    break

                if query.lower() == 'help':
                    # Mostrar ayuda contextual
                    self._show_help()
                    continue

                # Procesar la consulta válida
                self._process_query(query)

            except KeyboardInterrupt:
                # Permitir salida con Ctrl+C sin error
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                # Captura de errores generales no previstos
                print(Fore.RED + f"⚠️  Error procesando consulta: {e}")

    def _process_query(self, query: str):
        """
        Procesa una consulta de texto, ejecutándola contra los dos algoritmos disponibles:
        TF-IDF y BM25, y muestra los resultados al usuario.
        """
        print(Fore.MAGENTA + f"\n🔎 Buscando: '{query}'")
        print(Fore.LIGHTBLACK_EX + "─" * 50)

        # ======================
        # 📊 Búsqueda usando TF-IDF
        # ======================
        print(Fore.CYAN + "\n📊 RESULTADOS TF-IDF:")
        tfidf_results = self.retrieval_system.tfidf_search(query, k=10)  # Obtener top-10 resultados
        self._display_results(tfidf_results)

        # ======================
        # 🎯 Búsqueda usando BM25
        # ======================
        print(Fore.MAGENTA + "\n🎯 RESULTADOS BM25:")
        bm25_results = self.retrieval_system.bm25_search(query, k=10)
        self._display_results(bm25_results)

    def _display_results(self, results: list):
        """
        Muestra los resultados de búsqueda (ID del documento y score).
        Si no hay resultados, informa al usuario.
        """
        if not results:
            print(Fore.RED + "  ⚠️  No se encontraron resultados.")
            return

        # Mostrar resultados numerados con score formateado
        for i, (doc_id, score) in enumerate(results, 1):
            print(Fore.YELLOW + f"  {i:2d}. " + 
                  Fore.WHITE + f"Doc: {doc_id[:45]:<45}" +  # Truncar ID largo
                  Fore.GREEN + f" Score: {score:.4f}")

    def _show_help(self):
        """
        Muestra una guía de uso rápida para el usuario, incluyendo ejemplos de consulta
        y descripción de los algoritmos disponibles.
        """
        print(Fore.YELLOW + "\n" + "═" * 65)
        print(Fore.CYAN + "📘 AYUDA - Sistema de Recuperación de Información")
        print(Fore.YELLOW + "═" * 65)

        # Información sobre el corpus
        print(Fore.WHITE + "Este sistema utiliza el corpus TREC CAR car/v1.5/test200")
        
        # Algoritmos disponibles
        print("\nAlgoritmos implementados:")
        print(Fore.GREEN + "  • TF-IDF con similitud coseno")
        print("  • BM25 (k1=1.5, b=0.75)")
        
        # Ejemplos útiles de consulta
        print("\nEjemplos de consultas:")
        print(Fore.BLUE + "  • 'machine learning algorithms'")
        print("  • 'neural networks deep learning'")
        print("  • 'information retrieval systems'")
        print(Fore.YELLOW + "═" * 65)

# =======================================
# 🏁 Función de entrada al programa
# =======================================
def main():
    """
    Crea una instancia del CLI y lo lanza.
    Esta es la función de entrada principal del programa.
    """
    cli = SearchCLI()
    cli.run()

# =======================================
# 🚀 Ejecutar el CLI solo si se invoca directamente
# =======================================
if __name__ == "__main__":
    main()
