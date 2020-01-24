import random

sentences = [
    'I am extremely sorry for the disruption that Metropolitan line customers are experiencing this morning.'
    'This has been caused by an issue with the signalling system at Baker Street.'
]


def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences) - 1)]
