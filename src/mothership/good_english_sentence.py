import random

sentences = [
    'I am extremely sorry for the disruption that Metropolitan line customers are experiencing this morning.'
    'This has been caused by an issue with the signalling system at Baker Street.',
    "Michael Jackson was taking propofol to sleep, which is like doing chemotherapy because you're tired of shaving your head. (Robbie Williams)",
    "Brent Cross Shopping Centre is hell on the earth on saturday.",
    "Jeremy Clarskon - '(...) to create a vision of pure, what's the word? May and Hammond 'RUBBISH!"
]


def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences))]
