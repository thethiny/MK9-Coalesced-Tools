from typing import get_args
from coalesced import extract_coalesced
from utils import get_args

if __name__ == "__main__":
    filename, mode = get_args()
    if mode == "d":
        extract_coalesced(filename)
    elif mode == "c":
        raise NotImplementedError("Compression not implemented yet")
    else:
        raise ValueError("Invalid mode")