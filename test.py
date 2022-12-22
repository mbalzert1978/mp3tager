from pathlib import Path

from src.reader.reader import MutagenReader, TagReader

reader = TagReader()
result = reader.read(Path("gym.mp3"))
for tag in result:
    print(tag)
