from unidecode import unidecode
import string
import re


def to_lower(sentence: str):
    return sentence.lower()


def remove_numbers(sentence: str):
    return re.sub(r'\d+', '', sentence)


def remove_punctuation(sentence: str):
    PUNCTUATION = string.punctuation           
    translator = str.maketrans(PUNCTUATION, " "*len(PUNCTUATION))
    return sentence.translate(translator)


def remove_whitespaces(sentence: str):
    return " ".join(sentence.split())


def special_characters_to_ascii(sentence: str):
    return unidecode(sentence)


def standardize(sentence:str):
    # Treat number 
    sentence = remove_numbers(sentence)
    
    # Remove punctuation
    sentence = remove_punctuation(sentence)

    # Convert special characters
    sentence = special_characters_to_ascii(sentence)

    # Normalizing case
    sentence = to_lower(sentence)

    # Remove extra whitespaces
    sentence = remove_whitespaces(sentence)

    return sentence
