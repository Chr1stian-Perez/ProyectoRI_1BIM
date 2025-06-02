import pickle
import numpy as np
from utils import tokenize, compute_idf

def load_index():
    with open('data/index.pkl', 'rb') as f:
        d = pickle.load(f)
    return d['index'], d['lengths'], d['N']

def tfidf_search(query, k=10):
    index, doc_lengths, N = load_index()
    idf = compute_idf(index, N)
    q_tokens = tokenize(query)
    docs = {}
    q_tf = {}
    for t in q_tokens:
        q_tf[t] = q_tf.get(t, 0) + 1
    query_vec = []
    vocab = list(index.keys())
    for term in vocab:
        query_vec.append(q_tf.get(term, 0) * idf.get(term, 0))
    query_vec = np.array(query_vec)
    doc_vecs = {}
    for i, term in enumerate(vocab):
        for doc_id, tf in index[term]:
            if doc_id not in doc_vecs:
                doc_vecs[doc_id] = np.zeros(len(vocab))
            doc_vecs[doc_id][i] = tf * idf[term]
    results = []
    q_norm = np.linalg.norm(query_vec)
    for doc_id, vec in doc_vecs.items():
        sim = np.dot(query_vec, vec) / (q_norm * np.linalg.norm(vec) + 1e-9)
        results.append((doc_id, sim))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]

def bm25_search(query, k=10, k1=1.5, b=0.75):
    index, doc_lengths, N = load_index()
    idf = compute_idf(index, N)
    q_tokens = tokenize(query)
    import numpy as np
    avgdl = np.mean(list(doc_lengths.values()))
    scores = {}
    for term in set(q_tokens):
        if term not in index:
            continue
        idf_term = idf[term]
        for doc_id, tf in index[term]:
            dl = doc_lengths[doc_id]
            score = idf_term * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
            scores[doc_id] = scores.get(doc_id, 0) + score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:k]