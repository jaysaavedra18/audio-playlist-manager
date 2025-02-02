# utils.py

BYTES_PER_UNIT = 1024
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


def seconds_to_hhmmss(seconds: float) -> str:
    """Convert a time duration in seconds to a formatted string representing the time in hours, minutes, and seconds."""
    hours = int(seconds // SECONDS_PER_HOUR)
    minutes = int((seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
    seconds = int(seconds % SECONDS_PER_MINUTE)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def hhmmss_to_seconds(formatted_time: str) -> float:
    """Convert a formatted time string in "HH:MM:SS" format to time duration in seconds."""
    hours, minutes, seconds = map(int, formatted_time.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_mmss(seconds: float) -> str:
    """Convert a given number of seconds to a string in the 'mm:ss' format."""
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02d}:{seconds:02d}"


def mmss_to_seconds(formatted_time: str) -> int:
    """Convert a time string in 'mm:ss' format to the total number of seconds."""
    try:
        minutes, seconds = map(int, formatted_time.split(":"))
        return minutes * 60 + seconds
    except ValueError as err:
        message = "Invalid input format. Please use 'mm:ss' format."
        raise ValueError(message) from err


def bytes_to_formatted_size(file_size_bytes: int) -> str:
    """Convert a file size in bytes to a formatted string with units (e.g., "MB", "GB")."""
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while file_size_bytes >= BYTES_PER_UNIT and unit_index < len(units) - 1:
        file_size_bytes /= BYTES_PER_UNIT
        unit_index += 1

    return f"{file_size_bytes:.2f} {units[unit_index]}"


def formatted_size_to_bytes(formatted_size: str) -> int:
    """Convert a formatted file size string with units to bytes."""
    size, unit = formatted_size.split()
    size = float(size)
    unit_index = ["B", "KB", "MB", "GB", "TB"].index(unit)
    bytes_size = size * (1024**unit_index)
    return int(bytes_size)
