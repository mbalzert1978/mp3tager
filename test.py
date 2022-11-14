from pathlib import Path

from ShazamAPI import Shazam

file = Path("test.mp3").resolve()
file2 = Path("test2.mp3").resolve()
file3 = Path("test3.mp3").resolve()

mp3_file_content_to_recognize = file.read_bytes()

recognize_generator = Shazam(
    lang="de", timezone="Europe/Berlin", region="DE"
).recognize_song(mp3_file_content_to_recognize)
# or just:
#     recognize_generator = Shazam().recognize_song('filename.mp3')
_, resp = next(recognize_generator)
title = resp["track"]["title"]
artist = resp["track"]["subtitle"]
genre = resp["track"]["genres"]["primary"]
print(artist)
print(title)
print(genre)
