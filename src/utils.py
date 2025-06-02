import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

def tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS]

def compute_idf(inverted_index, N):
    import math
    idf = {}
    for term, postings in inverted_index.items():
        df = len(postings)
        idf[term] = math.log((N + 1) / (df + 1)) + 1
    return idf