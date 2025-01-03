import requests
from bs4 import BeautifulSoup
import json



def fetch_wikipedia_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        # Σε περίπτωση που δεν υπάρχει το url ή δεν βρίσκεται
        print(f"Failed to fetch {url}") 
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    paragraphs = soup.find_all('p')
    content = " ".join([para.text for para in paragraphs])
    return {"title": title, "content": content}

def collect_articles(urls):
    articles = []
    for url in urls:
        # Κλήση συνάρτησης για την εύρεση δεδομένων
        article = fetch_wikipedia_article(url) 
        if article:
            articles.append(article)
    # Επιστροφή πίνακα με τα δεδομένα
    return articles 

urls = ["https://en.wikipedia.org/wiki/Computer_programming"] # θα το τροποποιησουμε για manual search στα επομενα βηματα



articles = collect_articles(urls)


# Τα αρχεία που συλλέχθηκαν αποθηκεύονται σε json αρχείο
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

# Ο λόγος που κάνουμε with open αντί για open είναι διότι μας κλείνει αυτόματα το αρχείο όταν τελειώσει
