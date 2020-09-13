import sys
from boards import MSBoard
from typing import Tuple

def solve(msboard, pre_puts: Tuple[int, Tuple[int, int]]=None, lim=None) -> None:
    """
    Start the recursive process with a number and coordinate.
    Optional: Prefill board with chosen numbers in chosen coordinates.
    """
    if lim:
        msboard.lim = lim
    if pre_puts:
        for n, coord in pre_puts:
            msboard.write(n, coord)
    start_coord = msboard.next_empty_key()        
    try:
        for n in msboard.random_free():
            msboard.put2coord(n, start_coord)
    except BaseException as e:
        print(f"\n{e}\n")
    finally:
        print("Results:")
        msboard.show()
        print("\nFinished.")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("The program needs to get passed an argument for the order of magic square.")
    b = MSBoard(int(sys.argv[1]))

    if len(sys.argv) >= 3:
        solve(b, lim=int(sys.argv[2]))
    else:
        solve(b)