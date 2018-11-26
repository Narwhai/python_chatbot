from __future__ import print_function, unicode_literals

import os
import re
import sys
import random
import get_song_lyrics
import fact_responses
import create_response
from textblob import TextBlob

"""Logging is useful for debugging but not necessary for functionality"""
#importing logging 
#logging.basicConfig()
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

# GLOBAL VARIABLES 
running = True
known_user = False 
memory = {}

FACT_WORDS = ["frank ocean", "channel orange", "blonde", "nostalgia ultra", "endless", "blonded radio"]

GREETINGS = ("hello", "hi", "salutations", "hey", "what's up", "whats up", "sup")

GREETING_RESPONSES = ["Hello!", "Greetings!", "How's it going"]

GOODBYE_STATEMENTS = ["goodbye", "farewell", "bye", "exit"]

GOODBYE_RESPONSES = ["Goodbye!", "Farewell!", "Buh-bye!"]

COMMENTS_ABOUT_SELF = ["I know more about Frank Ocean than you.",
                        "I'm doing my best"]

NONE_RESPONSES = [ "What can I help you with?",
                    "Ask me about Frank Ocean!",
                    "What do you want to know about Frank Ocean?"]

# List of songs by Frank Ocean. Got this idea super last minute so it's very small.
# Might be able to create an extensive list using the Genius API
SONGS = ["thinking bout you", "biking", "chanel", "start", "fertilizer", "provider", "moon river", "lens", "slide"]


# Checks if the user is sending a greeting, if so then it responds with a greeting of its own
def check_greeting(sentence):
    for word in sentence.words:
        if word.lower() in GREETINGS:
            return random.choice(GREETING_RESPONSES)


# Checks if user is saying goodbye/terminating. If so, then global variable 'running' is set to False,
# it returns a closing response, and then stops execution
def check_ending(sentence):
    global running
    for word in sentence.words:
        if word.lower() in GOODBYE_STATEMENTS:
            running = False
            return random.choice(GOODBYE_RESPONSES)


#check for pronoun compability -- 'a' vs 'an'
def starts_with_vowel(word):
    return True if word[0] in 'aeiou' else False

#Construct a response if no special case was matched using as much of the user input as it can
def construct_response(pronoun, noun, verb):
    resp = []

    if pronoun:
        resp.append(pronoun)

    if verb:
        verb_word = verb[0]
        if pronoun.lower() == 'you':
            resp.append("aren't really")
        else:
            resp.append(verb_word)
    
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append("smh")
    return ' '.join(resp)


#Find best candidate verb
def find_verb(sent):
    verb = None
    #pos = None
    for w, p in sent.pos_tags:
        if p.startswith('VB'):
            verb = w
            #pos = p
            break
    return verb #, pos


#Find best candidate adjective
def find_adjective(sent):
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':
            adj = w
            break
    return adj


#Find best candidate noun
def find_noun(sent):
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':
                noun = w
                break
    #if noun:
        #logger.info("Found noun: %s", noun)
    return noun


#Given a sentence finds a pronoun to respond with 
def find_pronoun(sent):
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        #disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            #If user mentions themselves, they are the pronoun
            pronoun = 'You'
        return pronoun


#Determines the parts of speech of each word in user input sentence
def parts_of_speech(parsed):
    #Different parts of speech that will be found 
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    #logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb


#Preprocesses user input. Capitalizes singular 'i's' so they can be identified as pronouns
def preprocess_text(sentence):
   
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)
    return ' '.join(cleaned)


#Parses user input to see what is being asked and select best response
def respond(sentence):
    
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    #This will pick the parts of speech of user input 
    pronoun, noun, adjective, verb = parts_of_speech(parsed)

    #Checks if user is trying to end termination
    resp = check_ending(parsed)

    # Checks if user simply greeted bot
    if not resp:
        resp = check_greeting(parsed)

    # If the user is asking for lyrics, the function to pull them is called here
    if "lyrics" in sentence.lower():
        # If there are no quotation marks found in sentence, then it asks user to 
        # include them around the song title
        if ("\'" not in sentence) and ('\"' not in sentence):
            resp = "Please include the song title inside quotation marks"
        else:
            song_name = re.findall('''(?<='|")\s*[^']+?\s*(?='|")''', sentence) # finds text inside of double and single quotations
            resp = get_song_lyrics.get_lyrics(song_name[0], "Frank Ocean") # gets song lyrics and sets them as the response

    # Checks to see if one of the topic words is in the question being asked by the user
    # if so, then it searches for a response in the 'facts' file
    if not resp:
        for x in range(len(FACT_WORDS)):
            if FACT_WORDS[x] in sentence.lower():
                resp = fact_responses.specific_facts(FACT_WORDS[x], sentence, noun, adjective, verb)

    # If the topic words are not used in the question asked by the user, 
    # searches the larger knowledge base for adjective or noun given, verb 
    # tends to be too broad of a word 
    if not resp:
        for x in range(len(SONGS)):
            if SONGS[x] in sentence.lower():
                resp = create_response.search_kb_song(SONGS[x], sentence)
    
    # Tries picking a response using noun and adjective found in sentence,
    # by searching through the knowledge base 
    if not resp:
        resp = create_response.search_kb(sentence, noun, adjective)

    # If all of those fail, essentially picks a random response
    if not resp:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb)
        
    if not resp:
        resp = random.choice(NONE_RESPONSES)
    
    #logger.info("Returning phrase '%s'", resp)
    return resp


# Main function that takes user input and returns a response 
def main():

    global known_user # Used to get users name 
    global running # Used to continously ask for user input 

    while running:
        if not known_user:
            user_name = input("> Hello I'm a Frank Ocean expert. Whats your name? ")
            memory["user_name"] = user_name
            user_response = user_name
            known_user = True
            intro_response = "> Hello " + memory["user_name"] + ", how can I help you? "
            user_response = input(intro_response)
            response = respond(user_response)
            print(response)          
        else:
            #bot_response = "Hello " + memory["user_name"] + ", how can I help you?"
            #user_response = input(bot_response + '\n')
            user_response = input('> ')
            response = respond(user_response)
            print(response)


if __name__ == "__main__":
    main()

