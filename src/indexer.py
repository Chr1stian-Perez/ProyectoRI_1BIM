import pickle
import ir_datasets
from utils import tokenize

def build_inverted_index(documents):
    inverted = {}
    doc_lengths = {}
    for doc in documents:
        tokens = tokenize(doc.text)
        doc_lengths[doc.doc_id] = len(tokens)
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        for term, count in freq.items():
            inverted.setdefault(term, []).append((doc.doc_id, count))
    return inverted, doc_lengths

if __name__ == '__main__':
    dataset = ir_datasets.load("car/v1.5/test200")
    docs = list(dataset.docs_iter())
    inverted, doc_lengths = build_inverted_index(docs)
    with open('data/index.pkl', 'wb') as f:
        pickle.dump({'index': inverted, 'lengths': doc_lengths, 'N': len(docs)}, f)
    print("Índice invertido generado y guardado en data/index.pkl")