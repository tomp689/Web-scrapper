import string
import json
import nltk
from nltk.tokenize import RegexpTokenizer
import nltk.corpus
from indexing import inverted_index

query = []
unprocessed = []

print("Give at least one word, press enter when you're done.\n")


query = input()

def tokenization(query):
    # Τα γράμματα του ερωτήματος μετατρέπονται σε μικρά     
    lowered_query = query.lower()

    # Χωρίζεται το ερώτημα σε tokens και αφαιρούνται σημεία στίξης και άλλα σύμβολα με τον tokenizer της NLTK
    tokenizer = RegexpTokenizer(r'\w+')

    query_tokens = tokenizer.tokenize(lowered_query)

    return query_tokens
    
tokens = tokenization(query)


def not_processing(tokens):
        not_index = []
        not_res = []

        # Βρίσκεται ο δείκτης του "not" ώστε ο όρος που ακολουθεί να βρεθεί επίσης
        for i in range(len(tokens)):
            if tokens[i] == "not":
                not_index.append(i)
                unprocessed.pop(i)

        # Βρίσκεται ο όρος μετά το "not" (s1) 
        for i in not_index:
            s1 = tokens[i+1]

            # Αφαιρούνται επεξεργασμένοι όροι από την λίστα των μη επεξεργασμένων
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)

            # Βρίσκεται ο όρος s1 στο ευρετήριο και τα άρθρα που του αντιστοιχούν ώστε να αφαιρεθούν από το τελικό αποτέλεσμα αργότερα
            not_res.append(inverted_index.get(s1))
            print(s1)
            print(inverted_index.get(s1, []))

        return not_res



def and_processing(tokens):
        and_index = []
        res1 = []
        res2 = []

        # Βρίσκεται ο δείκτης του "and" ώστε οι όροι που βρίσκονται πριν και μετά να βρεθούν επίσης
        for i in range(len(tokens)):
            if tokens[i] == "and":
                and_index.append(i)
                unprocessed.pop(i)

        # Βρίσκεται ο όρος πριν το "and" (s1) και ο όρος μετά (s2)
        for i in and_index:
            s1 = tokens[i-1]
            s2 = tokens[i+1]

            # Αφαιρούνται επεξεργασμένοι όροι από την λίστα των μη επεξεργασμένων
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)
            index2 = unprocessed.index(s2)
            unprocessed.pop(index2)

            # Βρίσκονται οι όροι s1, s2 στο ευρετήριο και τα άρθρα που τους αντιστοιχούν μπαίνουν σε δύο λίστες (μία για κάθε όρο)
            res1.append(inverted_index.get(s1, []))
            print(s1)
            print(inverted_index.get(s1, []))
            res2.append(inverted_index.get(s2, []))
            print(s2)
            print(inverted_index.get(s2, []))

            # Ταξινομούνται οι δύο λίστες και γίνεται τομή σε αυτές (μπαίνουν μόνο τα άρθρα που ταιριάζουν, δηλαδή έχουν και τους δύο όρους
            res1.sort()
            res2.sort()

            and_res = [i for i in res1 if i in res2]   
    
        return and_res 



def or_processing(tokens):
        or_index = []
        res1 = []
        res2 = []
        or_res = []

        # Βρίσκεται ο δείκτης του "or" ώστε οι όροι που βρίσκονται πριν και μετά να βρεθούν επίσης
        for i in range(len(tokens)):
            if tokens[i] == "or":
                or_index.append(i)
                unprocessed.pop(i)

        # Βρίσκεται ο όρος πριν το "or" (s1) και ο όρος μετά (s2)
        for i in or_index:
            s1 = tokens[i-1]
            s2 = tokens[i+1]

            # Αφαιρούνται επεξεργασμένοι όροι από την λίστα των μη επεξεργασμένων
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)
            index2 = unprocessed.index(s2)
            unprocessed.pop(index2)

            # Βρίσκονται οι όροι s1, s2 στο ευρετήριο και τα άρθρα που τους αντιστοιχούν μπαίνουν στην λίστα αποτελεσμάτων
            or_res.append(inverted_index.get(s1))
            print(s1)
            print(inverted_index.get(s1, []))
            or_res.append(inverted_index.get(s2))
            print(s2)
            print(inverted_index.get(s2, []))

        return or_res



def processing(tokens):
    doc_ids = []

    for i in tokens:
        unprocessed.append(i)

    if "and" in tokens:
        doc_ids.append(and_processing(tokens))

     
    if "or" in tokens:
        doc_ids.append(or_processing(tokens))


    # if "not" in tokens:
        # How to handle not? 
        # doc_ids.pop(not_processing(tokens))

    # Αν η λίστα δεν είναι άδεια υπάρχουν ακόμη όροι που πρέπει να επεξεργαστούν
    if unprocessed:
        for i in range(len(unprocessed)):
            doc_ids.append(inverted_index.get(unprocessed[i], []))


    return doc_ids

result = processing(tokens)

print(result)
