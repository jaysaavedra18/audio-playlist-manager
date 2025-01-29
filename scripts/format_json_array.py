import json
from pathlib import Path


def format_json(filepath: str, key_name: str) -> None:
    """Format a JSON file containing an array of objects into a dictionary."""
    with Path.open(filepath, "r") as file:
        data = json.load(file)

    formatted_data = {}
    for item in data:
        key_value = item[key_name]
        formatted_data[key_value] = {k: v for k, v in item.items() if k != key_name}

    with Path.open(filepath, "w") as file:
        json.dump(formatted_data, file, indent=4)


# Usage:
# format_json("songs.json", "song_name")  # noqa: ERA001
