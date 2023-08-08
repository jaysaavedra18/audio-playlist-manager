import cv2
import os
import tkinter as tk
from tkinter import filedialog

SQUARE, VERTICAL, HORIZONTAL = [512, 512], [448, 704], [704, 448]

def get_folder():
    """
    Opens a folder dialog to allow the user to select a folder and returns the path of the selected folder.

    Returns:
        str or None: The path of the selected folder if a folder was chosen, otherwise None.
    """
    # Create the root window for the folder dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open the folder dialog and get the selected folder's path
    folder_path = filedialog.askdirectory()

    # Check if the user selected a folder or canceled the dialog
    if folder_path:
        print("Selected Folder:", folder_path)
    else:
        print("No folder selected.")
        return None
    return folder_path

def get_dimensions():
    while True:
        user_input = input("Are your frames (V)ertical, (H)orizontal, or (S)quare: ").upper()

        if user_input == 'V':
            return VERTICAL
        elif user_input == 'H':
            return HORIZONTAL
        elif user_input == 'S':
            return SQUARE
        else:
            print("Invalid input. Please enter 'V', 'H', or 'S'. Try again.")

def get_fps():
    while True:
        try:
            fps = int(input("Please enter the FPS (15-60): "))
            if 15 <= fps <= 60:
                return fps
            else:
                print("Invalid input. FPS must be between 15 and 60. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer between 15 and 60.")


def get_output_file():
    while True:
        output_filename = input(
            "Please enter the output file name (without extension): ")
        if output_filename.strip():
            return output_filename.strip() + '.mp4'
        else:
            print("Invalid input. The file name cannot be empty. Try again.")

def create_video():
    dimensions = get_dimensions()
    print(dimensions)
    fps = get_fps()
    output_file = get_output_file()
    folder_path = get_folder()
    file_names = [file for file in os.listdir(
        folder_path) if file.endswith('.png')]
    file_names.sort()

    # Set your desired frame width and height
    frame_width, frame_height = dimensions

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(
        output_file, fourcc, fps, (frame_width, frame_height))

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        img = cv2.imread(file_path)
        video_writer.write(img)

    video_writer.release()
    print("Video created successfully.")

if __name__ == '__main__':
    create_video()