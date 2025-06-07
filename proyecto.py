#!/usr/bin/env python3
"""
Sistema de Recuperación de Información - TREC CAR
Script principal que ejecuta todo el sistema
"""

import sys
import os
import time
from colorama import init, Fore, Style
from pyfiglet import figlet_format

# Inicializar colorama
init(autoreset=True, convert=True)

from src.indexer import main as build_index
from src.cli import main as run_cli
from src.evaluator import main as run_evaluation

def print_banner():
    """Muestra el logo del sistema en ASCII"""
    print(Fore.CYAN + figlet_format("TREC CAR", font="slant"))

def loading_animation():
    """Animación inicial de carga"""
    print(Fore.BLUE + "🚀 Iniciando Sistema", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print("\n")

def show_menu():
    """Muestra el menú principal con colores y estilo"""
    print(Fore.YELLOW + "\n" + "═" * 65)
    print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════════╗")
    print("║   " + Fore.CYAN + "SISTEMA DE RECUPERACIÓN DE INFORMACIÓN - TREC CAR" + Fore.WHITE + "   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Fore.YELLOW + "═" * 65)
    print(Fore.WHITE + "1. 🏗️  " + Fore.CYAN + "Construir índice" + Fore.WHITE + " (una sola vez)")
    print("2. 🔍 " + Fore.CYAN + "Interfaz de consultas interactiva")
    print("3. 📊 " + Fore.CYAN + "Evaluación automática del sistema")
    print("4. 🚪 " + Fore.RED + "Salir")
    print(Fore.YELLOW + "─" * 65)

def main():
    print_banner()
    loading_animation()

    while True:
        show_menu()
        
        try:
            choice = input(Fore.YELLOW + "\n🔸 Opción (1–4): " + Style.RESET_ALL).strip()
            
            if choice == '1':
                print(Fore.BLUE + "\n🏗️  Construyendo índice invertido...\n")
                build_index()
                
            elif choice == '2':
                print(Fore.CYAN + "\n🔍 Iniciando interfaz de consultas...\n")
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_cli()
                
            elif choice == '3':
                print(Fore.MAGENTA + "\n📊 Ejecutando evaluación...\n")
                if not os.path.exists("data/index.pkl"):
                    print(Fore.RED + "❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_evaluation()
                
            elif choice == '4':
                print(Fore.GREEN + "\n👋 ¡Hasta luego!")
                sys.exit(0)
                
            else:
                print(Fore.RED + "❌ Opción inválida. Por favor elige entre 1–4.")
                
        except KeyboardInterrupt:
            print(Fore.GREEN + "\n\n👋 Interrupción detectada. Cerrando...")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
