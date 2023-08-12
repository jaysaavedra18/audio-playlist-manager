import openai
import os

# Provide our openai api key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a generate_progressions function
def generate_progressions(number_of_progressions) -> list[list[str]]:
    """
    This costs money! This function queries openai chatgpt responses.

    Args:
        prompt: The prompt for openai chatbot.

    Returns:
        progressions: A list of the chord progressions which are themselves lists of strings that represent each chord.
    """
    system_role = """
    You are a Music Producing machine specializing in R&B, Hip-Hop, Raggae, and Afrobeats genres.
    Your responses are formatted specifically to ease parsing.
    You avoid words in your responses and only focus on generating chord progressions.
    """

    example_progressions = [
        """
        Cmaj7,Am7,Dm7,G7
        Fmaj7,Bm7b5,Em7,A7
        Gmaj7,Em7,Am7,D7
        Dmaj7,Bm7,Em7,A7
        Bbmaj7,Cm7,F7,Bbmaj7
        Aadd9,C#m7,F#m7,Dmaj7
        """,
        """
        Em7,A7,Dmaj7,Gmaj7
        Bm7,E7,Amaj7,Dmaj7
        Cmaj7,Gmaj7,Fmaj7,Gmaj7
        Am7,Dm7,G7,Cmaj7
        Dm7,G7,Cmaj7,Fmaj7
        Fmaj7,Bbmaj7,Dm7,G7
        """
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": "Give me 6 chord progressions that would sound nice together."},
            {"role": "assistant", "content": example_progressions[0]},
            {"role": "user", "content": "Give me 6 chord progressions that would sound nice together."},
            {"role": "assistant", "content": example_progressions[1]},
            {"role": "user", "content": f"Give me {number_of_progressions} chord progressions that would sound nice together."},
        ]
    )
    content = response['choices'][0]['message']['content']
    # print(content)
    progressions = parse_chord_progressions(content)
    return progressions

def parse_chord_progressions(input_string):
    chord_progressions = []

    lines = input_string.strip().split('\n')
    for line in lines:
        chord_progression = line.replace(" ", "").replace("\t", "").replace("\n", "").split(',')
        chord_progressions.append(chord_progression)

    return chord_progressions