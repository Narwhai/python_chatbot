import sys
import os
import re
import string
import requests
import nltk
import data_extraction
from nltk import tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

# Name: Roman Soriano
# Web scraper that finds URL's related to artist Frank Ocean starting from his wikipedia page. 
# Every relevant URL found on the page is then scraped and saved to a text file. These files are
# later cleaned up to find the top 40 most frequent terms found accross all pages scraped. 
# 
# The initial scrape takes a little bit as some of the pages take a little while to be loaded
#
# Needs to be optimized. Each function was created as a separate file during 
# development so I wouldn't have to run the entire program each time I was testing.
# 


# GLOBALS
current_working_dir: str = os.getcwd()

# Creates a dictionary of the most frequently used terms in the clean files
# accross all of the files
def term_extraction():

    #current_working_dir: str = os.getcwd()
    path = os.path.join(current_working_dir, "clean_files\\")
    stop = set(stopwords.words("english"))
    term_dict = {}

    # Iterates through each file and processes them further before
    # creating a dictionary with all of the terms and their frequency

    for file in os.listdir(path):
        file_read = path + "\\" + os.fsdecode(file)
        with open(file_read, "r", encoding='utf-8') as f_in:
            text = f_in.read()
            # I noticed an issue with some of the punctuation not having a space after it,
            # leading to two words getting combined. This line fixes most of those issues
            #text = text.replace(".", ". ")
            text = text.replace("’", "")
            text = text.replace('“', " ")
            text = text.replace('”', "")
            text = text.translate(str.maketrans('','',string.punctuation))
            tokens = nltk.word_tokenize(text)
            tokens = [w for w in tokens if not w in stop]
            # Creates a dictionary of the terms found in the text
            for word in tokens:
                if word in term_dict:
                    term_dict[word] += 1
                else:
                    term_dict[word] = 1

    # Sorts the dictionary and outputs the top 40 most frequent words
    sorted_dict = sorted(term_dict.items(), key=lambda kv: kv[1], reverse=True)
    for x in range(40):
        print(str(x+1) + ": " + str(sorted_dict[x]))

# Takes the files from the web scraping and cleans them up and splits them into sentences.
# The sentences from each file are output to a new file
def file_cleanup():

    path = os.path.join(current_working_dir, "raw_files\\")

    # Iterates through each file and cleans them up, saving the sentences
    # in the text to new files in a new directory.
    for file in os.listdir(path):
        file_read = path + "\\" + os.fsdecode(file)
        file_write = os.path.join(current_working_dir, "clean_files")
        filename = file[:-4] + "_clean.txt"
        file_write = os.path.join(file_write, filename)
        os.makedirs(os.path.dirname(file_write), exist_ok=True)
        with open(file_read, 'r', encoding='utf-8') as f_in:
            text = f_in.read()
            text = text.lower()
            text = text.replace('"', '')
            text = text.replace("’", "")
            text = text.replace('“', "")
            text = text.replace('”', "")
            text =  re.sub(r'\[.*\]', '', text)
            text = ' '.join(text.split())
            tokens = nltk.sent_tokenize(text)
            with open(file_write, 'w', encoding='utf-8') as f_out:
                 for token in tokens:
                    #token = token.translate(str.maketrans('','',string.punctuation))
                    f_out.write(token + '\n')

# Takes a starter URL, and finds more URLs related to the topic
# These URL's are stored in a list, and the first 15
# have the text from them scraped and output to files
def web(page,WebUrl):

    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        links = []
        links.append(WebUrl) #adds starter link to links

        # Words to search for in the URLs that relate to the topic
        topic_words = ["frank", "ocean", "orange", "blonde", "endless", "nostalgia", "ultra"]

        for link in s.findAll('a', attrs={'href': re.compile("^http://")}):
            link_url = link.get('href')
            if any(substring in link_url for substring in topic_words):
                if link_url not in links:
                    links.append(link_url)

        # The links that pointed to another wiki page were not a full URL,
        # so searching for "http://" didn't work to get them.
        for link in s.findAll('a', attrs={'href': re.compile("/wiki/")}):
            link_url = link.get('href')
            if any(substring in link_url.lower() for substring in topic_words):
                # It was pulling image URLs, this skips them
                if "File:" in link_url:
                    continue
                #  Makes each wiki link into a proper URL
                if link_url.startswith('/wiki/'):
                    link_url = "https://en.wikipedia.org" + link_url
                # Filters out non-english wikipedia pages
                if "wikipedia" in link_url and not link_url.startswith('https://en.'):
                    continue
                if link_url not in links:
                    links.append(link_url)

        # Outputs text from URL into a file 
        for x in range(len(links)):
            # Tries to get a response from url, if no response is received (dead link etc.)
            # then it is ignored and execution continues
            try:
                link_code = requests.get(links[x])
            except:
                continue
            soup2 = BeautifulSoup(link_code.content, 'html.parser')
            file_write = os.path.join(current_working_dir, "raw_files")
            filename = str(x) + ".txt"
            file_write = os.path.join(file_write, filename)
            os.makedirs(os.path.dirname(file_write), exist_ok=True)
            with open(file_write, 'w', encoding='utf-8') as f_out:
                for text in soup2.findAll('p'):
                    f_out.write(text.getText())


# Just calls all the other functions, I'm sure this can be improved
def main():

    web(1, 'https://en.wikipedia.org/wiki/Frank_Ocean')
    file_cleanup()
    term_extraction()
    data_extraction.knowledge_base_creator()
    data_extraction.fact_curator()


if __name__ == "__main__":
    main()
print("The program has executed fully.")