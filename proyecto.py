#!/usr/bin/env python3
"""
Sistema de Recuperación de Información - TREC CAR
Script principal que ejecuta todo el sistema
"""
import sys
import os
from src.indexer import main as build_index
from src.cli import main as run_cli
from src.evaluator import main as run_evaluation

def show_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("SISTEMA DE RECUPERACIÓN DE INFORMACIÓN - TREC CAR")
    print("="*60)
    print("1. Construir índice (ejecutar una sola vez)")
    print("2. Interfaz de consultas interactiva")
    print("3. Evaluación automática del sistema")
    print("4. Salir")
    print("="*60)

def main():
    """Función principal del sistema"""
    print("Iniciando Sistema de Recuperación de Información...")
    
    while True:
        show_menu()
        
        try:
            choice = input("\nSelecciona una opción (1-4): ").strip()
            
            if choice == '1':
                print("\n🔧 Construyendo índice invertido...")
                build_index()
                
            elif choice == '2':
                print("\n🔍 Iniciando interfaz de consultas...")
                if not os.path.exists("data/index.pkl"):
                    print("❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_cli()
                
            elif choice == '3':
                print("\n📊 Iniciando evaluación automática...")
                if not os.path.exists("data/index.pkl"):
                    print("❌ Error: Índice no encontrado. Ejecuta primero la opción 1.")
                    continue
                run_evaluation()
                
            elif choice == '4':
                print("\n¡Hasta luego!")
                sys.exit(0)
                
            else:
                print("❌ Opción inválida. Por favor selecciona 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()