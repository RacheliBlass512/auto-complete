from autoCompleteData import AutoCompleteData
import string

word_dict = dict()
from initialization import *


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def completed_sentence_change_one_char(input):
    optional_sentence = []
    for i in range(len(input)):
        for char in string.ascii_lowercase:
            if input != input[:i] + char + input[i + 1:]:
                optional_sentence.append({
                    'word': input[:i] + char + input[i + 1:],
                    'index': i
                })
    return optional_sentence


def completed_sentence_delete_one_char(input):
    optional_sentence = []
    for i in range(len(input)):
        if input != (input[:i] + input[i + 1:]):
            optional_sentence.append({
                'word': input[:i] + input[i + 1:],
                'index': i
            })
    return optional_sentence


def completed_sentence_add_one_char(input):
    optional_sentence = []
    for i in range(len(input)):
        for char in string.ascii_lowercase:
            if input != input[:i] + char + input[i:]:
                optional_sentence.append({
                    'word': input[:i] + char + input[i:],
                    'index': i
                })
    return optional_sentence


def get_res_of_search(dict, searching, case):
    all_possible_src = []
    searching_words = searching['word'].split(' ')
    if len(searching_words) == 1:
        if dict.words_dict.get(searching_words[0]):
            src_arr = dict.words_trie.search(searching_words[0])
            return [AutoCompleteData(searching['word'], i, case, searching['index']) for i in src_arr]
    for i in range(len(searching_words)):
        if dict.words_dict.get(searching_words[i]):
            trie = dict.words_dict[searching_words[i]]
            if i == len(searching_words) - 1:
                break
            temp = trie.search(searching_words[i + 1])
            if i == 0:
                all_possible_src = temp
            else:
                all_possible_src = intersection(temp, all_possible_src)
    return [AutoCompleteData(searching['word'], i, case, searching['index']) for i in all_possible_src]


def cli():
    dict = StoreData()
    open_file('mini-data')
    while True:
        searching = input('search in google or enter webSite Address:\n')
        auto_complete_data_arr = get_res_of_search(dict, {'word': searching, 'index': -1}, 'not_changed')
        for i in range(min(len(auto_complete_data_arr), 5)):
            print(auto_complete_data_arr[i])
        if len(auto_complete_data_arr) < 5:
            changed_and_deleted_arr = list()
            changed_arr = completed_sentence_change_one_char(searching)
            deleted_arr = completed_sentence_delete_one_char(searching)
            add_data = completed_sentence_add_one_char(searching)
            for i in range(len(changed_arr)):
                changed_and_deleted_arr += get_res_of_search(dict, changed_arr[i], 'changed')
            for i in range(len(deleted_arr)):
                changed_and_deleted_arr += get_res_of_search(dict, deleted_arr[i], 'delete_one')
            for i in range(len(add_data)):
                changed_and_deleted_arr += get_res_of_search(dict, add_data[i], 'add_one')
            hiest_score_arr = [AutoCompleteData('', (0, ''), '', -1, False)] * 5
            max_score = 0
            for i in range(len(changed_and_deleted_arr)):
                if changed_and_deleted_arr[i].score >= max_score:
                    max_score = changed_and_deleted_arr[i].score
                    hiest_score_arr = [changed_and_deleted_arr[i]] + hiest_score_arr
                    hiest_score_arr.pop()
            for i in range(min(5 - len(auto_complete_data_arr), len(hiest_score_arr))):
                if hiest_score_arr[i].is_real:
                    print(hiest_score_arr[i])
            if len(changed_and_deleted_arr) == 0:
                print('not suitable data')


if __name__ == '__main__':
    cli()
