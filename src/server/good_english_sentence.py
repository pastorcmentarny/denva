#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import random

# List of sentences that are cool to use or it is an examples of good English sentence patterns.
sentences = [
    "I am extremely sorry for the disruption that Metropolitan line customers are experiencing this morning."
    "This has been caused by an issue with the signalling system at Baker Street.",
    "Michael Jackson was taking propofol to sleep, which is like doing chemotherapy because you're tired of shaving "
    "your head. (by Robbie Williams)",
    "Brent Cross Shopping Centre is hell on the earth on saturday.",
    "Jeremy Clarkson - '(...) to create a vision of pure ... what's the word? May and Hammond: RUBBISH!",
    "(4B) I shaved off my beard and I went to 'bear & bird' pub to drink a few pints of beer.",
    "I do not have knowledge on that matter.",
    "They've been a few developments.",
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
    "Thank you. You definitely change the way I think about this. I appreciate that you take time and effort for this well-articulated thoughts. (Andy Stumpf)",
    "CAPS LOCK – Preventing Login Since 1980.",
    "It is a testimony to the power of taking intelligent risks, even when they don't quite work as intended.",
    "How to deal with the never-ending shit barrage of the human experience?",
    "The company admitted it would 'continue to improve the overall experience' via those never-ending patches we've all come to know and love over the years.",
    "I am not sure if this knowledge will enrich me in any meaningful way.",
    "The parents and grandparents are the heroes of our society.",
    "Do you know what time it is? It's tomorrow!",
    "The art of not giving a shit.",
    "How bad 'bad' gets.",
    "Developers are often  worse than networking people. Show me a developer who isn’t crashing production systems, and I’ll show you one who can’t fog a mirror. Or more likely, is on vacation.",
    "It is just one person who knows threading in java and that's is NOT YOU! - John R",
    "Arguing that you don’t care about the right to privacy because you have nothing to hide is no different from saying you don’t care about free speech because you have nothing to say. — EDWARD SNOWDEN",
    "Burnout is the car crash you don’t see coming. – Stacey King Gordon",
    "Seeing an opportunity, some pioneer plants got together and said, “Let’s go!” and migrated up onto land. But once the plants got out of the water, they discovered something they never had to deal with in the ocean: gravity",
    "That's incredibly gone. Is it?",
    "I don’t know the future better than anyone else.",
    "Ms Nowell, 19, from Winchester, Hampshire, told the BBC the interview left her feeling like 'the only atheist in a gigantic monastery'.",
    "Sleep involves doing literally nothing, lying down and not being conscious. How complicated could it possibly be?",
    "Brain never shuts down completely, partly because it has several roles in maintaining the sleep state, but mostly because if it did shutdown completely, we'd be dead.",
    "My final apology is based on the fact that a former colleague of mine once told me that i'd get a book published ' when hell freezes over'. Sorry to Satan. It must be very inconvenient for you.",
    "Some animals, such as jellyfish and sponges, don't show any sign of sleeping, but they don't even have brains so you can't trust them to do much of anything.",
    "What's the ROI* on hugging your mom? {*ROI - Return of Investment}",
    "I appreciate your thorough attentiveness to my deliverables. To ensure we are not duplicating work, please let me know in the future if you'd like to take this n yourself.",
    "This is a reason why god invited 'copy and paste'.",
    "The service is suspended between Harrow-on-the-Hill and Watford while we remove a gazebo from the track. (TfL)"
    "For every claim or statement made in this book, you'd probably be able to find some new study or investigation that argues against it.",
    "Thank you for sharing this timeline with me. Can you help me understand how this amount of work is achievable in such a short period of time? (LoeWhaley)",
    "Please help me understand why I am required to be in the office when I can effectively execute my job responsibilities remotely. (LoeWhaley)",
    "Germans are usually quiet, impeccably polite and keen to remind us that their mid-20th Century reputation for arriving everywhere in a tank is a thing of the past. (Jeremy Clarkson)",
    "That looks like next week problem for me (LoeWhaley)",
    "They have to be given a nice cup of fair trade, nuclear-free, peace coffee made with milk from a nut and told that their ridiculous demands will be met.(Jeremy Clarkson)",
    "Decommissioning activity has now been actioned."
]

def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences) - 1)]
