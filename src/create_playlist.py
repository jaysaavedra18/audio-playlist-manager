import os
import random
import datetime
from pydub import AudioSegment
from tkinter import Tk, filedialog

# Import functions from the get_songs module and rename the function
from get_songs import write_first_lines_to_file as update_songs, get_unique_file_name

# Get today's date
today_date = datetime.date.today()
date_string = today_date.strftime("%Y-%m-%d")

# Define file paths
HOME_DIRECTORY = "/Users/saavedj"
BASE_DIRECTORY = os.path.join(HOME_DIRECTORY, "SimpleSolutions")
AUDIO_DIRECTORY = os.path.join(BASE_DIRECTORY, "music")
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")

# Specific file paths
TEXT_FILE_PATH = os.path.join(DATA_DIRECTORY, "references.txt")
SONGS_PATH = os.path.join(DATA_DIRECTORY, "songs.txt")
output_references_path = os.path.join(HOME_DIRECTORY, "Downloads", "current-video", f"output-references-{date_string}.txt")
concatenated_audio_path = os.path.join(HOME_DIRECTORY, "Downloads", "current-video", f"concatenated-audio-{date_string}.mp3")


# Promotions, Licenses, Attributions
PROMOTIONS = """
Music promoted by https://www.chosic.com/free-music/all/

https://creativecommons.org/licenses/by-sa/3.0/
Creative Commons CC BY-SA 3.0
Creative Commons Attribution 3.0 Unported License
Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
Creative Commons — Attribution-NoDerivs 3.0 Unported — CC BY-ND 3.0

https://creativecommons.org/licenses/by/4.0/
Creative Commons CC BY 4.0
Attribution 4.0 International (CC BY 4.0)
"""


def main():
    text_blocks = read_text_blocks(TEXT_FILE_PATH)

    # Prompt user for their choice
    print("Choose an option:")
    print("1. Random playlist")
    print("2. Selected playlist")
    choice = input("Enter the number of your choice: ")

    # Query user's choice
    if choice == '1': 
        # Random file selection with number input
        num_files_to_stitch = int(
            input("How many files would you like to stitch together?\n"))
        audio_files = get_audio_files(AUDIO_DIRECTORY)
        selected_files = select_random_files(audio_files, num_files_to_stitch)
    elif choice == '2': 
        # Manual selection with file explorer
        selected_files = select_audio_files_with_dialog()
    else:
        print("Invalid choice. Exiting.")
        return

    # Concatenate the selected audio files
    concatenated_audio = concatenate_audio(selected_files, AUDIO_DIRECTORY)

    # Generate output references based on selected files and text blocks
    output_references = generate_output_references(selected_files, text_blocks)

    # Save the output references to the specified path
    save_output_references(output_references, output_references_path)

    # Export the concatenated audio to the specified path
    export_concatenated_audio(concatenated_audio, concatenated_audio_path)


def read_text_blocks(file_path):
    """
    Read text blocks from a file and split them based on double line breaks.
    Writes the name & artist of all songs to data/songs.txt.

    Args:
        file_path (str): The path to the file containing text blocks.

    Returns:
        list: A list of text blocks, where each block is a string representing
              a segment of text separated by double line breaks.

    Note:
        This function assumes that the file contains text blocks separated by
        two consecutive newline characters. If the file does not
        follow this format, the function behavior may not be as expected.

    """
    with open(file_path, "r") as file:
        text_blocks = file.read().split("\n\n")
        update_songs(text_blocks, SONGS_PATH)
        return text_blocks

def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3") or f.endswith(".wav")]


def get_audio_info(audio_files):
    total_size = sum(os.path.getsize(file) for file in audio_files)
    total_length = sum(AudioSegment.from_file(
        file).duration_seconds for file in audio_files)
    return total_size, total_length


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def select_audio_files_with_dialog():
    while True:
        root = Tk()
        root.withdraw()  # Hide the main window

        # Display a file dialog to select audio files
        selected_files = filedialog.askopenfilenames(
            initialdir=AUDIO_DIRECTORY,
            title="Select Audio Files",
            filetypes=(("Audio Files", "*.mp3 *.wav"),)
        )

        while True:
            # Display selected file(s) data
            total_size, total_length = get_audio_info(selected_files)
            print(f"Number of files: {len(selected_files)}")
            print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
            print(f"Total length: {format_time(total_length)}")

            # Prompt user for choice
            choice = input(
                "Are you satisfied with the length of the audio? (y/n/r): ").lower()
            if choice == 'y':
                root.destroy()  # Close the file dialog window
                return [os.path.basename(file) for file in selected_files]
            elif choice == 'n':
                removed_file = selected_files[-1]  # Get the last file
                selected_files = selected_files[:-1] # Remove the last file
                print(f"Removed file: {os.path.basename(removed_file)}")
                continue
            elif choice == 'r':
                break  # Exit the input loop and re-enter the file explorer.
            else:
                print("Invalid choice. Please enter 'y' or 'n' or 'r' for reselect.")


def select_random_files(audio_files, num_files):
    return random.sample(audio_files, num_files)


def concatenate_audio(selected_files, audio_directory):
    concatenated_audio = AudioSegment.silent(duration=0)

    for file in selected_files:
        audio_path = os.path.join(audio_directory, file)
        audio_segment = AudioSegment.from_file(audio_path)
        concatenated_audio += audio_segment

    return concatenated_audio


def generate_output_references(selected_files, text_blocks):
    """
    Generate a list of output references based on selected audio files and text blocks.

    Args:
        selected_files (list): List of audio file names.
        text_blocks (list): List of text blocks corresponding to each audio file.

    Returns:
        list: List of output references.
    """
    output_references = []
    output_references.append(PROMOTIONS.strip())

    total_duration = 0 # Initialize total duration

    for file in selected_files:
        # Calculate duration in seconds for the current audio file
        duration_seconds = len(AudioSegment.from_file(
            os.path.join(AUDIO_DIRECTORY, file))) / 1000

        try:
            # Get the index from the filename
            index = int(os.path.splitext(file)[0]) # Index is the filename

            # Check if the index is within the range of text_blocks
            if 0 <= index < len(text_blocks):
                # Format the position in minutes:seconds
                position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
                # Get the first line of the corresponding text block i.e. the title
                first_line = text_blocks[index].split('\n')[0]
                # Add the position and first line to the output references
                output_references.append(f"{position} {first_line}")
                total_duration += duration_seconds
        except ValueError:
            # Skip files with non-numeric filenames
            print(f"Skipped: {file} (Not in number format)")

    return output_references


def save_output_references(output_references, file_path):
    with open(get_unique_file_name(file_path), "w") as output_file:
        for reference in output_references:
            output_file.write(reference + "\n\n")


def export_concatenated_audio(concatenated_audio, file_path):
    concatenated_audio.export(get_unique_file_name(file_path), format="mp3")


if __name__ == "__main__":
    main()
