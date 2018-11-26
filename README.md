# python_chatbot
Python chatbot that builds a knowledge base about artist Frank Ocean by web scraping.

First run "web_scraper.py". This will start crawling at the starter url, in this case it's Frank Ocean's wikipedia page. Here it 
will look for more URLs, and scrape the text from them. It creates a new directory, called "raw_files" and saves the raw text to a 
file, one file per URL. 

Next, the text is cleaned up by removing stopwords and punctuation. These files are saved to a new directory titled "clean_files", 
and the file names are appended with "_clean". Using these files, a dictionary is created with each term that is found used as the 
key, and its value is how many times it appears throughout the files. The top 40 most frequent terms are output.

The functions from data_extraction.py are run next, first knowledge_base_creator and then fact_curator. The first one builds a 
knowledge base from the clean files, adding only lines that contain words from a list of words relating to the topic. The second 
then goes through the knowledge base, making a smaller one that contains only lines about a smaller set of topics, in this case 
Frank Ocean, his albums, and his radio show. 

Running the bot.py file begins execution on the chatbot. Asking it for lyrics to a song will return the lyrics using the Genius 
API. The word "lyrics" must be in the query, and the song title must be inside quotation marks, single or double. It can return a 
random fact about one of the main topics in the 'facts.txt' file, or it can try to pick one from that file based on the 
nouns/adjectives found in the users query. 

If the query contains one of the song titles in the SONGS list, it will search 'knowledge_base.txt' for a suitable response. I got 
this idea very last minute so there's very few songs in the list, but I think it might be possible to pull a list of songs using 
the Genius API. 

Failing all of that, the bot will attempt to find a response by searching through 'knowledge_base.txt' using the nouns/adjectives 
found in the users response. If that still does not yield a response, it will remove stopwords from the users response, and try to 
match one of the remaining tokens with a response from the knowledge base. 

If a response is still not found, it will either admit defeat, or attempt to create a response by using as much of the users input 
as possible. 

If the bot is sent a greeting, it will respond with a greeting of its own.

To end execution, send it a farewell message such as "goodbye" and the bot will respond with its own farewell message before 
terminating execution. 

