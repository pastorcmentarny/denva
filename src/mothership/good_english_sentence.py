#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import random

# list of sentence that are cool to use or it is example of good english sentence pattern.
sentences = [
    "I am extremely sorry for the disruption that Metropolitan line customers are experiencing this morning."
    "This has been caused by an issue with the signalling system at Baker Street.",
    "Michael Jackson was taking propofol to sleep, which is like doing chemotherapy because you're tired of shaving "
    "your head. (by Robbie Williams)",
    "Brent Cross Shopping Centre is hell on the earth on saturday.",
    "Jeremy Clarkson - '(...) to create a vision of pure ... what's the word? May and Hammond: RUBBISH!",
    "(4B) I shaved off my beard and I went to 'bear & bird' pub to drink a few pints of beer.",
    "I do not have knowledge on that matter.",
    "There've been a few developments.",
    "I am not a teacher, nor do I wish to become one.",  # from ST TNG
    "It was destined to fail. (by Tim Dillon in PowerfulJRE)",
    "The medicine is imperfect science. (by Dr. Mikhail 'Dr. Mike' Varshavski)",
    "Commander William T. Riker: A blind man teaching an android how to paint? ",
    "I am not very fashion conscious. (by James May in Vietnam Special)",
    "Compromise is a mutual dissatisfaction.",
    "I can't talk with you right now as somebody is wrong in the comment on the internet.",
    "Sons like put shit on fire. (by Jon Rogan)",
    "Firstly, if you end up reading this book and not liking it, I'm sorry. It is impossible to produce something that will be liked by everyone. ('The Idiot brain' by Dean Burnett).",
    "Science is the work of humans. (...) Humans are messy, chaotic and illogical creatures (...) and much of science reflects this.('The Idiot brain' by Dean Burnett).",
    "The mechanics that allow us to think and reason and contemplate didn't exist millions of years ago. The first fish to crawl onto land aeons ago wasn't racked with self-doubt, thinking, 'Why am I doing this? I can't breathe up here, and I don't even have any legs, whatever they are.  ('The Idiot brain' by Dean Burnett).",
    "Sleep involves doing nothing literally, lying down and not being conscious. How complicated could it possibly be?   ('The Idiot brain' by Dean Burnett).",
    "If you can't retrieve a memory, it's as good as not being there at all. It's like when you can't find your gloves; you've still got gloves, they still exist, but you've got cold hands anyway. ('The Idiot brain' by Dean Burnett).",
    "Brain never shuts down completely, partly because it has several ... the sleep state, but mostly because if it did shut down completely we'd be dead. ('The Idiot brain' by Dean Burnett)",
    "It's bit like using bathroom scales to weigh elephants; they can be useful for a standard range of weights, but at this level they'll give no useful data, just a load of broken plastic and springs ('The Idiot brain' by Dean Burnett)",
    "Modern politicians are media-trained so they can speak confidently and smoothly on any subject for prolonged periods without saying anything of value ('The Idiot brain' by Dean Burnett)",
    "You know for as long I can remember I had memories. (by Colin Mochrie)",
    "This is how I know that JP is a streamer on the another level. I got the email from the Microsoft with 'would you like a code'. I am like OMG 'Thank you me for blessing me with this influencer status' and then I found out that actually, I am getting lowest level of shit, because JP getting boxes of stuff' - Garry Whitta",
    "If you can't retrieve a memory, it's as good as not being there at all. It's like when you can't find your gloves; you've still got gloves, they still exist, but you've got cold hands anyway.",
    "Thank you. You definitely change the way I think about this. I appreciate that you take time and effort for this well-articulated thoughts. (Andy Stumpf)"
]


def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences) - 1)]
