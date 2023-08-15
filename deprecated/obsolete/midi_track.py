from midiutil import MIDIFile
from mingus.core import chords
from openai_proxy import generate_progressions
from datetime import date
import random
import os

# chord_progression to generate
DEF_CHORD_PROGRESSION = ["Cmaj7", "Cmaj7", "Fmaj7", "Gdom7"] # OpenAI response format: (Cmaj7, Cmaj7, Fmaj7, Gdom7)

# Track Name
FILENAME = 'midi-track' + '-'

# Valid Inputs for Notes, Octaves, and Size of list 
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

PATH = os.getcwd() + '/generated-midis'
DATE = str(date.today())
NUMBER_OF_PROGRESSIONS = random.randint(4,7)

def create_folder_with_duplicates(path, folder_name):
    folder_path = os.path.join(path, folder_name)

    if not os.path.exists(folder_path):
        # Folder with the given name doesn't exist, so create it directly.
        os.makedirs(folder_path)
        return folder_path

    # Folder with the given name exists, so find a new name with a suffix.
    suffix = 1
    while True:
        new_folder_name = f"{folder_name} ({suffix})"
        new_folder_path = os.path.join(path, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            return new_folder_path
        suffix += 1
    
FOLDER_PATH = create_folder_with_duplicates(PATH, DATE)

# Standard error message to add specifics to
errors = {
    'notes': 'Bad input, please refer this spec-\n'
}

class MIDITrack:
    """This class is a MIDITrack class where the inputs generate a MIDITrack 
    in the directory.

    The class has default attributes in the contructor but needs input to build 
    tracks for different rhythmsections.

    Attributes:
        chord_progression (list of str): list of the notes in the chord progression
        octave (int): octave to play the notes in
        track (int): number of the current track (we can leave at 0)
        channel (int): number of the current channel
        time (int): number in beats for note to be played
        duration (int): length in beats
        tempo (int): bpm of the track
        volume (int): volume of the track

    Methods:
        method1(): Description of method1.
        method2(arg1, arg2): Description of method2.
    """
    def __init__(self, track_number, chord_progression=DEF_CHORD_PROGRESSION, octave=7, track=0, channel=0, time=0, duration=1, tempo=120, volume=100, notes_per_beat=4):
        self.track = track
        self.channel = channel
        self.time = time
        self.duration = duration
        self.tempo = tempo
        self.volume = volume

        array_of_notes = []
        for chord in chord_progression:
            array_of_notes.append(chords.from_shorthand(chord)[0])

        array_of_note_numbers = []
        for note in array_of_notes:
            array_of_note_numbers.append(note_to_number(note, octave))

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
        # automatically)
        MyMIDI.addTempo(track, time, tempo)

        for i, pitch in enumerate(array_of_note_numbers):
            MyMIDI.addNote(track, channel, pitch, time + (i*4 / notes_per_beat), duration, volume)

        midi_file_path = os.path.join(FOLDER_PATH, f"{FILENAME}{track_number}.mid")
        with open(midi_file_path, "wb") as output_file:
            MyMIDI.writeFile(output_file)
        
def swap_accidentals(note):
    """
    Swap accidentals of the note.

    Some notes can be recognized by two names and so this swaps the note with its other name.
  
    Parameters:
    note (str): The note to be swapped.
  
    Returns:
    str: The swapped note.
  
    """
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'

    return note


def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']
    return note


def main():
    track_number = 1
    chord_progressions = generate_progressions(NUMBER_OF_PROGRESSIONS)
    for chord_progression in chord_progressions:
        current_track = MIDITrack(chord_progression=chord_progression, track_number=track_number)
        track_number += 1

if __name__ == '__main__':
    main()
