from typing import get_args
from coalesced import extract_coalesced, repack_coalesced
from utils import get_args

if __name__ == "__main__":
    filename, mode = get_args()
    if mode == "d":
        extract_coalesced(filename)
    elif mode == "c":
        repack_coalesced(filename)
    else:
        raise ValueError("Invalid mode")