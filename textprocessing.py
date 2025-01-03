import nltk
import string
from nltk.tokenize import RegexpTokenizer
import nltk.corpus
import json

with open("data.json") as data:
	articles = data.read()


def lowercase(articles):

	# Μετατροπή των γραμμάτων σε μικρά
	lowered = articles.lower()
	
	return lowered

lowered = lowercase(articles)


# Tokenization
def tokenization(lowered):

	# Χωρίζουμε το κείμενο σε tokens και αφαιρούμε σημεία στίξης και ειδικούς χαρακτήρες με τον tokenizer της NLTK
	tokenizer = RegexpTokenizer(r'\w+')

	tokenized = tokenizer.tokenize(lowered)

	return tokenized


tokenized = tokenization(lowered)


# Αφαίρεση stop-words
def remove_stopwords(tokenized):

   	# Δημιουργία λίστας με όλες τις stop-words της NLTK
	stopwords = nltk.corpus.stopwords.words('english')

	cleaned_tokens = []

	# Αν το token δεν είναι stop-word, τότε θεωρείται "καθαρισμένο"
	for i in tokenized:
		if i not in stopwords:
			cleaned_tokens.append(i)

	return cleaned_tokens


cleaned_tokens = remove_stopwords(tokenized)

# Όλα τα tokens αποθηκεύονται σε ένα αρχείο
with open("processed_data.json", "w", encoding = "utf-8") as processed:
	json.dump(cleaned_tokens, processed, ensure_ascii = False, indent = 4)
