import copy
import random
import sys
from enum import Enum
from typing import Collection, List, NamedTuple, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame
"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""


class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.
        """
        self.tactic = BoggleGame.SearchTactic.SEARCH_BOARD
        self.score = 0
        self.board = [[""]]
        self.size = int
        self.dictionary = BoggleDictionary
        self.cubes = []
        self.guessed_valid_words = []
        self.remaining_words = set()
        self.all_valid_words = set()
        self.path_of_word = set()

        self.visited = set()

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        self.dictionary = dictionary
        self.score = 0   # resets score
        self.guessed_valid_words = []  # resets words guessed
        self.remaining_words = set()
        self.all_valid_words = set()  # resets all valid words
        self.path_of_word = set()
        self.visited = set()

        self.size = size
        self.board = [[] for _ in range(size)]
        self.cubes = []  # resets cubes to empty string

        with open(cubefile, 'r') as f:
            for i in f.readlines():
                self.cubes.append(i.strip().lower())
        random.shuffle(self.cubes)

        counter = 0
        for i in range(size):
            for _ in range(size):
                self.board[i].append(random.choice(self.cubes[counter]))
                counter += 1

        self.all_valid_words = self.get_all_words()

    def get_board(self) -> List[List[str]]:
        return self.board

    def add_word(self, word: str) -> int:
        self.get_all_words()
        word = word.lower()
        if word in self.all_valid_words:
            if word not in self.guessed_valid_words:
                self.guessed_valid_words.append(word)
                return len(word) - 3
            else:
                return 0
        else:
            return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        self.get_all_words()
        if not self.guessed_valid_words:
            return None
        else:
            word = self.guessed_valid_words[-1]
            for paths in self.path_of_word:
                if paths[0] == word:
                    coords = paths[1]
                    return list(coords)

    def set_game(self, board: List[List[str]]) -> None:
        self.board = board
        self.size = len(board)
        self.score = 0  # resets score
        self.guessed_valid_words = []  # resets words guessed
        self.remaining_words = set()
        self.all_valid_words = set()  # resets all valid words
        self.visited = set()
        self.path_of_word = set()
        self.all_valid_words = self.get_all_words()

    def get_all_words(self) -> Collection[str]:
        if self.tactic == BoggleGame.SearchTactic.SEARCH_BOARD:
            return self.__board_driven_search()
        else:
            return self.__dictionary_driven_search()

    def set_search_tactic(self, tactic: BoggleGame.SearchTactic) -> None:
        self.tactic = tactic

    def get_score(self) -> int:
        score = 0
        for i in self.guessed_valid_words:
            score += len(i) - 3
        return score

    def dfs(self, row, column, node, prefix, coordinates):
        """Recursive call on the board to find all sequences of strings.

        Checks whether prefix string is in the dictionary trie. If the node is
        an end of a word, then add that word to the set of results

        Returns:
            None
        """
        if (row < 0 or column < 0 or row == len(self.board) or column == len(self.board)
                or (row, column) in self.visited or self.board[row][column] not in node.children):  # base case
            return
        self.visited.add((row, column))
        coordinates.append((row, column))  # update coordinates of prefix
        node = node.children[self.board[row][column]]
        prefix += self.board[row][column]
        if node.is_end:
            if len(prefix) >= 4:
                self.all_valid_words.add(prefix)
                self.path_of_word.add((prefix, tuple(coordinates)))

        self.dfs(row - 1, column - 1, node, prefix, coordinates)
        self.dfs(row - 1, column, node, prefix, coordinates)
        self.dfs(row - 1, column + 1, node, prefix, coordinates)
        self.dfs(row, column - 1, node, prefix, coordinates)
        self.dfs(row, column + 1, node, prefix, coordinates)
        self.dfs(row + 1, column - 1, node, prefix, coordinates)
        self.dfs(row + 1, column, node, prefix, coordinates)
        self.dfs(row + 1, column + 1, node, prefix, coordinates)

        self.visited.remove((row, column))
        coordinates.pop()  # remove current coordinate

    def __dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """

        for i in self.dictionary.root.children:  # at most 26 calls, i is a single letter string
            starting_coords = []
            self.visited = set()

            for row in range(len(self.board)):  # find potential starting points
                for column in range(len(self.board)):
                    letter = self.board[row][column]
                    if i == letter:  # found a match
                        starting_coords.append((row, column))

            if starting_coords:
                for starting_coord in starting_coords:  # loop through all potential starting coordinates
                    self.dfs(starting_coord[0], starting_coord[1], self.dictionary.root, "", [])

        return self.all_valid_words

    def __board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """
        self.visited = set()  # set of all coordinates on board that have been visited

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.dfs(i, j, self.dictionary.root, "", [])

        return self.all_valid_words
