class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Main Menu")
        label.pack()

        playlist_button = tk.Button(
            self, text="Playlist Creator", command=lambda: master.show_frame(PlaylistCreatorFrame))
        playlist_button.pack()

        option2_button = tk.Button(
            self, text="Song Library", command=lambda: master.show_frame(SongLibraryFrame))
        option2_button.pack()
