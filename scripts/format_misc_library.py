import os
from dotenv import load_dotenv

# Directory containing your files
load_dotenv()
directory = os.path.join(os.getenv("AUDIO_DIRECTORY"), "misc")

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".mp3") and "spotifydown" in filename:
        # Extract the song name
        song_name = filename.split(" - ", 1)[-1].replace(".mp3", "").strip()
        
        # Create the new filename
        new_filename = f"{song_name}.mp3"
        
        # # Rename the file
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        
        print(f"Renamed: {filename} -> {new_filename}")
