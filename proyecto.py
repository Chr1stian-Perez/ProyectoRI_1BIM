#!/usr/bin/env python3
"""
Sistema de Recuperación de Información - TREC CAR
Script principal que ejecuta todo el sistema mediante un menú interactivo.
"""

import sys
import os
import time
from colorama import init, Fore, Style
from pyfiglet import figlet_format

# Inicializa colorama para el manejo de colores en la terminal,
# con soporte multiplataforma (Windows incluido)
init(autoreset=True, convert=True)

# Importa las funciones principales del sistema desde sus respectivos módulos
from src.indexer import main as build_index
from src.cli import main as run_cli
from src.evaluator import main as run_evaluation

def print_banner():
    """
    Muestra el nombre del sistema en arte ASCII
    utilizando pyfiglet para destacar el título.
    """
    print(Fore.CYAN + figlet_format("TREC CAR", font="slant"))

def loading_animation():
    """
    Animación de carga simulada para mejorar la experiencia visual.
    """
    print(Fore.BLUE + "🚀 Iniciando Sistema", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print("\n")

def show_menu():
    """
    Muestra el menú principal del sistema con opciones numeradas,
    estilo decorativo y colores diferenciados por acción.
    """
    print(Fore.YELLOW + "\n" + "═" * 65)
    print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════════╗")
    print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN - TREC CAR" + Fore.WHITE + "      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Fore.YELLOW + "═" * 65)
    print(Fore.WHITE + "1. 🏗️  " + Fore.CYAN + "Construir índice" + Fore.WHITE + " (una sola vez)")
    print("2. 🔍 " + Fore.CYAN + "Interfaz de consultas interactiva")
    print("3. 📊 " + Fore.CYAN + "Evaluación automática del sistema")
    print("4. 🚪 " + Fore.RED + "Salir")
    print(Fore.YELLOW + "─" * 65)

def main():
    """
    Función principal que controla el flujo del sistema.
    Permite al usuario elegir entre construir el índice, ejecutar la interfaz
    de búsqueda o realizar una evaluación del sistema.
    """
    print_banner()
    loading_animation()

    while True:
        show_menu()
        
        try:
            choice = input(Fore.YELLOW + "\n🔸 Opción (1–4): " + Style.RESET_ALL).strip()
            
            if choice == '1':
                # Construcción del índice invertido
                print(Fore.BLUE + "\n🏗️  Construyendo índice invertido...\n")
                build_index()
                
            elif choice == '2':
                # Inicia la interfaz de búsqueda interactiva
                print(Fore.CYAN + "\n🔍 Iniciando interfaz de consultas...\n")
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_cli()
                
            elif choice == '3':
                # Lanza el proceso de evaluación del sistema de recuperación
                print(Fore.MAGENTA + "\n📊 Ejecutando evaluación...\n")
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_evaluation()
                
            elif choice == '4':
                # Finaliza el programa de forma amigable
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                sys.exit(0)
                
            else:
                # Entrada no válida
                print(Fore.RED + "❌ Opción inválida. Por favor elige entre 1–4.")
                
        except KeyboardInterrupt:
            # Maneja la interrupción manual (Ctrl+C)
            print(Fore.GREEN + "\n\n👋 Interrupción detectada. Cerrando...")
            sys.exit(0)
        except Exception as e:
            # Captura cualquier otro error inesperado
            print(Fore.RED + f"\n❌ Error inesperado: {e}")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
