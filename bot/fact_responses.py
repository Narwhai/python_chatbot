import facts_dict
import random

facts = facts_dict.create_facts_dict()

# If one of the topic words was in the question posed by the user, 
# it pulls facts about that topic and creates a dictionary
def specific_facts(topic, sentence, noun, adjective, verb):
    topic = topic.lower()
    # Weird case where I have to add a space after 'blonde'. Without it, my fact picker would include
    # facts about blonded radio, which is not the same topic
    if topic == "blonde":
        topic = "blonde "
    
    topic_facts = facts[topic]
    
    # Essentially goes through the whole dictionary of facts to find a potential match using 
    # the POS found within the sentence given by the user 
    for x in range(len(topic_facts)):
        #It tries to match all three if it can, if not then it tries matching two before going to just one
        if noun is not None and verb is not None and adjective is not None:
            if (noun in topic_facts[x]) and (verb in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None and verb is not None:
            if (noun in topic_facts[x]) and (verb in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None and adjective is not None:
            if (noun in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif verb is not None and adjective is not None:
            if (verb in topic_facts[x]) and (adjective in topic_facts[x]):
                resp = topic_facts[x]
                return resp
        elif noun is not None:
            if noun in topic_facts[x]:
                resp = topic_facts[x]
                return resp
        elif verb is not None:
            if verb in topic_facts[x]:
                resp = topic_facts[x]
                return resp
        elif adjective is not None:
            if adjective in topic_facts[x]:
                resp = topic_facts[x]
                return resp

    #If the user just wants a random fact, it is selected here
    if "random" in sentence.lower():
        num_facts = len(topic_facts)
        resp = "Here's a random fact about " + topic + ": " + topic_facts[random.randrange(num_facts-1)] 
    else:
        resp = "I couldn't find that, sorry"

    return resp