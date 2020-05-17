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
    "Firstly, if you end up reading this book and not liking it, I'm sorry. It is impossible to produce something that will be liked by everyone. (From the book  'The Idiot brain' by Dean Burnett).",
    "Science is the work of humans. (...) Humans are messy, chaotic and illogical creatures (...) and much of science reflects this.(From the book  'The Idiot brain' by Dean Burnett)."
]


def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences) - 1)]
