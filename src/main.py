# __main__.py
from gui import Application


def main() -> None:
    """Run the main function of the program."""
    app = Application()

    # Start the main loop of the GUI framework
    app.mainloop()


if __name__ == "__main__":
    main()
