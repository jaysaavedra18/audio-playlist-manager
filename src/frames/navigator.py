def navigate_to(frame, app_context):
    if frame == "main_menu":
        from .main_menu import MainMenuFrame
        return MainMenuFrame(app_context)
    elif frame == "playlist_creator":
        from .playlist_creator import PlaylistCreatorFrame
        return PlaylistCreatorFrame(app_context)
    elif frame == "song_library":
        from .song_library import SongLibraryFrame
        return SongLibraryFrame(app_context)
    elif frame == "edit_tags":
        from .edit_tags import EditTagsFrame
        return EditTagsFrame(app_context)
    elif frame == "create_by":
        from .create_by import CreateByFrame
        return CreateByFrame(app_context)