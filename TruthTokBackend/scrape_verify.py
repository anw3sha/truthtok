import requests
from bs4 import BeautifulSoup
from newspaper import Article
import urllib.parse
from transformers import pipeline

# initialize the classifier pipeline
classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news", tokenizer="mrm8488/bert-tiny-finetuned-fake-news")

def construct_search_url(keywords, start):
    query = urllib.parse.quote_plus(keywords)
    return f"https://www.google.com/search?q={query}&start={start}"

def scrape(keyword):
    all_articles = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    start = 0
    max_articles = 10

    while len(all_articles) < max_articles:
        URL = construct_search_url(keyword, start)

        try:
            response = requests.get(URL, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL for keywords '{keyword}': {e}")
            break

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error parsing the HTML for keywords '{keyword}': {e}")
            break

        links = soup.find_all('a', href=True)

        # filter and clean up the article links
        article_links = [link['href'].split('url?q=')[1].split('&sa=U')[0] for link in links if 'url?q=' in link['href']]

        for article_url in article_links:
            try:
                article = Article(article_url)
                article.download()
                article.parse()
                print(f"Processing article from {article_url}")
                all_articles.append({
                    'keyword': keyword,
                    'title': article.title,
                    'text': article.text.lower(),
                    'date': article.publish_date  # optional
                })

                # break if we reached the max articles
                if len(all_articles) >= max_articles:
                    break
            except Exception as e:
                print(f"Error processing article {article_url} for keywords '{keyword}': {e}")
                continue

        start += 10

    return all_articles

def classify(all_articles):
    real = 0
    fake = 0

    for article in all_articles:
        result = classifier(article['text'])[0]['label']  # classifier returns a list of dictionaries
        if result == 'REAL': 
            real += 1
        else:
            fake += 1

    if real > fake:
        return 'CHECK'
    elif real == fake:
        return 'QUESTION'
    else:
        return 'CROSS'