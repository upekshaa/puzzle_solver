from puzzle import Puzzle
import copy

class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]]) # check whether all each row is of equal length to the first row
        assert all([all(x in marker_set for x in row) for row in marker]) # checks whether every item in each row is a possible marker
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])  # checks whether each marker in marker_set is one of: #, *, .
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return True if this GridPegSolitairePuzzle self is equivalent to other

        @param self GridPegSolitairePuzzle: this GridPegSolitairePuzzle
        @param other GridPegSolitairePuzzle|Object: other object to compare to
        self
        @rtype:bool

        >>> grid = []
        >>> grid.append(['#', '*', '*', '*'])
        >>> grid.append(['*', '*', '.', '*'])
        >>> grid.append(['*', '*', '*', '#'])
        >>> m = {'#', '.', '*'}
        >>> p = GridPegSolitairePuzzle(grid, m)
        >>> grid1 = []
        >>> grid1.append(['#', '*', '*', '*'])
        >>> grid1.append(['*', '*', '.', '*'])
        >>> grid1.append(['*', '*', '*', '#'])
        >>> p1 = GridPegSolitairePuzzle(grid1, m)
        >>> p == p1
        True
        >>> grid2 = []
        >>> grid2.append(['#', '*', '*', '*'])
        >>> grid2.append(['#', '*', '.', '*'])
        >>> grid2.append(['#', '*', '*', '#'])
        >>> p2 = GridPegSolitairePuzzle(grid2, m)
        >>> p == p2
        False
        """
        return (self._marker_set == other._marker_set) and \
               (self._marker == other._marker)

    def __str__(self):
        """
        Return a string representation of an instance of class
        GridPegSolitairePuzzle

        @param self GridPegSolitairePuzzle: this GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [["*", "*", "*", "*", "*"],\
                    ["*", "*", "*", "*", "*"],\
                    ["*", "*", "*", "*", "*"],\
                    ["*", "*", ".", "*", "*"],\
                    ["*", "*", "*", "*", "*"]]
        >>> g1 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g1)
        * * * * * |
        * * * * * |
        * * * * * |
        * * . * * |
        * * * * * |
        >>> grid = [["#", "#", "*", "#", "#"],\
                    ["#", "*", "*", "*", "#"],\
                    ["*", "*", "*", "*", "*"],\
                    ["#", "*", ".", "*", "#"],\
                    ["#", "#", "*", "#", "#"]]
        >>> g2 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g2)
        # # * # # |
        # * * * # |
        * * * * * |
        # * . * # |
        # # * # # |
        """
        s = ''
        for row in self._marker:
            for x in row:
                s += x + ' '
            # add | to indicate end of row
            s += '|'+'\n'
        return s

    def __repr__(self):
        """
        Return a representation of an instance of class GridPegSolitairePuzzle

        @param self GridPegSolitairePuzzle: this GridPegSolitairePuzzle
        @rtype: str

        # NOTE : sets are unordered therefore these examples will always have
        # errors

        >>> grid = [["*", "*", "*", "*", "*"]]
        >>> g1 = GridPegSolitairePuzzle([["*", "*", "*", "*", "*"]],\
         {"*", ".", "#"})
        >>> g1
        GridPegSolitairePuzzle([['*', '*', '*', '*', '*']])
        >>> grid1 = [["#", "#", "*", "#", "#"]]
        >>> g2 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> g2
        GridPegSolitairePuzzle([['#', '#', '*', '#', '#']])
        """
        return "GridPegSolitairePuzzle({})".format(self._marker)


    def extensions(self):
        """
        Return list of legal extensions of Puzzle self.

        This is an overridden method of parent class Puzzle

        @param self : this GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", ".", "."],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.extensions()
        [GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '.'], ['*', '*', '.', '.', '*'], ['*', '*', '*', '.', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '.', '.', '*', '.'], ['*', '*', '.', '*', '*'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '.'], ['*', '*', '.', '.', '*'], ['*', '*', '*', '.', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '.', '.', '*', '.'], ['*', '*', '.', '*', '*'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '.', '*', '*'], ['*', '*', '.', '.', '.'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '*', '*', '.', '.'], ['*', '*', '*', '*', '*'], ['*', '*', '.', '*', '*'], ['*', '*', '.', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '*', '*', '.', '.'], ['*', '*', '*', '.', '.'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*']]), GridPegSolitairePuzzle([['*', '*', '*', '*', '*'], ['*', '*', '*', '.', '.'], ['.', '.', '*', '*', '*'], ['*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*']])]
        >>> grid2 = [["*"], ["*"], ['.'], ["*"], ["*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.extensions()
        [GridPegSolitairePuzzle([['.'], ['.'], ['*'], ['*'], ['*']]), GridPegSolitairePuzzle([['*'], ['*'], ['*'], ['.'], ['.']])]
        >>> grid3 = [["."], ["*"], ["*"]]
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gpsp3.extensions()
        [GridPegSolitairePuzzle([['*'], ['.'], ['.']])]
        """
        # for simplification
        grid = self._marker

        possible_move, has_empty_, r_index, c_index = [], None, 0, 0
        # find index: (c_index, r_index)
        for row in grid:
             for i in row:
                 if i == ".":
                     # has_empty_ = True
                     c_index = row.index(i)
                     r_index = grid.index(row)

                     #vertical down move
                     if r_index >= 2 and grid[r_index -1][c_index] == "*" and grid[r_index - 2][c_index] == "*":
                         up_temp = copy.deepcopy(grid)
                         up_temp[r_index - 1][c_index] = "."
                         up_temp[r_index - 2][c_index] = "."
                         up_temp[r_index][c_index] = "*"
                         possible_move.append(up_temp)

                     # vertical up move
                     if r_index + 3 <= len(grid) and grid[r_index + 2][c_index] == "*" and grid[r_index + 1][c_index] == "*":
                         down_temp = copy.deepcopy(grid)
                         down_temp[r_index + 1][c_index] = "."
                         down_temp[r_index + 2][c_index] = "."
                         down_temp[r_index][c_index] = "*"
                         possible_move.append(down_temp)

                     # horizontal left move
                     if c_index + 3 <= len(grid[0]) and grid[r_index][c_index + 2] == "*" and grid[r_index][c_index + 1] == "*":
                         left_temp = copy.deepcopy(grid)
                         left_temp[r_index][c_index + 2] = "."
                         left_temp[r_index][c_index + 1] = "."
                         left_temp[r_index][c_index] = "*"
                         possible_move.append(left_temp)

                     # horizontal right move
                     if c_index >= 2 and grid[r_index][c_index - 2] == "*" and grid[r_index][c_index - 1] == "*":
                         right_temp = copy.deepcopy(grid)
                         right_temp[r_index][c_index - 2] = "."
                         right_temp[r_index][c_index - 1] = "."
                         right_temp[r_index][c_index] = "*"
                         possible_move.append(right_temp)

        final = []
        for move in possible_move:
            final.append((GridPegSolitairePuzzle(move, self._marker_set)))
        return final


    def is_solved(self):
        """
        Return True iff Puzzle self is solved.

        This is an overridden method from parent class Puzzle

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [["*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*"], ["*", "*", "*", "*", "*"], ["*", "*", ".", "*", "*"], ["*", "*", "*", "*", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        False
        >>> grid2 = [[".", ".", ".", ".", "."], [".", ".", ".", ".", "."], [".", ".", ".", ".", "."], [".", ".", ".", "*", "."], [".", ".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.is_solved()
        True
        """

        count = 0

        for row in self._marker:
            for pos in row:
                if pos == "*":
                    count += 1

        return count == 1



if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time
    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
