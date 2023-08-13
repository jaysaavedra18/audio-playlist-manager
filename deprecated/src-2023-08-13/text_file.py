import os

# THIS FILE HAS BEEN COMPLETELY DEPRECATED

def read_text_blocks(file_path):
    """
    EXPORTED!!!
    """
    with open(file_path, "r") as file:
        text_blocks = file.read().split("\n\n")
        return text_blocks


def delete_first_block(file_path):
    """
    DEPRECATED!!!
    """
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the position of the first '\n\n' delimiter
    first_delimiter_pos = content.find('\n\n')

    # If the delimiter is found, remove the first block
    if first_delimiter_pos != -1:
        # Skip the first delimiter
        updated_content = content[first_delimiter_pos + 2:]
    else:
        updated_content = content

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)

def write_first_lines_to_file(text_blocks, output_file):
    """
    EXPORTED!!!
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
    EXPORTED!!!
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
