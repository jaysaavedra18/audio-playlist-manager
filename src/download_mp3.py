import tkinter as tk
from tkinter import messagebox

import os

from pytube import YouTube
from config import DOWNLOADS_DIRECTORY

def download_mp3(url, output_path):
    try:
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_stream.download(output_path)
        print("MP3 downloaded successfully!")
    except Exception as e:
        print("Error:", e)


def perform_function():
    # Get the text from the text box
    input_text = text_box.get("1.0", "end-1c")
    
    # Parse out artist, title, and url
    parts = input_text.split('-', 2)
    artist = parts[0].lower().strip().replace(' ', '_')
    title = parts[1].lower().strip().replace(' ', '_')
    url = parts[2]

    # Create filepath 
    filename = f"{title.replace(' ', '_').lower()}_{artist.replace(' ', '_').lower()}.mp3"
    filepath = os.path.join(DOWNLOADS_DIRECTORY, filename)

    # Download mp3 to the filepath
    print(artist)
    print(title)
    print(url)
    print(filepath)
    download_mp3(url, filepath)

    # Ask the user if they want to perform the function again
    answer = messagebox.askyesno(
        "Repeat?", "Do you want to perform the function again?")
    if answer:
        text_box.delete("1.0", "end")  # Clear the text box
    else:
        app.destroy()  # Close the GUI


app = tk.Tk()
app.title("Download MP3")

# Set window size and position (widthxheight+xposition+yposition)
app.geometry("900x150+600+400")

label = tk.Label(app, text="Please enter your URL in the following format: 'artist - title - url:")
label.pack()

text_box = tk.Text(app, height=5, width=90)
text_box.pack(fill="both", padx=10, pady=10)

submit_button = tk.Button(app, text="Download MP3", command=perform_function)
submit_button.pack()

app.mainloop()
