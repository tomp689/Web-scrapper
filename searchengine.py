import string
import json
import nltk
from nltk.tokenize import RegexpTokenizer
import nltk.corpus
from indexing import inverted_index

query = []

print("Give at least one word, press enter when you're done.\n")


query = input()

def tokenization(query):
    # Turn the query into lowercase    
    lowered_query = query.lower()

    # print(lowered_query)

    # Split lowered query into tokens and remove all punctuation with NTLK's tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    query_tokens = tokenizer.tokenize(lowered_query)

    # print(query_tokens)

    return query_tokens
    
tokens = tokenization(query)

# print(tokens)

with open("invertedindex.json") as file:
    documents = file.read()

def processing(tokens):
    doc_ids = []
    res1 = []
    res2 = []
    res = []

    if "and" in tokens:
        and_index = []

        # Find the index of the word "and" so the word before and after that can be found
        for i in range(len(tokens)):
            if tokens[i] == "and":
                and_index.append(i)

            # Get the word before "and" (s1) and the word after "and" (s2)
        for i in and_index:
            s1 = tokens[i-1]
            s2 = tokens[i+1]

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

            res = [i for i in res1 if i in res2]   
            doc_ids.append(res)         

    """   
    elif tokens[i] = "or":
        # TO BE DONE
    elif tokens[i] = "not":
        # TO BE DONE
    else
        # TO BE DONE 
    """

    return doc_ids

result = processing(tokens)

print(result)
