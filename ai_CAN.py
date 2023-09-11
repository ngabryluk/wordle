# ai_CAN.py
# AI Wordle player created by Noah Gabryluk and Matt Flammenspeck

import pdb
import random
import utils

def makeguess(wordlist, guesses=[], feedback=[]):
    """Guess a word from the available wordlist, (optionally) using feedback 
    from previous guesses.
    
    Parameters
    ----------
    wordlist : list of str
        A list of the valid word choices. The output must come from this list.
    guesses : list of str
        A list of the previously guessed words, in the order they were made, 
        e.g. guesses[0] = first guess, guesses[1] = second guess. The length 
        of the list equals the number of guesses made so far. An empty list 
        (default) implies no guesses have been made.
    feedback : list of lists of int
        A list comprising one list per word guess and one integer per letter 
        in that word, to indicate if the letter is correct (2), almost 
        correct (1), or incorrect (0). An empty list (default) implies no 
        guesses have been made.
    Output
    ------
    word : str
        The word chosen by the AI for the next guess.
    """

    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # valid letters to guess

    # Create a list of length 5 representing the amount of possible letters that a given space could have
    # We will remove letters from these alphabet strings as we make guesses
    lettersPerWord = []
    for i in range(5):
        lettersPerWord.append(ALPHABET)

    return lettersPerWord
    
def main():
    makeguess()

if __name__ == "__main__":
    main()