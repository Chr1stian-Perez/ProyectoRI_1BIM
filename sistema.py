import os

def run():
    print("1. Construir índice\n2. CLI interactivo\n3. Evaluación\n4. Salir")
    c = input("Selecciona opción: ")
    if c == "1":
        os.system("python src/indexer.py")
    elif c == "2":
        os.system("python src/cli.py")
    elif c == "3":
        os.system("python src/evaluator.py")
    else:
        print("Bye!")

if __name__ == "__main__":
    run()