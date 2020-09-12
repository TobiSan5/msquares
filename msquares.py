from random import random, shuffle
from itertools import combinations
from typing import Tuple, List, Dict
import sys
from copy import deepcopy


class Board:
    """
    Board of n x x size, with cells with coordinates row, column.
    """
    def __init__(self, n):
        # check for valid value of n
        if type(n) != int or n < 3:
            raise ValueError("Order by n parameter needs to be egual to or greater than 3.")

        # setup lines dict with coordinate tuples
        lines = {}
        for y in range(n):
            lr = lines[f"r{y}"] = {}
            lr["coords"] = tuple([(y, x) for x in range(n)])
            lr["sum"] = 0
        for x in range(n):
            lc = lines[f"c{x}"] = {}
            lc["coords"] = tuple([(y, x) for y in range(n)])
            lc["sum"] = 0
        x1, y1, x2, y2 = 0, 0, 0, n-1
        ld1 = lines["d1"] = {}
        ld1["coords"] = tuple([(y1+i, x1+i) for i in range(n)])
        ld1["sum"] = 0
        ld2 = lines["d2"] = {}
        ld2["coords"] = tuple([(y2-i, x2+i) for i in range(n)])
        ld2["sum"] = 0
        self.lines = lines
        
        #setup board dictionary, with tuples as key
        board = {(y, x): {} for x in range(n) for y in range(n)}
        for k in board.keys():
            board[k]["value"] = 0
            board[k]["line_idx"] = []
            for lnam in lines.keys():
                for coord in lines[lnam]["coords"]:
                    if coord == k:
                        board[k]["line_idx"].append(lnam)
        self.board = board
        self.m_sum = n * (n**2 +1) // 2
        self.dim = n
        self.depleted = set()
        self.free = set([x for x in range(1, n**2 +1)])
        self.n_top = n**2
        self.ns = 0
        self.lim = None
        self.mss = 0
        self.results = {}

    def random_free(self):
        """
        Return a list of unused elements in random order.
        """
        n = list(self.free)
        shuffle(n)
        return n
    
    def ordered_free(self):
        """
        Return a list with free elements in sorted order.
        """
        return sorted(list(self.free))
    
    def put_n(self, n: int, coord: Tuple[int, int]) -> bool:
        """
        Put number n into coordinate coord, if it fits. Then return True, False otherwise.
        """
        
        def write(n, coord):
            """
            Write a number into cell with corresponding coordinate.
            """
            self.board[coord]["value"] = n
            self.ns += 1
            self.free.remove(n)
            self.depleted.add(n)
            for line_key in self.board[coord]["line_idx"]:
                self.lines[line_key]["sum"] += n
            if self.ns == self.n_top:
                self.mss += 1
                self.results[self.mss] = {}
                self.results[self.mss]["board"] = deepcopy(self.board)
                self.results[self.mss]["lines"] = deepcopy(self.lines)
                print(f"Magic square no. {self.mss} found.")
                
        # conditional check if n fits
        ordered_free_minus_n = self.ordered_free()
        ordered_free_minus_n.remove(n)
        line_keys = self.board[coord]["line_idx"]
        sets_a = []
        diffs = []
        ns_lefts = []
        arr_gens = []
        fits = []
        for line_k in line_keys:
            sets_a.append(set([self.board[x]["value"] for x in self.lines[line_k]["coords"]]))
            sets_a[-1].discard(0)
            diffs.append(self.m_sum - sum(sets_a[-1]))
            ns_lefts.append(self.dim - len(sets_a[-1]))
            arr_gens.append(combinations(self.random_free(), ns_lefts[-1]))
            fits.append(False)
                   
        for i in range(len(sets_a)):
            if 1 == ns_lefts[i]:
                if n != diffs[i]:
                    return False
                else:
                    fits[i] = True
                    continue
            else:
                if (n + sum(ordered_free_minus_n[:ns_lefts[i] -1])) > diffs[i]:
                    return False

            for cmb in arr_gens[i]:
                if sum(cmb) == diffs[i]:
                    if n in cmb:
                        fits[i] = True
                        break
                    
        if False not in fits:
            write(n, coord)
            if self.mss == self.lim:
                raise InterruptedError(f"Limit of {self.lim} magic squares reached. Aborting program.")
            return True
        
        return False
                                        
    def next_empty_key(self) -> Tuple[int, int]:
        """
        Return the coordinate of next cell with value 0.
        """
        for k in self.board:
            if self.board[k]["value"] == 0:
                return k
        return (None, None)
            
    def show(self) -> None:
        """
        Print the results, with numbers in place and sum of each line.
        """
        for k in self.results.keys():
            print("\n\n")
            print(f"{self.results[k]['lines']['d1']['sum']:<5}")
            for r in [x for x in self.results[k]['lines'].keys() if x[0] == "r"]:
                print(" " * 5, end="")
                print("|", end="")
                for y in self.results[k]['lines'][r]["coords"]:
                    val = self.results[k]['board'][y]["value"]
                    print(f" {val:>2} ", end="|")
                print(f"{self.results[k]['lines'][r]['sum']:>4}")
                print(" " * 5, "|", "----|" * self.dim, sep="")
            print(f"{self.results[k]['lines']['d2']['sum']:<5}", end="")
            for c in [x for x in self.results[k]['lines'].keys() if x[0]== "c"]:
                print(f"{self.results[k]['lines'][c]['sum']:^5}", end="")
            
            
    def put2coord(self, n: int, coord: Tuple[int, int]) -> None:
        """
        Start with given number and coordinate, and loop through free elements and call itself
        recursively on next empty cell.
        """

        def backtrack(n, coord):
            """
            Reststore state of board to state prior to placing number.
            """
            self.board[coord]["value"] = 0
            self.ns -= 1
            self.free.add(n)
            self.depleted.remove(n)
            for line_key in self.board[coord]["line_idx"]:
                self.lines[line_key]["sum"] -= n
              
        if coord == (None, None):
            return
        
        if self.put_n(n, coord):
            choices = self.random_free()
            next_empty = self.next_empty_key()
            for el in choices:
                self.put2coord(el, next_empty)
            backtrack(n, coord)
        return
                
    def solve(self, pre_puts: Tuple[int, Tuple[int, int]]=None, lim=None) -> None:
        """
        Start the recursive process with a number and coordinate.
        Optional: Prefill board with chosen numbers in chosen coordinates.
        """
        if lim:
            self.lim = lim
        if pre_puts:
            for n, coord in pre_puts:
                self.put_n(n, coord)
        start_coord = self.next_empty_key()        
        try:
            for n in self.random_free():
                self.put2coord(n, start_coord)
        except BaseException as e:
            print(f"\n{e}\n")
        finally:
            print("Results:")
            self.show()
            print("\nFinished.")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("The program needs to get passed an argument for the order of magic square.")
    b = Board(int(sys.argv[1]))

    if len(sys.argv) >= 3:
        b.solve(lim=int(sys.argv[2]))
    else:
        b.solve()