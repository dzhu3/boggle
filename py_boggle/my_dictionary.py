import typing
from collections.abc import Iterator
import itertools
from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    def __init__(self, letter):
        self.letter = letter  # character stored in node
        self.is_end = False  # marker to signal end of word
        self.children = {}


class MyGameDictionary(BoggleDictionary):

    def __init__(self):
        self.root = TrieNode("")  # instantiate the root for the dictionary
        self.words = []

    def load_dictionary(self, filename: str) -> None:
        with open(filename, 'r') as f:
            words = f.readlines()

        for word in words:
            current_node = self.root
            word = word.lower().strip()
            for letter in word:
                if letter not in current_node.children:
                    new_node = TrieNode(letter)
                    current_node.children[letter] = new_node  # add new node to children
                    current_node = new_node
                else:
                    current_node = current_node.children[letter]

            current_node.is_end = True  # indicates end of a word

    def is_prefix(self, prefix: str) -> bool:
        current_node = self.root
        if prefix == '':
            return True
        prefix = prefix.lower()

        for i in prefix:
            if i not in current_node.children:
                return False
            else:
                current_node = current_node.children[i]
        return True

    def contains(self, word: str) -> bool:
        current_node = self.root
        word = word.lower()
        for i in word:
            if i not in current_node.children:
                return False
            else:
                current_node = current_node.children[i]

        if current_node.is_end:
            return True
        else:
            return False

    def dfs(self, node, prefix):
        prefix += node.letter
        if node.is_end:
            self.words.append(prefix)
        if not node.children:
            return
        for i in node.children.values():  # traverses through entire trie in lexicographic order
            self.dfs(i, prefix)

    def root(self):
        return self.root()

    def __iter__(self) -> typing.Iterator[str]:
        self.words = []
        self.dfs(self.root, "")  # fills self.words with all words in trie
        return iter(self.words)
