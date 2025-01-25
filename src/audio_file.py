# audio_file.py
class AudioFile:
    def __init__(self, index, song_name, artist, artist_link, duration, filename, file_size, licenses, genre, moods):
        self.index = index
        self.song_name = song_name
        self.artist = artist
        self.artist_link = artist_link
        self.duration = duration
        self.filename = filename
        self.file_size = file_size
        self.licenses = licenses
        self.genre = genre
        self.moods = moods

    def to_dict(self):
        return {
            "index": self.index,
            "song_name": self.song_name,
            "artist": self.artist,
            "artist_link": self.artist_link,
            "duration": self.duration,
            "filename": self.filename,
            "file_size": self.file_size,
            "licenses": self.licenses,
            "genre": self.genre,
            "moods": self.moods
        }

    def print_info(self):
        print(f"Index: {self.index}")
        print(f"Song Name: {self.song_name}")
        print(f"Artist: {self.artist}")
        print(f"Artist Link: {self.artist_link}")
        print(f"Duration: {self.duration}")
        print(f"Filename: {self.filename}")
        print(f"File Size: {self.file_size}")
        print("Licenses:")
        for license in self.licenses:
            print(f"  - {license}")
        print("Genre:")
        for g in self.genre:
            print(f"  - {g}")
        print("Moods:")
        for mood in self.moods:
            print(f"  - {mood}")

    def add_mood(self, mood):
        if mood not in self.moods:
            self.moods.append(mood)
            print(f"Added '{mood}' mood to '{self.song_name}'")

    def add_genre(self, genre):
        if genre not in self.genre:
            self.genre.append(genre)
            print(f"Changed genre to '{genre}' for '{self.song_name}'")

