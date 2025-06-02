# Sistema de Recuperación de Información TREC CAR

## Estructura:
- src/indexer.py: Genera el índice invertido y longitudes.
- src/retrieval.py: Modelos TF-IDF y BM25.
- src/cli.py: Interfaz interactiva.
- src/evaluator.py: Evalúa Precision, Recall y MAP.
- data/index.pkl: Persistencia del índice.

## Comandos de ejecución
1. Construir índice:
    python src/indexer.py
2. CLI interactivo:
    python src/cli.py
3. Evaluación:
    python src/evaluator.py
4. Menú principal:
    python sistema.py