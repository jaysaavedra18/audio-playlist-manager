import tkinter as tk
from tkinter import filedialog, simpledialog, Menu

from config import DATE_STRING
from playlist import Playlist

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        label = tk.Label(root, text="Main Menu")
        label.pack()

        PlaylistCreator_button = tk.Button(
            root, text="Playlist Creator", command=self.show_PlaylistCreator)
        PlaylistCreator_button.pack()

        option2_button = tk.Button(
            root, text="MP3 Downloader", command=self.show_option2)
        option2_button.pack()

        option3_button = tk.Button(
            root, text="Song Library", command=self.show_option3)
        option3_button.pack()

    def show_PlaylistCreator(self):
        self.root.destroy()  # Close the main menu window
        PlaylistCreator_window = tk.Tk()
        PlaylistCreatorOption(PlaylistCreator_window)

    def show_option2(self):
        self.root.destroy()  # Close the main menu window
        option2_window = tk.Tk()
        Option2Screen(option2_window)

    def show_option3(self):
        self.root.destroy()  # Close the main menu window
        option3_window = tk.Tk()
        Option2Screen(option3_window)


class PlaylistCreatorOption:
    def __init__(self, root):
        self.root = root
        self.root.title("Playlist Creator")

        label = tk.Label(root, text="Create a Playlist")
        label.pack()

        select_button = tk.Button(
            root, text="Browse Files", command=self.browse_files)
        select_button.pack()
  
        create_by_button = tk.Button(
            root, text="Create By...", command=self.open_create_by_window)
        create_by_button.pack()

        back_button = tk.Button(
            root, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack()


    def show_main_menu(self):
        self.root.destroy()  # Close the current screen
        main_menu_window = tk.Tk()
        MainMenu(main_menu_window)

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select MP3 Files", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if files:
            print("Selected MP3 Files:")
            for path in files:
                print(path)

    def create_random_playlist(self):
        pass

    def create_genre_playlist(self):
        # Prompt user for genre
        genre = simpledialog.askstring(
            "Enter Genre", "Enter the genre you're looking for:")
        if not genre:
            pass
        # Prompt user for playlist name
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass
        # Prompt user to enter max playlist duration
        max_duration = self.enter_duration()

        # Create playlist object
        playlist = Playlist(title=title)
        playlist.create_playlist_by_genre(genre=genre, max_duration=max_duration)
        playlist.date_created = DATE_STRING

    def create_mood_playlist(self):
        # Prompt user for mood
        mood = simpledialog.askstring(
            "Enter Mood", "Enter the mood you're looking for:")
        if not mood:
            pass
        # Prompt user for playlist name
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass
        # Prompt user to enter max playlist duration
        max_duration = self.get_time_input()

        if max_duration is not None:
            # Create playlist object
            playlist = Playlist(title=title)
            playlist.create_playlist_by_mood(mood=mood, max_duration=max_duration)
            playlist.date_created = DATE_STRING
            playlist.export_playlist()

        

    def get_time_input(self):
        while True:
            time_str = simpledialog.askstring(
                "Enter Max Duration", "Enter max duration (hh:mm:ss):")
            try:
                hours, minutes, seconds = map(int, time_str.split(':'))
                if hours >= 0 and minutes >= 0 and seconds >= 0:
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    return total_seconds
                else:
                    print(
                        "Invalid time input. Please enter positive values for hours, minutes, and seconds.")
            except ValueError:
                print("Invalid time format. Please use the format hh:mm:ss.")

    def open_create_by_window(self):
        create_by_window = tk.Toplevel(self.root)
        create_by_window.title("Create By...")

        genre_button = tk.Button(create_by_window, text="Create By Genre", command=self.create_genre_playlist)
        genre_button.pack()

        mood_button = tk.Button(create_by_window, text="Create By Mood", command=self.create_mood_playlist)
        mood_button.pack()

        random_button = tk.Button(create_by_window, text="Create Random Playlist", command=self.create_random_playlist)
        random_button.pack()


class Option2Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Downloader")

        label = tk.Label(root, text="Download an MP3")
        label.pack()

        back_button = tk.Button(
            root, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack()

    def show_main_menu(self):
        self.root.destroy()  # Close the current screen
        main_menu_window = tk.Tk()
        MainMenu(main_menu_window)


class Option3Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Library")

        label = tk.Label(root, text="Your Collection")
        label.pack()

        back_button = tk.Button(
            root, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack()

    def show_main_menu(self):
        self.root.destroy()  # Close the current screen
        main_menu_window = tk.Tk()
        MainMenu(main_menu_window)



def main():
    # app = tk.Tk()
    # main_menu = MainMenu(app)
    # app.mainloop()

    # Create the main application window
    root = tk.Tk()
    app = PlaylistCreatorOption(root)
    root.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
