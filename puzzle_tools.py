"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @param Puzzle puzzle: Puzzle
    @rtype: PuzzleNode| None

    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> pn2 = WordLadderPuzzle("on", "no", {"on", "oo", "no"})
    >>> sol = depth_first_solve(pn2)
    >>> print(sol)
    on -> no
    <BLANKLINE>
    oo -> no
    <BLANKLINE>
    no -> no
    <BLANKLINE>
    <BLANKLINE>
    """
    seen = set()

    # helper function
    def recs(puz, set_):
        """
        Return a valid solution in the form of PuzzleNode from given puz and
        make sure to ignore any extensions that are already in set_

        @param Puzzle puz : Puzzle to search
        @param Set set_: set to track
        @rtype: PuzzleNode
        """
        if not puz.extensions():
            if puz.is_solved():
                return PuzzleNode(puz, [])
            else:
                return None
        else:
            for move in puz.extensions():
                if str(move) not in seen:
                    set_.add(str(move))
                    r = recs(move, set_)
                    if not r:
                        continue
                    else:
                        curr = PuzzleNode(puz, [r], None)
                        r.parent = curr
                        return curr
    return recs(puzzle, seen)


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> pn2 = WordLadderPuzzle("on", "no", {"on", "oo", "no"})
    >>> sol = breadth_first_solve(pn2)
    >>> print(sol)
    on -> no
    <BLANKLINE>
    oo -> no
    <BLANKLINE>
    no -> no
    <BLANKLINE>
    <BLANKLINE>
    """
    q = deque()
    q.append(PuzzleNode(puzzle))
    seen = set()
    # if q is not empty
    while q:
        # pop first node entered
        lnk = q.popleft()
        # check if node is solution
        if lnk.puzzle.is_solved():
            # return lnk
            if not lnk.parent:
                return lnk
            else:
                return invert(lnk)
        # popped value isn't solution
        else:
            # if node not in seen and has extensions
            if lnk.puzzle.extensions() != [] and not puzzle.fail_fast():
                for move in lnk.puzzle.extensions():
                    if str(move) not in seen:
                        seen.add(str(move))
                        q.append(PuzzleNode(move, [], lnk))
            # if node is in seen or doesnt have extensions
            else:
                continue
    return None


# helper method to breadth first search
def invert(lk):
    """
    Return a valid path, made up of a list of PuzzleNode children, after linking
    the parent references from lk

    @param PuzzleNode lk: PuzzleNode that has a parent reference
    @return: PuzzleNode
    """
    q = deque()
    q.append(lk)
    while q:
        val = q.pop()
        if val.parent:
            pn = val.parent
            pn.children.append(val)
            q.append(pn)
        else:
            return val


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))