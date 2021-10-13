import os
from trie import Trie


class StoreData:
    __instance = None
    words_dict = {}
    words_trie = Trie()

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __str__(self):
        return "words_dict={}".format(self.words_dict)


def get_list_of_files(dirName):
    list_of_file = os.listdir(dirName)
    allFiles = list()
    for entry in list_of_file:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def add_words_to_dictionary(line, num_line, file):
    dict = StoreData()
    words_array = line.replace('\n', '').split()
    for index in range(len(words_array)):
        if index == len(words_array) - 1:
            new_word = ''
        else:
            new_word = words_array[index + 1]
        if not dict.words_dict.get(words_array[index]):
            dict.words_dict[words_array[index]] = Trie()
        dict.words_trie.insert(words_array[index], (num_line, file))
        dict.words_dict[words_array[index]].insert(new_word, (num_line, file))


def open_file(dirName):
    files_list = get_list_of_files(dirName)
    try:
        for file in files_list:
            print(file)
            line_index = 0
            with open(str(file), 'r', encoding='utf8') as f:
                for line in f:
                    line_index += 1
                    add_words_to_dictionary(line, line_index, file)
    except OSError:
        print("Oops! That was no valid file. Try again...")
        return
