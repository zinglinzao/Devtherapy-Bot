import json
from pydantic import BaseModel
from gemini import GeminiAI
import difflib
from discord import Interaction, Embed, InteractionResponse

async def send_embed(ctx: Interaction, embed: Embed, ephemeral: bool = False):
    # providers linting capabilities to the editor
    response: InteractionResponse = ctx.response
    await response.send_message(embed=embed, ephemeral=ephemeral)

def calculate_similarity_percentage(reference: str, compared: str) -> float:
    """
    Calculate the similarity percentage between two strings.
    The 'reference' string is used as the baseline for comparison.

    Args:
        reference (str): The reference string which we compare against.
        compared (str): The string to compare with the reference string.

    Returns:
        float: The similarity percentage (between 0 and 100).
    """
    # Use SequenceMatcher to compute a similarity ratio.
    matcher = difflib.SequenceMatcher(None, reference, compared)
    ratio = matcher.ratio()  # Ratio is a float between 0 and 1.
    percentage = ratio * 100  # Convert to percentage.
    return percentage

mapping = {
    # Row 1
    'q': "'", 'w': ",", 'e': ".", 'r': "p", 't': "y",
    'y': "f", 'u': "g", 'i': "c", 'o': "r", 'p': "l",
    # Row 2
    'a': "a", 's': "o", 'd': "e", 'f': "u", 'g': "i",
    'h': "d", 'j': "h", 'k': "t", 'l': "n", ';': "s",
    # Row 3
    'z': ";", 'x': "q", 'c': "j", 'v': "k", 'b': "x",
    'n': "b", 'm': "m", ',': "w", '.': "v", '/': "z"
}
inverse_mapping = {value: key for key, value in mapping.items()}

async def sentence_generator(gemini: GeminiAI):
    class Data(BaseModel):
        data: str
    res = await gemini.send_prompt(
        f""
        f"generate random sentence for typing out without punctuation, sentence should be about: mountain climbing"
        f"use simple words at sentence should not be more than 6 words"
        ,
        response_schema=Data
    )
    sentence = json.loads(res)['data'].lower()
    return sentence

def qwerty_from_dvorak(text: str, character_mapping: dict) -> str:
    """
    Convert text typed on a QWERTY keyboard (but intended as Dvorak)
    into the text that would have been produced on a Dvorak layout.

    For example, with the standard mapping:
      QWERTY: q w e r t y u i o p
              a s d f g h j k l ;
              z x c v b n m , . /
      Dvorak: ' , . p y f g c r l
              a o e u i d h t n s
              ; q j k x b m w v z

    The input "jdpps" is converted to "hello".
    """
    # Mapping for lowercase characters according to physical key positions
    # Build the conversion by checking each character.
    # If the character is uppercase, convert it to lower case, map it, then re-capitalize.
    converted = ""
    for char in text:
        lower_char = char.lower()
        if lower_char in character_mapping:
            new_char = character_mapping[lower_char]
            # Preserve capitalization if necessary
            if char.isupper():
                new_char = new_char.upper()
            converted += new_char
        else:
            # For characters without mapping, keep them as is (e.g., spaces or punctuation)
            converted += char
    return converted

def calculate_word_similarity(reference_sentence: str, compared_sentence: str) -> list:
    """
    Calculate the similarity percentage for each corresponding word between two sentences.

    The reference sentence acts as the baseline. For every word in this sentence,
    the function compares it against the word at the same position within the compared sentence.
    If the compared sentence is shorter and lacks a corresponding word, a 0% similarity is returned for that position.

    Args:
        reference_sentence (str): The baseline sentence to compare against.
        compared_sentence (str): The sentence to be compared.

    Returns:
        list: A list of similarity percentages (floats) for each word in the reference sentence.

    Example:
        reference_sentence = "The quick brown fox jumps over the lazy dog"
        compared_sentence  = "The kwik brown fox jumpd over the lazi dog"
        Output might be: [100.0, 80.0, 100.0, 100.0, 80.0, 100.0, 100.0, 80.0, 100.0]
    """
    # Split both sentences into words
    ref_words = reference_sentence.split()
    cmp_words = compared_sentence.split()

    similarities = []

    # Iterate over the reference words by index.
    for i, ref_word in enumerate(ref_words):
        # Check if there is a corresponding word in the compared sentence
        if i < len(cmp_words):
            cmp_word = cmp_words[i]
            # Compute the similarity ratio between the two words
            ratio = difflib.SequenceMatcher(None, ref_word, cmp_word).ratio()
            # Multiply ratio by 100 to get percentage and round if desired
            similarities.append(ratio * 100)
        else:
            # If there's no corresponding word, we assume a similarity of 0%
            similarities.append(0.0)
    return similarities

get_average_score = lambda x: round(sum(x) / len(x), 2)

# Example usage:
if __name__ == "__main__":
    ...


