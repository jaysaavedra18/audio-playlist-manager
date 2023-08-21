import tkinter as tk
from tkinter import messagebox

import os

from pytube import YouTube
from config import DOWNLOADS_DIRECTORY


def download_and_rename_mp3(url, output_path, new_filename):
    try:
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        file_path = os.path.join(output_path, audio_stream.default_filename)
        audio_stream.download(output_path=output_path)

        new_file_path = os.path.join(output_path, new_filename)
        os.rename(file_path, new_file_path)

        print("MP3 downloaded and renamed successfully!")
    except Exception as e:
        print("Error:", e)


def user_prompt_download_details():
    # Get the text from the text box
    input_text = text_box.get("1.0", "end-1c")
    if input_text.strip() == "":
        messagebox.showwarning("Empty Text Box", "Text box cannot be empty.")
        return # Text box cannot be empty
    
    for line in input_text.split('\n'):
        if line == "": continue
        # Parse out artist, title, and url
        parts = line.split('-', 2)
        artist = parts[0].lower().strip().replace(' ', '_')
        title = parts[1].lower().strip().replace(' ', '_')
        url = parts[2]

        # Create filepath 
        filename = f"{title.replace(' ', '_').lower()}_{artist.replace(' ', '_').lower()}.mp3"

        # Download mp3 to the filepath
        print(f"Downloading {filename}")
        download_and_rename_mp3(url, DOWNLOADS_DIRECTORY, filename)

    # Ask the user if they want to perform the function again
    answer = messagebox.askyesno(
        "Repeat?", "Do you want to download more mp3s?")
    if answer:
        text_box.delete("1.0", "end")  # Clear the text box
    else:
        app.destroy()  # Close the GUI


def clear_placeholder(event):
    if text_box.get("1.0", "end-1c") == "artist - title - url":
        text_box.delete("1.0", "end")
        text_box.unbind("<FocusIn>")


app = tk.Tk()
app.title("Download MP3")

# Set window size and position (widthxheight+xposition+yposition)
app.geometry("900x150+600+400")

label = tk.Label(app, text="Please enter your URL in the following format: 'artist - title - url:")
label.pack()

text_box = tk.Text(app, height=5, width=90)
text_box.pack(fill="both", padx=10, pady=10)
text_box.insert(1.0, "artist - title - url")
text_box.bind("<FocusIn>", clear_placeholder)

submit_button = tk.Button(app, text="Download MP3", command=user_prompt_download_details)
submit_button.pack()



app.mainloop()
