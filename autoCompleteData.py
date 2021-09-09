import linecache
from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int
    __num_line: int
    __file: str
    __input_word: str

    def __init__(self, input_word, word_src, status, index, is_real = True):
        self.__file = word_src[1]
        self.__num_line = word_src[0]
        self.__input_word = input_word
        self.__status = status
        self.__index = index
        self.completed_sentence = self.get_completed_sentence().replace('\n', '')
        self.source_text = self.__file.split('\\')[-1] + ' ' + str(self.__num_line)
        self.offset = self.get_offset()
        self.score = self.get_score()
        self.is_real = is_real

    def __str__(self):
        return f'completed_sentence: {self.completed_sentence}, source_text: {self.source_text}, offset: {self.offset} , score: {self.score}'

    def get_completed_sentence(self):
        try:
            return linecache.getline(self.__file, self.__num_line)
        except OSError:
            print("Oops! That was no valid file. Try again...")
            return

    def get_offset(self):
        return self.completed_sentence.find(self.__input_word)

    def get_score(self):
        if self.__status == 'not_changed':
            return len(self.__input_word) * 2
        elif self.__status == 'add_one' or self.__status == 'delete_one':
            if self.__index > 3:
                return (len(self.__input_word) * 2) - 2
            else:
                return (len(self.__input_word) * 2) - (10 - self.__index * 2)
        elif self.__status == 'changed':
            if self.__index > 3:
                return (len(self.__input_word) * 2) - 1
            else:
                return (len(self.__input_word) * 2) - (5 - self.__index)
