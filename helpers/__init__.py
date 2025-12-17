from pathlib import Path
from typing import Callable
from time import time

BASE_DIR = Path(__file__).parent.parent

def fetch(year:str, day:str) -> str:
    file = f"{BASE_DIR}/{year}/inputs/{day}.txt"
    with open(file, 'r') as f:
        return f.read()
    
def function_runner(*funcs:list[Callable[[], any]]) -> None:
    for fn in funcs:
        st = time()
        print(f"{fn.__name__} result: {fn()} (took {time() - st:.4f} seconds)")