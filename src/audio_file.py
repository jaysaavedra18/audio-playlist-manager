import os

from file_utils import read_text_blocks, parse_text_block_into_song, read_json, write_json, get_audio_info
from utils import format_time
from config import AUDIO_DIRECTORY, TEXT_FILE_PATH, MUSIC_DATA_PATH

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


def add_audio_files(): 
    audio_files = read_json(MUSIC_DATA_PATH, AudioFile) # List of AudioFile objects
    num_of_audio_files = len(audio_files) # Number of existing audio files in json data
    text_blocks = read_text_blocks(TEXT_FILE_PATH) # List of new data to be parsed
    num_of_text_blocks = len(text_blocks) # Number of new audio files to create
    
    print("Working on that data...")

    # Parse all data and store it in parsed set
    for index, text_block in enumerate(text_blocks):
        index += num_of_audio_files # Offset by existing objects
        # Get audio file data
        parsed_data = parse_text_block_into_song(text_block)
        song_name = parsed_data["song_name"]
        filename = song_name + '.mp3'
        filepath = os.path.join(AUDIO_DIRECTORY, filename)
        audio_info = get_audio_info([filepath])
        file_size = f"{audio_info[0] / (1024 * 1024):.2f} MB"
        duration = format_time(audio_info[1])

        # Build audio file
        audio_file = AudioFile(
            index=index,
            song_name=song_name,
            artist=parsed_data["artist_name"],
            artist_link=parsed_data["artist_link"],
            duration=duration,
            filename=filename,
            file_size=file_size,
            licenses=parsed_data["licenses"],
            genre=[],
            moods=[]
        )

        audio_files.append(audio_file)
        print(f"Added {filename}.")
        
    write_json(objects=audio_files, output_path=MUSIC_DATA_PATH) # Append data
    open(TEXT_FILE_PATH, "w").close() # Remove input data onced transformed and written