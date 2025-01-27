from pathlib import Path

import pandas as pd

from src.config import FMA_METADATA_DIRECTORY

# Load the FMA metadata files

tracks_metadata = pd.read_csv(Path(FMA_METADATA_DIRECTORY) / "tracks.csv")
features_metadata = pd.read_csv(Path(FMA_METADATA_DIRECTORY) / "features.csv")
genres_metadata = pd.read_csv(Path(FMA_METADATA_DIRECTORY) / "genres.csv")

# Align the metadata files based on the track_id
features_metadata = features_metadata.set_index("track_id")
tracks_metadata = tracks_metadata.set_index("track_id")

# Merge the metadata files
fma_metadata = features_metadata.merge(
    tracks_metadata,
    left_index=True,
    right_index=True,
)
