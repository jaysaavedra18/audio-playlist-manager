import tkinter as tk
from frames.main_menu import MainMenuFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Playlist Creator")

        self.center_window()

        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes, "-topmost", False)

        self.menu_frame = MainMenuFrame(self)
        self.menu_frame.pack(fill="both", expand=True)
        self.current_frame = self.menu_frame

    def center_window(self):
        """Center the window on the screen."""
        window_width = 500
        window_height = 200

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        new_frame.pack(fill="both", expand=True)
        self.current_frame.destroy()
        self.current_frame = new_frame


def main():
    app = Application()
    app.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
