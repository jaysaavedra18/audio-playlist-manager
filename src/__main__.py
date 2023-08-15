# __main__.py

from playlist import Playlist

playlist = Playlist("My Sample Playlist")
playlist.create_playlist_by_random(5) # Create a random 5 song playlist
playlist.export_playlist()

print(playlist.total_duration)
print(playlist.total_file_size)

