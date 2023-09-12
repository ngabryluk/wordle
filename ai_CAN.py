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
    #   - We will remove letters from ALL these alphabet strings if not in the word
    #   - We will remove letters from the spot they were in but not the others if yellow
    #   - We will remove all but the letter and that letter from the other alphabet strings if green
    lettersPerWord = []
    for i in range(5):
        lettersPerWord.append(ALPHABET)

    print(lettersPerWord)

    # Test out removing letters from 
    word = 'WORLD'
    
    # Looping through each of the 5 letter spots
    for i in range(5):
        # If correct make the possible letters list at that spot just the letter (Because it's the correct one)
        if feedback[i] == 2:
            lettersPerWord[i] = word[i]
        # If almost correct (in the word but not the correct spot), remove from list at that spot
        elif feedback[i] == 1:
            lettersPerWord[i].replace(word[i], "")
        # If incorrect, remove the wrong letter from all possible letter lists
        else:
            lettersPerWord = [list.replace(word[i], "") for list in lettersPerWord]



def main():
    makeguess()

if __name__ == "__main__":
    main()