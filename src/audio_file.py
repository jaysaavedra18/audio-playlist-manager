import os
import json
from pydub import AudioSegment
from typing import List

from text_file import read_text_blocks, get_unique_file_name, parse_text_block, delete_first_block

TEXT_FILE_PATH = "/Users/saavedj/SimpleSolutions/data/references.txt"
MUSIC_PATH = '/Users/saavedj/SimpleSolutions/music'
DATA_DIRECTORY = '/Users/saavedj/SimpleSolutions/data'

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


def write_json(objects):
    # Serialize to JSON and write to file
    with open(os.path.join(DATA_DIRECTORY, "music_data.json"), "w") as json_file:
        json.dump([vars(file) for file in objects], json_file, indent=4)

def read_json():
    # Read JSON data back into AudioFile objects
    with open("music_data.json", "r") as json_file:
        loaded_data = json.load(json_file)

    # Convert JSON data back to AudioFile objects
    loaded_audio_files = [AudioFile(**data) for data in loaded_data]
    return loaded_audio_files

def add_audio_files(confirmation):
    if confirmation.lower() != 'confirm':
        return  # Stop if we did not confirm

    audio_files = []
    text_blocks = read_text_blocks('/Users/saavedj/SimpleSolutions/data/references.txt')

    # text_blocks = ["""Crescent Moon by Purrple Cat | https://purrplecat.com/
    # Music promoted by https://www.chosic.com/free-music/all/
    # Creative Commons CC BY-SA 3.0
    # https://creativecommons.org/licenses/by-sa/3.0/"""]
    
    # Parse all data and store it in parsed set
    for index, text_block in enumerate(text_blocks): 
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
        # delete_first_block(TEXT_FILE_PATH)

    write_json(objects=audio_files)


#Execute
add_audio_files(input('Are you sure? type \'confirm\' if so: '))
