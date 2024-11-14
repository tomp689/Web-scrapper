from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/Main_Page"

def get_contents(url):
		result = requests.get(url)

		if result.status_code != 200:
			print("Unable to retrieve page.")
			return None

		soup = BeautifulSoup(result.text, "html.parser")

		# Get the article's title
		title = soup.find('h1', class_='firstHeading').text.strip()


		# Get all content from the div class, then extract the paragraphs from it
		div = soup.find('div', class_='mw-parser-output')
		paragraphs = div.find_all('p').text.strip()

		# Join all the paragrpahs into one piece of text / string
		text = "\n".join(paragraphs)

		return title, text




def crawler(url, i=0):
	articles = []
	links = []

	while i <= 99:
		i++

		title, text = get_contents(url)

		# Add the article to the list of articles

		if title and text:
			articles.append(
				{
				'URL': url,
				'Title': title,
				'Text': text
				})


		# Get links that are featured in the page and add them to the link list
		links = get_links(url)

	return articles




def get_links(url):
	links = []
	basic_wiki = 'https://en.wikipedia.org'

	result = requests.get(url)

	if result.status_code != 200:
		print("Unable to retrieve URL.")
		return None

	soup = BeautifulSoup(result.text, "html.parser")

	# Find the links that are featured (inside <a> tags, href starts with /wiki/)
	for a in soup.find_all('a', href=True):
		href = a['href']

		# Combine Wiki's link with the href of the specific link you got
		new_link = basic_wiki + href
		links.append(new_link)


	return links


# Start the crawler
articles = crawler(url, i=0)


# Save articles to a JSON file
with open('articles.json', 'w') as file:
	json.dump(articles, file)
		