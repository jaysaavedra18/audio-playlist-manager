import os
from tkinter import Tk, filedialog

# import random
# from pydub import AudioSegment

# Import functions from the get_songs module and rename the function
from file_utils import read_text_blocks, get_audio_files, get_audio_info, concatenate_audio, export_audio, select_random_files
from utils import seconds_to_formatted_time
from config import TEXT_FILE_PATH, AUDIO_DIRECTORY, ARCHIVES_DIRECTORY, OUTPUT_PLAYLIST_PATH, OUTPUT_PROMOTIONS_PATH

# # Define paths/dirs
# ARCHIVES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, f"{DATE_STRING}")
# OUTPUT_PROMOTIONS_PATH = os.path.join(ASSETS_DIRECTORY, f"output-references-{DATE_STRING}.txt")
# OUTPUT_PLAYLIST_PATH = os.path.join(ASSETS_DIRECTORY, f"playlist-{DATE_STRING}.mp3")


# # Promotions, Licenses, Attributions (MOVED - playlist.py)
# PROMOTIONS = """
# Music promoted by https://www.chosic.com/free-music/all/

# https://creativecommons.org/licenses/by-sa/3.0/
# https://creativecommons.org/licenses/by/4.0/

# - Creative Commons CC BY-SA 3.0
# - Creative Commons Attribution 3.0 Unported License
# - Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
# - Creative Commons — Attribution-NoDerivs 3.0 Unported — CC BY-ND 3.0
# - Creative Commons CC BY 4.0
# - Attribution 4.0 International (CC BY 4.0)
# """


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
    # output_references = generate_output_references(selected_files, text_blocks)

    # # Save the output references to the specified path
    # save_output_references(output_references, OUTPUT_PROMOTIONS_PATH)

    # Export the concatenated audio to the specified path
    export_audio(concatenated_audio, OUTPUT_PLAYLIST_PATH)

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

        # Calculate selected file(s) data
        total_size, total_length = get_audio_info(selected_files)

        while True:
            last_file = selected_files[-1]  # Get the last file

            # Display selected file(s) data
            print(f"Number of files: {len(selected_files)}")
            print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
            print(f"Total length: {seconds_to_formatted_time(total_length)}")

            # Prompt user for choice
            choice = input(
                "Are you satisfied with the length of the audio? (y/n/r): ").lower()
            if choice == 'y':
                root.destroy()  # Close the file dialog window
                print("We are putting together your playlist.\nOne moment please.")
                return [os.path.basename(file) for file in selected_files]
            elif choice == 'n':
                tsize, tlength = get_audio_info([last_file]) # Get removed file data
                total_size -= tsize
                total_length -= tlength
                selected_files = selected_files[:-1] # Remove the last file
                print(f"Removed file: {os.path.basename(last_file)}")
                continue
            elif choice == 'r':
                break  # Exit the input loop and re-enter the file explorer.
            else:
                print("Invalid choice. Please enter 'y' or 'n' or 'r' for reselect.")


# def generate_output_references(selected_files, text_blocks):
#     """
#     DEPRECATED!!!
#     """
#     output_references = []
#     output_references.append(PROMOTIONS)

#     total_duration = 0 # Initialize total duration

#     for file in selected_files:
#         # Calculate duration in seconds for the current audio file
#         duration_seconds = len(AudioSegment.from_file(
#             os.path.join(AUDIO_DIRECTORY, file))) / 1000

#         try:
#             # Get the index from the filename
#             index = int(os.path.splitext(file)[0]) # Index is the filename

#             # Check if the index is within the range of text_blocks
#             if 0 <= index < len(text_blocks):
#                 # Format the position in minutes:seconds
#                 position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
#                 # Get the first line of the corresponding text block i.e. the title
#                 first_line = text_blocks[index].split('\n')[0]
#                 # Add the position and first line to the output references
#                 output_references.append(f"{position} {first_line}")
#                 total_duration += duration_seconds
#         except ValueError:
#             # Skip files with non-numeric filenames
#             print(f"Skipped: {file} (Not in number format)")

#     return output_references


# def save_output_references(output_references, file_path):
#     """
#     DEPRECATED!!!
#     """
#     make_archive_directory() # Create the daily archive if does not exist
#     with open(get_unique_file_name(file_path), "w") as output_file:
#         for reference in output_references:
#             output_file.write(reference + "\n\n")


# def make_archive_directory():
    """
    DEPRECATED!!!
    """
    if not os.path.exists(ARCHIVES_DIRECTORY):
        os.mkdir(ARCHIVES_DIRECTORY)



if __name__ == "__main__":
    main()
