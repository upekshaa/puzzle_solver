from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __str__(self):
        """
        Return a human-friendly string representation of an instance of class
        WordLadderPuzzle

        @param WordLadderPuzzle self: this WordLadderPuzzle
        @rtype: str


        >>> word_set = {'cast', 'cave', 'save'}
        >>> w = WordLadderPuzzle("same", "cost", word_set)
        >>> print(w)
        same -> cost
        """
        # return ("initial word: {}, resulting word: {}".format(
        #     self._from_word, self._to_word))
        return "{} -> {}".format(self._from_word, self._to_word)

    def __eq__(self, other):
        """
        Return whether self WordLadderPuzzle is equivalent to other

        @param WordLadderPuzzle self: this WordLadderPuzzle
        @param WordLadderPuzzle|object other: object to compare to self
        @rtype: bool

        >>> word_set = {'cast', 'cave', 'save'}
        >>> w = WordLadderPuzzle("same", "cost", word_set)
        >>> v = WordLadderPuzzle("same", "cost", word_set)
        >>> m = WordLadderPuzzle("same", "lost", word_set)
        >>> w == v
        True
        >>> m == w
        False
        """
        return (type(self) == type(other) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __repr__(self):
        """
        Return a string representation of an instance of class WordLadderPuzzle

        @param WordLadderPuzzle self: this WordLadderPuzzle
        @rtype: str

        >>> word_set = {'cast', 'cave', 'save'}
        >>> w = WordLadderPuzzle("same", "cost", word_set)
        >>> w
        same -> cost
        """
        return str(self)

    def extensions(self):
        """
        Returns all legal extensions possible that can be reached by
        changing a single letter in from_word to one of those in self._chars

        @param WordLadderPuzzle self: this Puzzle
        @rtype: list[Puzzle]

        >>> word_set = {'cast', 'cave', 'save', 'cost'}
        >>> w = WordLadderPuzzle("same", "cost", word_set)
        >>> l = ['save']
        >>> l.sort() == w.extensions().sort()
        True
        >>> word_set2 = {'cast', 'cave', 'save', 'sane', 'cost'}
        >>> w2 = WordLadderPuzzle("same", "cost", word_set)
        >>> l2 = ['save', 'sane']
        >>> l2.sort() == w2.extensions().sort()
        True
        >>> word_set = {'cast', 'cave', 'save', 'sane', 'cost'}
        >>> w3 = WordLadderPuzzle("do", "cost", word_set)
        >>> l3 = []
        >>> l3.sort() == w3.extensions().sort()
        True
        """
        temp = []
        final = []

        if self._from_word == self._to_word:
            return final

        for word in self._word_set:
            count = 0
            if len(word) == len(self._from_word):
                for ch, char in zip(self._from_word, word):
                    if ch != char:
                        count += 1
            else:
                continue

            if count == 1:
                temp.append(word)

        for word in temp:
            final.append(WordLadderPuzzle(word, self._to_word, self._word_set))
        return final

    def is_solved(self):
        """
        Return true if
        @param WorldLadderPuzzle self:
        @return: bool
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r", encoding='UTF-8') as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
