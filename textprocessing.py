import nltk
import string
import nltk.tokenize
import nltk.corpus
import json

with open("data.json") as data:
	articles = data.read()



# Turning letters to lower case
def lowercase(articles):

	lowered = " ".join([i.lower() for i in articles])

	# print(lowered)

	return lowered

lowered = lowercase(articles)


# Stemming 
"""
def stemming(lowered):

	lowered = lowercase(articles)

	print("BEGIN STEMMING")

	porter = nltk.PorterStemmer()
	stemmed = [porter.stem(t) for t in articles]

	print(stemmed)

	print("STEMMING COMPLETE")

	return stemmed
"""



# Lemmatization

"""
Κατέβασε το wordnet: nltk.download('wordnet')

def lemmatization(lowered):

	lemmatizer = nltk.WordNetLemmatizer()
	lemmantized = [lemmatizer.lemmatize(t) for t in articles]

	print(lemmatized)

	return lemmatized



lemmatization(articles)
"""

# stemmed = stemming(articles)
# OR lemmatized = lemmatization(articles)



# Tokenization
def tokenization(lowered):

	tokenized = str.split(lowered)
	# tokenized = stemmed.split() 
	# OR tokenized = nltk.word_tokenize(lowered) 

	# print(tokenized)

	return tokenized


tokenized = tokenization(lowered)


# Stop words removal
def remove_stopwords(tokenized):

	# print(string.punctuation)

	# Για τα προθήματα, κατέβασε nltk.download('stopwords')
	stopwords = nltk.corpus.stopwords.words('english')

	cleaned_tokens = []
	for i in tokenized:
		if i not in string.punctuation and i not in stopwords:
			cleaned_tokens.append(i)

	# print(cleaned_tokens)

	return cleaned_tokens


cleaned_tokens = remove_stopwords(tokenized)

with open("processed_data.json", "w", encoding = "utf-8") as processed:
	json.dump(cleaned_tokens, processed, ensure_ascii = False, indent = 4)