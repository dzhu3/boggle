"""
This module contains the definition of an abstract game class.
Your concrete implementation inherits from the abstract class.
"""

import enum
from abc import ABC, abstractmethod
from typing import Collection, List, Optional, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary


class BoggleGame(ABC):
    """
    This abstract class defines the game logic for Boggle.
    """

    @enum.unique
    class SearchTactic(enum.Enum):
        """An enum for the possible tactics when searching for words."""

        # Search through the board in a depth-first search, checking
        # for valid words.
        SEARCH_BOARD = enum.auto()

        # Go through every dictionary word, and see if they exist on
        # the board.
        SEARCH_DICT = enum.auto()

    # The default search tactic to use if none are provided.
    SEARCH_DEFAULT = SearchTactic.SEARCH_BOARD

    @abstractmethod
    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """Create a new Boggle game using a `size` x `size` board and
        the cubes specified in the file `cubefile`.

        Args:
            size: The size of the Boggle Board.
            cubefile: Name of a file containing the cubes.
            dict: A `BoggleDictionary` of valid words.

        Raises:
            OSError: The `cubefile` cannot be opened or read.

        Note:
            This is NOT the constructor for the class.
            Instead, it sets the internal state of the class to a new, playable game.
            Your `MyGameManager` constructor must not take any parameters.

        Example Usage
        -------
        dictionary = MyGameDictionary()
        dictionary.load_dictionary("words.txt")
        game = MyGameManager()
        game.new_game(4, 2, "cubes.txt", dictionary)
        """
        raise NotImplementedError("abstract method `new_game`")

    @abstractmethod
    def get_board(self) -> List[List[str]]:
        """Return a `size` x `size` character matrix representing the
        Boggle board, in row-major order.
        """
        raise NotImplementedError("abstract method `get_board`")

    @abstractmethod
    def add_word(self, word: str) -> int:
        """Add a word to a list of guessed words.

        Each word can only be added once throughout the entirety of the
        game. This method should be case-insensitive.

        Args:
            word: The word to add.

        Returns:
            The point value of the word.

        If the word is invalid or the player cannot add the word, it
        is worth zero points and is not actually added to the guessed list.
        """
        raise NotImplementedError("abstract method `add_word`")

    @abstractmethod
    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """Return a list of coordinates showing the previous
        successfully added word.

        If there is no previous word, return `None`.

        The coordinates are listed by letter, then row, then column.
        That is, if `coords` is the return value, then:
        - `len(coords)` is the length of the last word added
        - `coords[0]` is the position of the first letter of the word
          - `coords[0][0]` is the row of the first letter of the word
          - `coords[0][1]` is the column of the first letter of the word
        - `coords[1]` is the position of the second letter...
        ... and so on
        """
        raise NotImplementedError("abstract method `get_last_added_word`")

    @abstractmethod
    def set_game(self, board: List[List[str]]) -> None:
        """Set the game board to the given board.

        The `board` should be in row-major order and must be square.

        Sets the current score to zero and resets guessed list.
        Other game-related parameters (like the dictionary) should be left as-is.
        """
        raise NotImplementedError("abstract method `set_game`")

    @abstractmethod
    def get_all_words(self) -> Collection[str]:
        """Return a collection containing all valid words in the current
        Boggle board.

        The words do not need to have any particular capitalization.
        Uses the current search tactic.
        """
        raise NotImplementedError("abstract method `get_all_words`")

    @abstractmethod
    def set_search_tactic(self, tactic: SearchTactic) -> None:
        """Set the search tactic to the given `tactic`.

        This tactic is used by `get_all_words()`. Valid tactics are
        defined above in `class SearchTactic`.
        """
        raise NotImplementedError("abstract method `set_search_tactic`")

    @abstractmethod
    def get_score(self) -> int:
        """Returns the current player score"""
        raise NotImplementedError("abstract method `get_score`")
