import os
import json
from pydub import AudioSegment
from typing import List

from text_file import read_text_blocks, get_unique_file_name, parse_text_block, delete_first_block

TEXT_FILE_PATH = "/Users/saavedj/SimpleSolutions/data/references.txt"
MUSIC_PATH = '/Users/saavedj/SimpleSolutions/music'
DATA_DIRECTORY = '/Users/saavedj/SimpleSolutions/data'
MUSIC_DATA_PATH = os.path.join(DATA_DIRECTORY, "music_data.json")

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


def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3") or f.endswith(".wav")]


def get_audio_info(audio_files: List[str]):
    total_size = sum(os.path.getsize(file) for file in audio_files)
    total_length = sum(AudioSegment.from_file(
        file).duration_seconds for file in audio_files)
    return total_size, total_length


def concatenate_audio(selected_files, audio_directory):
    concatenated_audio = AudioSegment.silent(duration=0)

    for file in selected_files:
        audio_path = os.path.join(audio_directory, file)
        audio_segment = AudioSegment.from_file(audio_path)
        concatenated_audio += audio_segment

    return concatenated_audio


def export_audio(audio, file_path):
    audio.export(get_unique_file_name(file_path), format="mp3")


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def write_json(objects, output_path):
    # Serialize to JSON
    json_data = [vars(file) for file in objects]

    # Determine the mode based on file existence
    # if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
    if False: # Always overwrite
        mode = "a"  # Append mode if the file exists and is not empty
    else:
        mode = "w"  # Write mode if the file does not exist or is empty

    # Write JSON data to the file
    with open(output_path, mode) as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json():
    try:
        # Read JSON data back into AudioFile objects
        with open(MUSIC_DATA_PATH, "r") as json_file:
            loaded_data = json.load(json_file)
    except json.JSONDecodeError:
        # Handle empty JSON file or invalid JSON data
        return []

    # Convert JSON data back to AudioFile objects
    loaded_audio_files = [AudioFile(**data) for data in loaded_data]
    return loaded_audio_files

def add_audio_files(confirmation):
    if confirmation.lower() != 'confirm':
        return  # Stop if we did not confirm
    
    print("Working on that data...")

    audio_files = read_json()
    num_of_audio_files = len(audio_files)
    text_blocks = read_text_blocks('/Users/saavedj/SimpleSolutions/data/references.txt')

    # Parse all data and store it in parsed set
    for index, text_block in enumerate(text_blocks):
        index += num_of_audio_files # Offset by existing objects
        # Get audio file data
        parsed_data = parse_text_block(text_block)
        filename = f"{index}.mp3"  # Use string formatting for the filename
        filepath = os.path.join(MUSIC_PATH, filename)
        audio_info = get_audio_info([filepath])
        file_size = f"{audio_info[0] / (1024 * 1024):.2f} MB"
        duration = format_time(audio_info[1])

        # Build audio file
        audio_file = AudioFile(
            index=index,
            song_name=parsed_data["song_name"],
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


#Execute
add_audio_files(input('Are you sure? type \'confirm\' if so: '))
# for audio_file in read_json(): audio_file.print_info()
