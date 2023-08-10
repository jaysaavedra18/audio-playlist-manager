import os
from tkinter import Tk, filedialog
from pydub import AudioSegment

AUDIO_DIRECTORY = "/Users/saavedj/Downloads/music-licensed"


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
        selected_files = filedialog.askopenfilenames(
            initialdir=AUDIO_DIRECTORY, title="Select Audio Files", filetypes=(("Audio Files", "*.mp3 *.wav"),)
        )

        total_size, total_length = get_audio_info(selected_files)
        print(f"Number of files: {len(selected_files)}")
        print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
        print(f"Total length: {format_time(total_length)}")

        while True:
            choice = input(
                "Are you satisfied with the length of the audio? (y/n): ").lower()
            if choice == 'y':
                root.destroy()  # Close the file dialog window
                return [os.path.basename(file) for file in selected_files]
            elif choice == 'n':
                break  # Exit the input loop and re-enter the file explorer.
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    selected_audio_files = select_audio_files_with_dialog()
    print("Selected audio files:")
    for file in selected_audio_files:
        print(file)
