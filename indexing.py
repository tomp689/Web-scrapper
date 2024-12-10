from collections import defaultdict
import json


def create_inverted_index(documents):
    inverted_index = defaultdict(list) 
    for doc_id, text in enumerate(documents, 1): 
        tokens = text.split()  # split σε λεξεις
        for token in set(tokens):  #Σετ για να μην υπαρχουν διπλες εγγραφες
            inverted_index[token].append(doc_id)
    return inverted_index

# Φόρτωση το json αρχείο 

with open("processed_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Δημιουργία ευρετηρίου
inverted_index = create_inverted_index(documents)

#Εκτυπώση
for term, doc_ids in inverted_index.items():
    print(f"{term}: {doc_ids}")
