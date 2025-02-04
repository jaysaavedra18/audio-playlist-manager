# audio_file.py
class AudioFile:
    """AudioFile class to store information about an audio file."""

    def __init__(
        self,
        index: int,
        song_name: str,
        artist: str,
        artist_link: str,
        duration: float,
        filename: str,
        file_size: float,
        licenses: list[str],
        genres: list[str],
        moods: list[str],
    ) -> None:
        """Initialize the AudioFile object."""
        self.index = index
        self.song_name = song_name
        self.artist = artist
        self.artist_link = artist_link
        self.duration = duration
        self.filename = filename
        self.file_size = file_size
        self.licenses = licenses
        self.genres = genres
        self.moods = moods

    def to_dict(self) -> dict:
        """Return a dictionary representation of the audio file."""
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
            "moods": self.moods,
        }

    def print_info(self) -> None:
        """Print information about the audio file."""
        print(f"Index: {self.index}")
        print(f"Song Name: {self.song_name}")
        print(f"Artist: {self.artist}")
        print(f"Artist Link: {self.artist_link}")
        print(f"Duration: {self.duration}")
        print(f"Filename: {self.filename}")
        print(f"File Size: {self.file_size}")
        print("Licenses:")
        for line in self.licenses:
            print(f"  - {line}")
        print("Genre:")
        for g in self.genre:
            print(f"  - {g}")
        print("Moods:")
        for mood in self.moods:
            print(f"  - {mood}")

    def add_mood(self, mood: str) -> None:
        """Add a mood to the audio file."""
        if mood not in self.moods:
            self.moods.append(mood)
            print(f"Added '{mood}' mood to '{self.song_name}'")

    def add_genre(self, genre: str) -> None:
        """Add a genre to the audio file."""
        if genre not in self.genre:
            self.genre.append(genre)
            print(f"Changed genre to '{genre}' for '{self.song_name}'")
