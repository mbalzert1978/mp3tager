from ShazamAPI import Shazam


def shazam_it(root, tag) -> None:
    mp3_file_content_to_recognize = root.read_bytes()
    recognize_generator = Shazam(
        lang="de", timezone="Europe/Berlin", region="DE"
    ).recognize_song(mp3_file_content_to_recognize)
    _, resp = next(recognize_generator)
    if resp.get("matches"):
        tag.title = resp.get("track", {}).get("title")
        tag.artist = resp.get("track", {}).get("subtitle")
        tag.genre = resp.get("track", {}).get("genres", {}).get("primary")
