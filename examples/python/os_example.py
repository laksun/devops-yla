from os import rename
from pathlib import Path

original_path = Path("examples/python/rename.txt")

renamed = Path("examples/python/renamed.txt")

original_path.rename(renamed)
