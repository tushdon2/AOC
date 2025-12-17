from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def fetch(year:str, day:str):
    file = f"{BASE_DIR}/{year}/inputs/{day}.txt"
    with open(file, 'r') as f:
        return f.read()