# utils.py

def format_time(seconds):
    """
    Convert a time duration in seconds to a formatted string representing the time in hours, minutes, and seconds.

    Parameters:
    seconds (float or int): Time duration in seconds.

    Returns:
    str: A formatted string representing the time duration in "HH:MM:SS" format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
