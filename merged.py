import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from collections import defaultdict
import json
from nltk.tokenize import RegexpTokenizer

# load data
with open("processed_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Ελέγξτε τη δομή των δεδομένων
if isinstance(documents, list):
    doc_ids = list(range(len(documents)))  #κανοντας την λιστα ως λεξικο
    doc_texts = documents
elif isinstance(documents, dict):
    doc_ids = list(documents.keys())
    doc_texts = list(documents.values())
else:
    raise ValueError("Unsupported JSON structure")

# Δημιουργία ανεστραμμένου ευρετηρίου για Boolean Retrieval
def create_inverted_index(documents):
    inverted_index = defaultdict(list)
    for doc_id, text in zip(doc_ids, documents):
        tokens = text.split()
        for token in set(tokens):
            inverted_index[token].append(doc_id)
    return inverted_index

inverted_index = create_inverted_index(doc_texts)

def tokenization(query):
    # Turn the query into lowercase    
    lowered_query = query.lower()

    # Split lowered query into tokens and remove all punctuation with NTLK's tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    query_tokens = tokenizer.tokenize(lowered_query)

    return query_tokens

def boolean_retrieval(query, inverted_index, operator="AND"):
    terms = query.split()
    if operator == "AND":
        result = set(inverted_index.get(terms[0], []))
        for term in terms[1:]:
            result &= set(inverted_index.get(term, []))
        return list(result)
    elif operator == "OR":
        result = set()
        for term in terms:
            result |= set(inverted_index.get(term, []))
        return list(result)
    elif operator == "NOT":
        result = set(doc_ids)
        for term in terms:
            result -= set(inverted_index.get(term, []))
        return list(result)
    else:
        raise ValueError("Invalid Boolean operator")

# TF-IDF algorithm
def tfidf_ranking(query, documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    ranked_indices = np.argsort(scores)[::-1]
    return [(doc_ids[i], scores[i]) for i in ranked_indices]

# BM25 algorithm
def bm25_ranking(query, documents):
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    ranked_indices = np.argsort(scores)[::-1]
    return [(doc_ids[i], scores[i]) for i in ranked_indices]

# Query χρηστη
query = input("Enter your search query: ")

# επιλογη αλγοριθμου
print("\nSelect retrieval algorithm:")
print("1. Boolean Retrieval (AND)")
print("2. Boolean Retrieval (OR)")
print("3. Boolean Retrieval (NOT)")
print("4. TF-IDF")
print("5. BM25")
choice = int(input("Enter choice (1/2/3/4/5): "))

if choice == 1:
    results = boolean_retrieval(query, inverted_index, operator="AND")
elif choice == 2:
    results = boolean_retrieval(query, inverted_index, operator="OR")
elif choice == 3:
    results = boolean_retrieval(query, inverted_index, operator="NOT")
elif choice == 4:
    results = tfidf_ranking(query, doc_texts)
elif choice == 5:
    results = bm25_ranking(query, doc_texts)
else:
    print("Invalid choice")
    results = []

# Αποτελεσματα
print("\nResults:")
if choice in [1, 2, 3]:
    for doc_id in results:
        print(f"Document ID: {doc_id}")
else:
    for rank, (doc_id, score) in enumerate(results, start=1):
        print(f"{rank}. Document ID: {doc_id}, Score: {score:.4f}")

