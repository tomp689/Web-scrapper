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
    # Turn the query into lowercase    
    lowered_query = query.lower()

    # Split lowered query into tokens and remove all punctuation with NTLK's tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    query_tokens = tokenizer.tokenize(lowered_query)

    return query_tokens
    
tokens = tokenization(query)


def not_processing(tokens):
        not_index = []
        not_res = []

        # Find the index of the word "not" so the word after that can be found
        for i in range(len(tokens)):
            if tokens[i] == "not":
                not_index.append(i)
                unprocessed.pop(i)

        # Get the word after "not" (s1)
        for i in not_index:
            s1 = tokens[i+1]

            # Remove processed words from the list of unprocessed words
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)

            # Find the id of the word and store it to be used later and remove references to it from the total result
            not_res.append(inverted_index.get(s1))
            print(s1)
            print(inverted_index.get(s1, []))

        return not_res



def and_processing(tokens):
        and_index = []
        res1 = []
        res2 = []

        # Find the index of the word "and" so the word before and after that can be found
        for i in range(len(tokens)):
            if tokens[i] == "and":
                and_index.append(i)
                unprocessed.pop(i)

        # Get the word before "and" (s1) and the word after "and" (s2)
        for i in and_index:
            s1 = tokens[i-1]
            s2 = tokens[i+1]

            # Remove processed words from the list of unprocessed words
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)
            index2 = unprocessed.index(s2)
            unprocessed.pop(index2)

            # Find the ids of those words in the inverted index, split them into two lists
            res1.append(inverted_index.get(s1, []))
            print(s1)
            print(inverted_index.get(s1, []))
            res2.append(inverted_index.get(s2, []))
            print(s2)
            print(inverted_index.get(s2, []))

            # Sort the two lists and then do AND on them (τομή), append to doc_ids only values that match
            res1.sort()
            res2.sort()

            and_res = [i for i in res1 if i in res2]   
    
        return and_res 



def or_processing(tokens):
        or_index = []
        res1 = []
        res2 = []
        or_res = []

        # Find the index of the word "or" so the word before and after that can be found
        for i in range(len(tokens)):
            if tokens[i] == "or":
                or_index.append(i)
                unprocessed.pop(i)

        # Get the word before "or" (s1) and the word after "or" (s2)
        for i in or_index:
            s1 = tokens[i-1]
            s2 = tokens[i+1]

            # Remove processed words from the list of unprocessed words
            index1 = unprocessed.index(s1)
            unprocessed.pop(index1)
            index2 = unprocessed.index(s2)
            unprocessed.pop(index2)

            # Find the ids of those words in the inverted index and add them to the list of doc_ids
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
        # doc_ids.append(not_processing(tokens))

    # If the unprocessed list is not empty -- there are still some words to be processed
    if unprocessed:
        for i in range(len(unprocessed)):
            doc_ids.append(inverted_index.get(unprocessed[i], []))


    return doc_ids

result = processing(tokens)

print(result)
