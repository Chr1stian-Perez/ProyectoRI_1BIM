from retrieval import tfidf_search, bm25_search
import ir_datasets

def main():
    dataset = ir_datasets.load("car/v1.5/test200")
    doc_map = {doc.doc_id: doc.text for doc in dataset.docs_iter()}
    while True:
        query = input("\nConsulta (enter para salir): ")
        if not query.strip():
            break
        print("\n--- TF-IDF ---")
        for doc_id, score in tfidf_search(query):
            print(f"{doc_id[:8]}... | Score: {score:.4f}\n   {doc_map.get(doc_id, '')[:150]}")
        print("\n--- BM25 ---")
        for doc_id, score in bm25_search(query):
            print(f"{doc_id[:8]}... | Score: {score:.4f}\n   {doc_map.get(doc_id, '')[:150]}")
        print("-" * 30)
if __name__ == '__main__':
    main()