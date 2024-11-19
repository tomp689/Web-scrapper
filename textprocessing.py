import nltk
import string
import nltk.tokenize
import nltk.corpus
import json

with open("data.json") as data:
	articles = data.read()

normalization(articles)

stemming(normalized_data)

tokenization(stemmed)

remove_stopwords(tokenized)



# OR lemmatization(articles)

tokenization(articles)

# Normalization
def normalization(articles):

	normalized_data = [i.lower() for i in articles]

	print(normalized_data)



# Stemming 
def stemming(normalized_data):

	print("BEGIN STEMMING")

	porter = nltk.PorterStemmer()
	stemmed = [porter.stem(t) for t in normalized_data]

	print(stemmed)

	print("STEMMING COMPLETE")


# Lemmatization

"""
Κατέβασε το wordnet: nltk.download('wordnet')

def lemmatization(articles):

	lemmatizer = nltk.WordNetLemmatizer()
	lemmantized = [lemmatizer.lemmatize(t) for t in articles]

	print(lemmatized)
"""



# Tokenization
def tokenization(stemmed):

	print("BEGIN TOKENIZATION")

	tokenized = stemmed.split() 
	# OR tokenized = nltk.word_tokenize(articles) (με import nltk.tokenize)

	print(tokenized)

	print("TOKENIZATION COMPLETE")



# Stop words removal
def remove_stopwords(tokenized):

	print(string.punctuation)
	print("STARTING TO REMOVE")

	# Για τα προθήματα, κατέβασε nltk.download('stopwords')
	stopwords = nltk.corpus.stopwords.words('english')

	cleaned_tokens = []
		for i in tokens:
			if i not in string.punctuation & i not in stopwords:
				cleaned_tokens.append(i)

	print("STOP WORDS REMOVED")

	with open("processed_data.json", "w", encoding = "uth-8") as processed:
		json.dump(cleaned_tokens, processed, ensure_ascii = False, indent = 4)


