# utils.py

# Define utility functions for common operations

def seconds_to_hhmmss(seconds: int | float) -> str:
    """Convert a time duration in seconds to a formatted string representing the time in hours, minutes, and seconds."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def hhmmss_to_seconds(formatted_time: str) -> float:
    """Convert a formatted time string in "HH:MM:SS" format to time duration in seconds."""
    hours, minutes, seconds = map(int, formatted_time.split(":"))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def seconds_to_mmss(seconds: int | float) -> str:
    """Convert a given number of seconds to a string in the 'mm:ss' format."""
    minutes = seconds // 60
    seconds %= 60
    mmss_format = f"{minutes:02d}:{seconds:02d}"
    return mmss_format


def mmss_to_seconds(formatted_time: str) -> int:
    """Convert a time string in 'mm:ss' format to the total number of seconds."""
    try:
        minutes, seconds = map(int, formatted_time.split(":"))
        total_seconds = minutes * 60 + seconds
        return total_seconds
    except ValueError:
        raise ValueError("Invalid input format. Please use 'mm:ss' format.")



def bytes_to_formatted_size(file_size_bytes: int) -> str:
    """Convert a file size in bytes to a formatted string with units (e.g., "MB", "GB")."""
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while file_size_bytes >= 1024 and unit_index < len(units) - 1:
        file_size_bytes /= 1024
        unit_index += 1

    return f"{file_size_bytes:.2f} {units[unit_index]}"


def formatted_size_to_bytes(formatted_size: str) -> int:
    """Convert a formatted file size string with units to bytes."""
    size, unit = formatted_size.split()
    size = float(size)
    unit_index = ["B", "KB", "MB", "GB", "TB"].index(unit)
    bytes_size = size * (1024 ** unit_index)
    return int(bytes_size)
