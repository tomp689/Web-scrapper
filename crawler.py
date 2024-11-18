import requests
from bs4 import BeautifulSoup
import json



def fetch_wikipedia_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}") # σε περιπτωση που δεν υπαρχει το url ή δεν βρισκεται
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    paragraphs = soup.find_all('p')
    content = " ".join([para.text for para in paragraphs])
    return {"title": title, "content": content}

def collect_articles(urls):
    articles = []
    for url in urls:
        article = fetch_wikipedia_article(url) #κληση συναρτησης για την ευρηση δεδομενων
        if article:
            articles.append(article)
    return articles #επιστοφη πινακα με τα δεδομενα 

urls = ["https://en.wikipedia.org/wiki/Computer_programming"] # θα το τροποποιησουμε για manual search στα επομενα βηματα



articles = collect_articles(urls)


#αποθηκευεονται στο  json αρχειο τα αποτελεσματα απο την κληση της συναρητσης colect_articles


with open("data.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

#ο λογος που κανουμε with open αντι για open ειναι διοτι μας κλεινει αυτοματα το αρχειο οταν τελειωσει.

