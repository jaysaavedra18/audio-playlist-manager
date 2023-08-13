import os

TEXT_FILE_PATH = "/Users/saavedj/SimpleSolutions/data/references.txt"
SONGS_PATH = '/Users/saavedj/SimpleSolutions/data/songs.txt'

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
        write_first_lines_to_file(text_blocks, SONGS_PATH)
        return text_blocks


def delete_first_block(file_path):
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
    with open(output_file, "w") as file:
        for text_block in text_blocks:
            lines = text_block.split("\n")
            first_line = lines[0].strip()
            if first_line:
                file.write(first_line + "\n")

                import os


def get_unique_file_name(file_path):
    """
    Get a unique file name by appending "(1)", "(2)", and so on to the original file name.

    Args:
        file_path (str): Original file path.

    Returns:
        str: A unique file path.
    """
    base_name, extension = os.path.splitext(file_path)
    unique_path = file_path
    counter = 1

    while os.path.exists(unique_path):
        unique_path = f"{base_name} ({counter}){extension}"
        counter += 1

    return unique_path


def parse_text_block(text):
    lines = text.strip().split('\n')

    # Extract song name and artist name
    song_info = lines[0].split(' by ')
    song_name = song_info[0].strip()
    artist_info = song_info[1].split(' | ')
    artist_name = artist_info[0].strip()
    artist_link = artist_info[1].strip()


    # Extract licenses as a list
    licenses = []
    for line in lines[1:4]:  # Extract the 2nd to 4th lines (if they exist)
        licenses.append(line.strip())

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "artist_link": artist_link,
        "licenses": licenses
    }


if __name__ == "__main__":
    text_blocks = read_text_blocks(TEXT_FILE_PATH)

    output_file = "/Users/saavedj/SimpleSolutions/data/songs.txt"
    write_first_lines_to_file(text_blocks, output_file)
    print(f"Songs written to {output_file}")
