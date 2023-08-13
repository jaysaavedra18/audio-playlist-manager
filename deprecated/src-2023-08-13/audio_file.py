import os
import json
from pydub import AudioSegment

from file_utils import read_text_blocks, get_unique_file_name, parse_text_block_into_song
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


def get_audio_files(directory):
    """
    EXPORTED!!!
    """
    return [f for f in os.listdir(directory) if f.endswith(".mp3") or f.endswith(".wav")]


def get_audio_info(audio_files):
    """
    EXPORTED!!!
    """
    # If a single file path is provided as a string, convert it to a list
    if isinstance(audio_files, str):
        audio_files = [audio_files]

    # Sum size and length of audio_files
    total_size = sum(os.path.getsize(file) for file in audio_files)
    total_length = sum(AudioSegment.from_file(
        file).duration_seconds for file in audio_files)
    return total_size, total_length


def concatenate_audio(selected_files, audio_directory):
    """
    EXPORTED!!!
    """
    # Initialize an empty AudioSegment object to hold the concatenated audio
    concatenated_audio = AudioSegment.silent(duration=0)

    for file in selected_files:
        audio_path = os.path.join(audio_directory, file)
        audio_segment = AudioSegment.from_file(audio_path)
        concatenated_audio += audio_segment

    return concatenated_audio


def export_audio(audio, file_path):
    """
    EXPORTED!!!
    """
    audio.export(get_unique_file_name(file_path), format="mp3")


def format_time(seconds):
    """
    EXPORTED!!!
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def write_json(objects, file_path):
    """
    EXPORTED!!!
    """
    # Serialize to JSON
    json_data = [vars(file) for file in objects]

    # Write JSON data to the file
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json(file_path, target_class):
    """
    EXPORTED!!!
    """
    try:
        # Read JSON data from the file
        with open(file_path, "r") as json_file:
            loaded_data = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle empty JSON file or invalid JSON data
        return []

    # Convert JSON data back to objects of the specified target_class
    loaded_objects = [target_class(**data) for data in loaded_data]
    return loaded_objects

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


def rename_files_in_directory(directory_path):
    """
    DEPRECATED!!!
    """
    # Ensure the directory path is valid
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return

    # Get a list of files in the directory
    files = [file for file in os.listdir(directory_path) if os.path.isfile(
        os.path.join(directory_path, file))]
    audio_files = read_json(MUSIC_DATA_PATH, AudioFile)
    new_names = [audio_file.song_name for audio_file in audio_files]

    # Iterate over the files in the directory
    for file in files:
        # Extract the index from the filename
        file_name, file_extension = os.path.splitext(file)
        try:
            index = int(file_name)
        except ValueError:
            # Skip files that don't have a numeric index
            continue

        # Check if the index is within the range of new_names
        if 0 <= index < len(new_names):
            new_name = new_names[index]
            new_file_name = f"{new_name}{file_extension}"
            old_file_path = os.path.join(directory_path, file)
            new_file_path = os.path.join(directory_path, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{file}' to '{new_file_name}'")



#Execute
# add_audio_files(input('Are you sure? type \'confirm\' if so: '))
