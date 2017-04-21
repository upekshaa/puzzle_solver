from puzzle import Puzzle
from copy import deepcopy

class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __str__(self):
        """
        Return a human friendly string representation of an instance of class
        self

        @param MNPuzzle self: this MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> start_grid2 = (("2", "*", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn)
        start grid: (('*', '2', '3'), ('1', '4', '5'))
        target grid: (('1', '2', '3'), ('4', '5', '*'))
        >>> mn2 = MNPuzzle(start_grid2, target_grid)
        >>> print(mn2)
        start grid: (('2', '*', '3'), ('1', '4', '5'))
        target grid: (('1', '2', '3'), ('4', '5', '*'))
        """
        return ("start grid: {}\ntarget grid: {}".format(self.from_grid,
                                                         self.to_grid))

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other

        @param MNPuzzle self: this MNPuzzle
        @param MNPuzzle|object other: object to compare to self
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> start_grid2 = (("2", "*", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn1 = MNPuzzle(start_grid, target_grid)
        >>> mn2 = MNPuzzle(start_grid2, target_grid)
        >>> mn == mn1
        True
        >>> mn == mn2
        False
        """
        return (type(self) == type(other) and
                self.m == other.m and
                self.n == other.n and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __repr__(self):
        """
        Return a string representation of an instance of class MNPuzzle

        @param MNPuzzle self: this MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> start_grid2 = (("2", "*", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn
        MNPuzzle((('*', '2', '3'), ('1', '4', '5')), (('1', '2', '3'), \
('4', '5', '*')))
        >>> mn2 = MNPuzzle(start_grid2, target_grid)
        >>> mn2
        MNPuzzle((('2', '*', '3'), ('1', '4', '5')), (('1', '2', '3'), \
('4', '5', '*')))
        """
        return "MNPuzzle({}, {})".format(self.from_grid, self.to_grid)

    def extensions(self):
        """
        Return list of legal extensions of Puzzle self.

        This is an overridden method of parent class Puzzle

        @param self : this MNPuzzle
        @rtype: tuple[tuple[str]]
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> mn.extensions()
        [MNPuzzle((('1', '2', '3'), ('*', '4', '5')), (('1', '2', '3'), ('4', '5', '*'))), MNPuzzle((('2', '*', '3'), ('1', '4', '5')), (('1', '2', '3'), ('4', '5', '*')))]
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid2 = (("5", "2", "3"), ("1", "4", "*"))
        >>> mn2 = MNPuzzle(start_grid2, target_grid2)
        >>> mn2.extensions()
        [MNPuzzle((('5', '2', '*'), ('1', '4', '3')), (('1', '2', '3'), ('4', '5', '*'))), MNPuzzle((('5', '2', '3'), ('1', '*', '4')), (('1', '2', '3'), ('4', '5', '*')))]
        >>> target_grid3 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid3 = (("5", "2", "*"), ("1", "4", "3"))
        >>> mn3 = MNPuzzle(start_grid3, target_grid3)
        >>> mn3.extensions()
        [MNPuzzle((('5', '2', '3'), ('1', '4', '*')), (('1', '2', '3'), ('4', '5', '*'))), MNPuzzle((('5', '*', '2'), ('1', '4', '3')), (('1', '2', '3'), ('4', '5', '*')))]
        >>> target_grid4 = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid4= (("5", "2", "1"), ("*", "4", "3"))
        >>> mn4 = MNPuzzle(start_grid4, target_grid4)
        >>> mn4.extensions()
        [MNPuzzle((('*', '2', '1'), ('5', '4', '3')), (('1', '2', '3'), ('4', '5', '*'))), MNPuzzle((('5', '2', '1'), ('4', '*', '3')), (('1', '2', '3'), ('4', '5', '*')))]

        """
        grid = deepcopy([list(x) for x in self.from_grid])
        has_empty_, r_index, c_index = None, 0, 0
        legal_moves = []

        if self.from_grid == self.to_grid:
            return legal_moves

        #find empty spot
        for row in grid:
            for value in row:
                if value == "*":
                    r_index = grid.index(row)
                    c_index = row.index(value)
                    has_empty_ = True

        if has_empty_:
            if r_index - 1 >= 0:
                #up move
                up_grid = deepcopy(grid)
                up_grid[r_index][c_index], up_grid[r_index - 1][c_index] = up_grid[r_index - 1][c_index], up_grid[r_index][c_index]
                legal_moves.append(tuple(tuple(x) for x in up_grid))
            if r_index + 1 < len(grid):
                #down move
                down_grid = deepcopy(grid)
                down_grid[r_index][c_index], down_grid[r_index + 1][c_index] = down_grid[r_index + 1][c_index], down_grid[r_index][c_index]
                legal_moves.append(tuple(tuple(x) for x in down_grid))
            if c_index - 1 >= 0:
                #left move
                left_grid = deepcopy(grid)
                left_grid[r_index][c_index], left_grid[r_index][c_index - 1] = left_grid[r_index][c_index - 1], left_grid[r_index][c_index]
                legal_moves.append(tuple(tuple(x) for x in left_grid))
            #if c_index + 1 <= len(grid[r_index]) >= 0:
            if c_index + 1 <= len(grid[r_index])-1:
                #right move
                right_grid = deepcopy(grid)
                right_grid[r_index][c_index], right_grid[r_index][c_index + 1] = right_grid[r_index][c_index + 1], right_grid[r_index][c_index]
                legal_moves.append(tuple(tuple(x) for x in right_grid))

        final = []
        for move in legal_moves:
            final.append(MNPuzzle(move, self.to_grid))
        return final


        #vertical move

    def is_solved(self):
        """
        return True iff MNPuzzle self is solved.

        This is an overridden method from parent class Puzzle

        @type self MNPuzzle: this MNPuzzle self
        @rtype: bool
        """

        return self.from_grid == self.to_grid



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
