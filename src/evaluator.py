from retrieval import tfidf_search, bm25_search
import ir_datasets
from collections import defaultdict

def calculate_precision(retrieved, relevant):
    retrieved_set = set([d for d, _ in retrieved])
    relevant_set = set([d for d in relevant if relevant[d] > 0])
    return len(retrieved_set & relevant_set) / (len(retrieved_set) or 1)

def calculate_recall(retrieved, relevant):
    retrieved_set = set([d for d, _ in retrieved])
    relevant_set = set([d for d in relevant if relevant[d] > 0])
    return len(retrieved_set & relevant_set) / (len(relevant_set) or 1)

def average_precision(retrieved, relevant):
    relevant_set = set([d for d in relevant if relevant[d] > 0])
    if not relevant_set:
        return 0
    score = 0
    hits = 0
    for i, (doc_id, _) in enumerate(retrieved, 1):
        if doc_id in relevant_set:
            hits += 1
            score += hits / i
    return score / len(relevant_set)

def evaluate_all_queries(method="tfidf", k=10):
    dataset = ir_datasets.load("car/v1.5/test200")
    queries = {q.query_id: q.text for q in dataset.queries_iter()}
    qrels = defaultdict(dict)
    for q in dataset.qrels_iter():
        qrels[q.query_id][q.doc_id] = q.relevance
    precisions, recalls, aps = [], [], []
    search_fn = tfidf_search if method == "tfidf" else bm25_search
    for qid, text in queries.items():
        retrieved = search_fn(text, k=k)
        relevant = qrels[qid]
        precisions.append(calculate_precision(retrieved, relevant))
        recalls.append(calculate_recall(retrieved, relevant))
        aps.append(average_precision(retrieved, relevant))
    print(f"{method.upper()} | MAP: {sum(aps)/len(aps):.4f} | Precisión media: {sum(precisions)/len(precisions):.4f} | Recall medio: {sum(recalls)/len(recalls):.4f}")
    return sum(aps)/len(aps)

if __name__ == '__main__':
    evaluate_all_queries("tfidf")
    evaluate_all_queries("bm25")