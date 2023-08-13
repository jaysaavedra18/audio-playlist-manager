# audio_io.py

import os
import json
from pydub import AudioSegment

# Audio input/output functions

def get_audio_files(directory):
    """
    Retrieve a list of audio file names (MP3 and WAV) from the specified directory.

    Parameters:
    directory (str): The path to the directory containing the audio files.

    Returns:
    list: A list of strings representing the names of audio files (MP3 and WAV)
          found in the specified directory. Only file names with the extensions
          '.mp3' or '.wav' are included in the list.
    """
    return [f for f in os.listdir(directory) if f.endswith(".mp3") or f.endswith(".wav")]


def get_audio_info(audio_files):
    """
    Calculate the total size and length of audio files provided as either a single file path string
    or a list of file path strings.

    Parameters:
    audio_files (Union[str, List[str]]): A file path string or a list of file path strings.
        If a single file path is provided as a string, it will be treated as a list containing
        that single file path.

    Returns:
    tuple: A tuple containing the total size (in bytes) and the total length (in seconds) of the
           audio files. The size represents the sum of the file sizes, and the length represents
           the sum of the audio durations for all the files.
    """
    # If a single file path is provided as a string, convert it to a list
    if isinstance(audio_files, str):
        audio_files = [audio_files]

    # Sum size and length of audio_files
    total_size = sum(os.path.getsize(file) for file in audio_files)
    total_length = sum(AudioSegment.from_file(file).duration_seconds for file in audio_files)
    return total_size, total_length


def concatenate_audio(selected_files, audio_directory):
    """
    Concatenate multiple audio files specified in the 'selected_files' list.
    
    Parameters:
    selected_files (list): A list of audio file names (strings) to be concatenated.
    audio_directory (str): The directory where the audio files are located.

    Returns:
    AudioSegment: An AudioSegment object containing the concatenated audio from the specified files.

    Notes:
    - The 'selected_files' list should contain the names of the audio files (e.g., ["file1.mp3", "file2.wav"]).
    - The concatenation order follows the order in the 'selected_files' list.
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
    Export an AudioSegment object to an MP3 audio file at the specified file path.
    
    Parameters:
    audio (AudioSegment): An AudioSegment object to be exported as an MP3 file.
    file_path (str): The desired file path (including the file name) for the exported MP3 file.
    
    Notes:
    - The exported audio file will be in MP3 format.
    - The function uses the 'get_unique_file_name' function to ensure that the exported file has a
      unique name in the specified file path, to prevent overwriting existing files.
    """
    audio.export(get_unique_file_name(file_path), format="mp3")



# text_io.py

# Text input/output functions

def read_text_blocks(file_path):
    """
    Read text blocks from a file and split them based on double line breaks.

    Args:
        file_path (str): The path to the file containing text blocks.

    Returns:
        list: A list of text blocks.

    Note:
        This function assumes that the file contains text blocks separated by
        two consecutive newline characters. If the file does not
        follow this format, the function behavior may not be as expected.

    """
    with open(file_path, "r") as file:
        text_blocks = file.read().split("\n\n")
        return text_blocks
    

def write_first_lines_to_file(text_blocks, output_file):
    """
    Write the first line of each text block in the input list to a specified output file.

    Parameters:
    text_blocks (list): A list of text blocks, where each block is a string with one or more lines.
    output_file (str): The path to the output file where the first lines will be written.

    Notes:xs
    - The output file is overwritten if it already exists; if it doesn't exist, it will be created.
    """
    with open(output_file, "w") as file:
        for text_block in text_blocks:
            lines = text_block.split("\n")
            first_line = lines[0].strip()
            if first_line:
                file.write(first_line + "\n")


def get_unique_file_name(file_path):
    """
    Generate a unique file name by adding a counter suffix to the base file name if the file already exists.

    Parameters:
    file_path (str): The original file path for which a unique name is needed.

    Returns:
    str: A unique file path based on the input 'file_path', ensuring that the file does not already exist
    in the specified location.
    """
    base_name, extension = os.path.splitext(file_path)
    unique_path = file_path
    counter = 1

    while os.path.exists(unique_path):
        unique_path = f"{base_name} ({counter}){extension}"
        counter += 1

    return unique_path


def parse_text_block_into_song(text):
    """
    Parse a text block containing song information and extract relevant details.

    Parameters:
    text (str): A text block containing multiple lines of song information.

    Returns:
    dict: A dictionary containing the extracted song details, including song name, artist name,
    artist link, and licenses.

    Notes:
    - The input 'text' parameter is expected to be a string with multiple lines, where the first line is
      in the format "Song Name by Artist | Artist Link".
    - The resulting dictionary includes the extracted details under the keys: "song_name", "artist_name",
      "artist_link", and "licenses".
    """
    lines = text.strip().split('\n')

    # Extract song name, artist name, and artist link from the first line
    song_info = lines[0].split(' by ')
    song_name = song_info[0].strip()
    artist_info = song_info[1].split(' | ')
    artist_name, artist_link = artist_info[0].strip(), artist_info[1].strip()

    # Extract licenses from lines 2 to 4 (if they exist) as a list
    licenses = [line.strip() for line in lines[1:4]]

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "artist_link": artist_link,
        "licenses": licenses
    }


# json_io.py

# JSON/object input/output functions

def write_json(objects, file_path):
    """
    Serialize a list of objects and write the JSON representation to a file.

    Parameters:
    objects (list): A list of objects to be serialized to JSON.
    file_path (str): The file_path (including the file name) where the JSON data will be written.
    """
    # Serialize to JSON
    json_data = [vars(file) for file in objects]

    # Write JSON data to the file
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json(file_path, target_class):
    """
    Read JSON data from a file and convert it into a list of objects of the specified class.

    Parameters:
    file_path (str): The path to the JSON file to be read.
    target_class (class): The class to which the JSON data should be converted.

    Returns:
    list: A list of objects of the specified class, created from the JSON data in the file.
    If the JSON file is empty or invalid, an empty list is returned.
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

