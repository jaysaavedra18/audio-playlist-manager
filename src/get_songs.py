TEXT_FILE_PATH = "/Users/saavedj/SimpleSolutions/data/references.txt"

def read_text_blocks(file_path):
    with open(file_path, "r") as file:
        return file.read().split("\n\n")


def write_first_lines_to_file(text_blocks, output_file):
    with open(output_file, "w") as file:
        for text_block in text_blocks:
            lines = text_block.split("\n")
            first_line = lines[0].strip()
            if first_line:
                file.write(first_line + "\n")

if __name__ == "__main__":
    text_blocks = read_text_blocks(TEXT_FILE_PATH)

    output_file = "/Users/saavedj/SimpleSolutions/data/songs.txt"
    write_first_lines_to_file(text_blocks, output_file)
    print(f"Songs written to {output_file}")
