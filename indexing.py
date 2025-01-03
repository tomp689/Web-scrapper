from collections import defaultdict
import json


def create_inverted_index(documents):
    inverted_index = defaultdict(list) 
    for doc_id, text in enumerate(documents, 1): 
        # Split σε λέξεις
        tokens = text.split() 
        # Χρησιμοποιούμε set για να μην υπάρχουν διπλές εγγραφές
        for token in set(tokens):  
            inverted_index[token].append(doc_id)
    return inverted_index

# Φόρτωση του json αρχείου 
with open("processed_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Δημιουργία του ευρετηρίου
inverted_index = create_inverted_index(documents)

# Εκτυπώση του ευρετηρίου
for term, doc_ids in inverted_index.items():
    print(f"{term}: {doc_ids}")
