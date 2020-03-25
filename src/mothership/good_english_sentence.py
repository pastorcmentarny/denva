import random

sentences = [
    'I am extremely sorry for the disruption that Metropolitan line customers are experiencing this morning.'
    'This has been caused by an issue with the signalling system at Baker Street.',
    "Michael Jackson was taking propofol to sleep, which is like doing chemotherapy because you're tired of shaving your head. (Robbie Williams)",
    "Brent Cross Shopping Centre is hell on the earth on saturday.",
    "Jeremy Clarskon - '(...) to create a vision of pure, what's the word? May and Hammond 'RUBBISH!",
    "(4B) I shaved off my beard and I went to 'bear & bird' pub to drink a few pints of beer.",
    "I do not have knowledge on that matter.",
    "There've been a few developments.",
    "I am not a teacher, nor do I wish to become one." #from ST TNG
]


def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences)-1)]

