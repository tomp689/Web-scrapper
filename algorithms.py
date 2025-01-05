import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import json

#need scikit-learn
#also need rank_bm25
#οι βιβλιοθηκες παρεχουν τους αλγοριθμους που χρειαζομαστε

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

# Boolean Retrieval
def boolean_retrieval(query, documents):
    query_terms = set(query.split())
    results = []
    for doc_id, doc in zip(doc_ids, documents):
        doc_terms = set(doc.split())
        if query_terms.issubset(doc_terms):  
            results.append(doc_id)
    return results

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
print("Select retrieval algorithm:")
print("1. Boolean Retrieval")
print("2. TF-IDF")
print("3.  BM25")
choice = int(input("Enter choice (1/2/3): "))

if choice == 1:
    results = boolean_retrieval(query, doc_texts)
    print("\nBoolean Retrieval Results:")
    for doc_id in results:
        print(f"Document ID: {doc_id}")
elif choice == 2:
    results = tfidf_ranking(query, doc_texts)
    print("\nTF-IDF Results:")
    for rank, (doc_id, score) in enumerate(results, start=1):
        print(f"{rank}. Document ID: {doc_id}, Score: {score:.4f}")
elif choice == 3:
    results = bm25_ranking(query, doc_texts)
    print("\nBM25 Results:")
    for rank, (doc_id, score) in enumerate(results, start=1):
        print(f"{rank}. Document ID: {doc_id}, Score: {score:.4f}")
else:
    print("Invalid choice")
