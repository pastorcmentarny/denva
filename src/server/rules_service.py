import random

rules = [
    "It is so easy to say 'You will do it tomorrow'. Re-program yourself to say: 'Tomorrow is not a viable option. I am doing it TODAY!",
    "Eliminate things and interactions that made u sad.  Remember, This world is heartless to everything.",
    "Visualize good things in the times of struggle.",
    "Approach everything you do from a place of self-compassion.",
    "Discipline allows you to get things done. Discipline equals freedom, it sounds counterproductive but you have freedom because of discipline. I have freedom because of the discipline to get things done."
]

#TODO REMOVE IT, It is part of Inkyframe now
def get_all_rules() -> list:
    return rules


def get_random_rule() -> str:
    return rules[random.randint(0, len(rules) - 1)]
