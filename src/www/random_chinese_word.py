import random

words = []

def load_dictionary_file() -> list:
    file_path = 'D:/Projects/denva/src/data/dictionary.txt'
    file = open(file_path, 'r',encoding="UTF-8",  newline='')
    content = file.readlines()
    for line in content:
        definition = line.split(";;")
        definition = definition[2:len(definition)-2]
        word = {'character': definition[0],
                'pinyin' : definition[1],
                'english' : definition[3],
                'polish' : definition[4]
                }
        words.append(word)
    return words


def get_random_chinese_word() -> dict:
    load_dictionary_file()
    return words[random.randint(0, len(words) - 1)]


if __name__ == '__main__':
    load_dictionary_file()
    random_chinese_word = get_random_chinese_word()
    print(random_chinese_word.get('character'))
    print(random_chinese_word.get('pinyin'))
    print(random_chinese_word.get('english'))
    print(random_chinese_word.get('polish'))