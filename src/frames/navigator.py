import tkinter as tk


def navigate_to(frame: str, app_context: tk.Tk) -> tk.Frame:
    """Navigate to the frame specified by the frame parameter."""
    if frame == "main_menu":
        from .main_menu import MainMenuFrame

        app_context.show_frame(MainMenuFrame)
        return MainMenuFrame(app_context)
    if frame == "playlist_creator":
        from .playlist_creator import PlaylistCreatorFrame

        app_context.show_frame(PlaylistCreatorFrame)
        return PlaylistCreatorFrame(app_context)
    if frame == "song_library":
        from .song_library import SongLibraryFrame

        app_context.show_frame(SongLibraryFrame)
        return SongLibraryFrame(app_context)
    if frame == "edit_tags":
        from .edit_tags import EditTagsFrame

        app_context.show_frame(EditTagsFrame)
        return EditTagsFrame(app_context)
    if frame == "create_by":
        from .create_by import CreateByFrame

        app_context.show_frame(CreateByFrame)
        return CreateByFrame(app_context)
    return None
