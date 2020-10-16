from usp.tree import sitemap_tree_for_homepage
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import nltk
import re
import string

def main():
    urls = ask_for_url()
    print(urls)
    texts = scrape(urls)
    print(texts)
    word_list = create_wordlist(texts)
    print(word_list)
    save(word_list)



def ask_for_url():
    print("What URL do you want to search?")
    url = input('>')
    print("Do you want to search more than one URL?")
    answer = input('>').lower()
    if answer.startswith('y'):
        # Check sitemap of URL
        tree = sitemap_tree_for_homepage(url)
        #for page in tree.all_pages():
        #   print(page)
        # Tell user how many pages are found
        number_of_pages_found = len(list(tree.all_pages()))
        print(f'A total of  {number_of_pages_found} pages were found.')

        # Allow user to specify how many pages to scrape
        print("How many pages do you want to scrape?")
        pages_to_scrape = int(input('>'))
        pages_scraped = []
        for page in tree.all_pages():
            pages_scraped.append(page.url)
            if len(pages_scraped) == pages_to_scrape:
                break

        return pages_scraped
    else:
        return [url]

def scrape(urls):
    results = []
    for url in urls:
        html = urllib.request.urlopen(url).read()
        text = text_from_html(html)
        results.append(text)
    return results

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)

def create_wordlist(texts):
    word_set = set()
    for text in texts:
        words = text.split(" ")
        words = clean_words(words)
        word_set.update(words)

    return list(word_set)

def clean_words(words):
    result = []
    for word in words:
        table = str.maketrans(dict.fromkeys(string.punctuation))
        clean_word = word.translate(table)
        result.append(clean_word)
    return result

#def create_phraselist(texts):


def save(word_list):
    print('Name the file')
    name = input('>')
    with open(name + '.txt', 'w') as outfile:
        outfile.write( "\n".join(word_list))







if __name__ == '__main__':
   main()


