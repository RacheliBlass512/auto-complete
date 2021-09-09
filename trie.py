# Python program for insert and search
# operation in a Trie

class TrieNode:

    # Trie node class
    def __init__(self):
        self.children = {}

        # is_and_of_word is True if node represent the end of the word
        self.is_and_of_word = False
        self.words_src = []


class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def insert(self, key, word_src=''):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        p_crawl = self.root
        length = len(key)
        for level in range(length):
            index = key[level]

            # if current character is not present
            # print(index, key[level], word_src)
            if not p_crawl.children.get(index):
                p_crawl.children[index] = self.get_node()
            p_crawl = p_crawl.children[index]

        # mark last node as leaf
        p_crawl.is_and_of_word = True
        p_crawl.words_src.append(word_src)

    def search(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        p_crawl = self.root
        length = len(key)
        for level in range(length):
            index = key[level]
            if not p_crawl.children.get(index):
                return ''
            p_crawl = p_crawl.children[index]

        return p_crawl.words_src
