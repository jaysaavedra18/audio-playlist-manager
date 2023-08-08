import os
import random
from pydub import AudioSegment

# Path to the directory containing audio files
audio_directory = "/Users/saavedj/Downloads/music-licensed"

# Read the input text file and split it into blocks
with open("/Users/saavedj/midi-generation/all_refererences.txt", "r") as file:
    text_blocks = file.read().split("\n\n")

num_files_to_stitch = int(
    input("How many files would you like to stitch together? "))

audio_files = [f for f in os.listdir(
    audio_directory) if f.endswith(".mp3") or f.endswith(".wav")]

# Select random audio files
selected_files = random.sample(audio_files, num_files_to_stitch)

concatenated_audio = AudioSegment.silent(duration=0)
output_references = []  # Store associated text blocks

total_duration = 0  # Keep track of the total duration

for file in selected_files:
    audio_path = os.path.join(audio_directory, file)
    audio_segment = AudioSegment.from_file(audio_path)
    concatenated_audio += audio_segment
    duration_seconds = len(audio_segment) / 1000  # Convert to seconds

    try:
        # Get the index from the filename (assuming filenames are numbers)
        index = int(os.path.splitext(file)[0])
        if 0 <= index < len(text_blocks):
            # Format position as mm:ss
            position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
            output_references.append(f"{position} {text_blocks[index]}")
            total_duration += duration_seconds
    except ValueError:
        print(f"Skipped: {file} (Not in number format)")
        # Format position as mm:ss
        position = f"{int(total_duration // 60):02}:{int(total_duration % 60):02}"
        filename_without_extension = os.path.splitext(file)[0]
        output_references.append(
            f"{position} {filename_without_extension} from HookSounds.com")
        total_duration += duration_seconds

    
# Save the output_references to a file
with open("/Users/saavedj/Downloads/output_references.txt", "w") as output_file:
    for reference in output_references:
        output_file.write(reference + "\n\n")

output_file_path = "/Users/saavedj/Downloads/concatenated_audio.mp3"
concatenated_audio.export(output_file_path, format="mp3")
