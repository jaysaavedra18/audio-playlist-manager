import shutil
import os

source_path = "/Users/saavedj/SimpleSolutions/music-licensed"
backup_path = "/Users/saavedj/Backups/Lofi Audio Files"

# Create the backup directory if it doesn't exist
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

for root, dirs, files in os.walk(source_path):
    for file in files:
        source_file_path = os.path.join(root, file)
        backup_file_path = os.path.join(backup_path, file)

        # Copy the file from the source to the backup directory
        shutil.copy2(source_file_path, backup_file_path)

        print(f"File '{file}' backed up to '{backup_file_path}'")
