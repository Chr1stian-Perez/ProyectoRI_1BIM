#!/usr/bin/env python3
"""
Sistema de Recuperación de Información - TREC CAR
Script principal que coordina la construcción del índice, la consulta interactiva
y la evaluación automática del sistema.
"""

# ========================== #
#      IMPORTACIONES         #
# ========================== #

import sys       # Para salir del programa de forma segura
import os        # Para verificar la existencia de archivos (índice)
import time      # Para efectos de tiempo en animaciones
from colorama import init, Fore, Style   # Para darle color y estilo a la consola
from pyfiglet import figlet_format       # Para imprimir texto ASCII como banner

# ========================== #
#     INICIALIZACIONES       #
# ========================== #

# Inicializa colorama para habilitar soporte de colores en Windows y otros entornos
# autoreset=True reinicia colores después de cada impresión
# convert=True convierte los códigos ANSI para sistemas que lo requieren
init(autoreset=True, convert=True)

# Importar funciones principales de los módulos internos del sistema
from src.indexer import main as build_index       # Función para construir el índice invertido
from src.cli import main as run_cli               # CLI interactiva para realizar consultas
from src.evaluator import main as run_evaluation  # Evaluación automática del sistema

# ========================== #
#     FUNCIONES DE UI        #
# ========================== #

def print_banner():
    """Muestra el título del sistema en un banner estilo ASCII usando pyfiglet"""
    print(Fore.CYAN + figlet_format("TREC CAR", font="slant"))

def loading_animation():
    """Pequeña animación de carga para mejor UX (simula inicialización del sistema)"""
    print(Fore.BLUE + "🚀 Iniciando Sistema", end="", flush=True)
    for _ in range(3):  # Mostrar tres puntos con pausa
        time.sleep(0.3)
        print(".", end="", flush=True)
    print("\n")  # Salto de línea final

def show_menu():
    """Imprime el menú principal de opciones del sistema con estilo y colores"""
    print(Fore.YELLOW + "\n" + "═" * 65)
    print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════════╗")
    print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN - TREC CAR" + Fore.WHITE + "   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Fore.YELLOW + "═" * 65)

    # Imprimir opciones disponibles para el usuario
    print(Fore.WHITE + "1. 🏗️  " + Fore.CYAN + "Construir índice" + Fore.WHITE + " (una sola vez)")
    print("2. 🔍 " + Fore.CYAN + "Interfaz de consultas interactiva")
    print("3. 📊 " + Fore.CYAN + "Evaluación automática del sistema")
    print("4. 🚪 " + Fore.RED + "Salir")
    print(Fore.YELLOW + "─" * 65)

# ========================== #
#     FUNCIÓN PRINCIPAL      #
# ========================== #

def main():
    """Función principal que orquesta la ejecución del sistema"""
    
    print_banner()         # Mostrar logo inicial en ASCII
    loading_animation()    # Mostrar animación antes del menú

    # Bucle principal para mantener el menú activo hasta que el usuario salga
    while True:
        show_menu()  # Mostrar menú en cada iteración
        
        try:
            # Leer opción ingresada por el usuario
            choice = input(Fore.YELLOW + "\n🔸 Opción (1–4): " + Style.RESET_ALL).strip()

            # ========================== #
            #    OPCIÓN 1: INDEXACIÓN    #
            # ========================== #
            if choice == '1':
                print(Fore.BLUE + "\n🏗️  Construyendo índice invertido...\n")
                build_index()  # Ejecutar función que crea el índice (se guarda en disco)

            # ========================== #
            #  OPCIÓN 2: CONSULTAS CLI   #
            # ========================== #
            elif choice == '2':
                print(Fore.CYAN + "\n🔍 Iniciando interfaz de consultas...\n")

                # Verificar si el índice ya fue creado antes de permitir consultar
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue  # Regresar al menú principal

                run_cli()  # Iniciar CLI de búsqueda (modo interactivo)

            # ========================== #
            #   OPCIÓN 3: EVALUACIÓN     #
            # ========================== #
            elif choice == '3':
                print(Fore.MAGENTA + "\n📊 Ejecutando evaluación...\n")

                # Verificar que el índice esté disponible para evaluar el sistema
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue

                run_evaluation()  # Ejecutar módulo de evaluación automática (e.g., MRR, MAP)

            # ========================== #
            #       OPCIÓN 4: SALIR      #
            # ========================== #
            elif choice == '4':
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                sys.exit(0)  # Salida limpia del sistema

            # ========================== #
            #  OPCIÓN NO RECONOCIDA      #
            # ========================== #
            else:
                print(Fore.RED + "❌ Opción inválida. Por favor elige entre 1–4.")

        # ========================== #
        #  MANEJO DE INTERRUPCIONES  #
        # ========================== #
        except KeyboardInterrupt:
            print(Fore.GREEN + "\n\n👋 Interrupción detectada. Cerrando...")
            sys.exit(0)

        # ========================== #
        # MANEJO DE ERRORES GENERALES#
        # ========================== #
        except Exception as e:
            print(Fore.RED + f"\n❌ Error inesperado: {e}")

# ========================== #
#     EJECUCIÓN DEL SCRIPT   #
# ========================== #

# Punto de entrada del programa. Solo se ejecuta si este archivo es el principal
if __name__ == "__main__":
    main()
