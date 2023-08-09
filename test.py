import os
import random
from pydub import AudioSegment
from tkinter import Tk, filedialog

# Constants for file paths
AUDIO_DIRECTORY = "/Users/saavedj/SimpleSolutions/music-licensed"
TEXT_FILE_PATH = "/Users/saavedj/SimpleSolutions/all_refererences.txt"
OUTPUT_REFERENCES_PATH = "/Users/saavedj/Downloads/output_references.txt"
CONCATENATED_AUDIO_PATH = "/Users/saavedj/Downloads/concatenated_audio.mp3"


def main():
    text_blocks = read_text_blocks(TEXT_FILE_PATH)

    choice = input(
        "Choose an option:\n1. Random playlist\n2. Selected playlist\n")

    if choice == '1':
        num_files_to_stitch = int(
            input("How many files would you like to stitch together?\n"))
        audio_files = get_audio_files(AUDIO_DIRECTORY)
        selected_files = select_random_files(audio_files, num_files_to_stitch)
    elif choice == '2':
        selected_files = select_audio_files_with_dialog()
    else:
        print("Invalid choice. Exiting.")
        return

    concatenated_audio = concatenate_audio(selected_files, AUDIO_DIRECTORY)
    output_references = generate_output_references(selected_files, text_blocks)

    save_output_references(output_references, OUTPUT_REFERENCES_PATH)
    export_concatenated_audio(concatenated_audio, CONCATENATED_AUDIO_PATH)



def read_text_blocks(file_path):
    with open(file_path, "r") as file:
        return file.read().split("\n\n")


def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3") or f.endswith(".wav")]


def select_audio_files_with_dialog():
    root = Tk()
    root.withdraw()  # Hide the main window
    selected_files = filedialog.askopenfilenames(
        initialdir=AUDIO_DIRECTORY, title="Select Audio Files", filetypes=(("Audio Files", "*.mp3 *.wav"),)
    )
    # Extract only file names
    return [os.path.basename(file) for file in selected_files]



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
    output_references = []
    total_duration = 0

    for file in selected_files:
        duration_seconds = len(AudioSegment.from_file(
            os.path.join(AUDIO_DIRECTORY, file))) / 1000

        try:
            index = int(os.path.splitext(file)[0])
            if 0 <= index < len(text_blocks):
                position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
                output_references.append(f"{position} {text_blocks[index]}")
                total_duration += duration_seconds
        except ValueError:
            print(f"Skipped: {file} (Not in number format)")
            position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
            filename_without_extension = os.path.splitext(file)[0]
            output_references.append(
                f"{position} {filename_without_extension} from HookSounds.com")
            total_duration += duration_seconds

    return output_references


def save_output_references(output_references, file_path):
    with open(file_path, "w") as output_file:
        for reference in output_references:
            output_file.write(reference + "\n\n")


def export_concatenated_audio(concatenated_audio, file_path):
    concatenated_audio.export(file_path, format="mp3")

if __name__ == "__main__":
    main()
