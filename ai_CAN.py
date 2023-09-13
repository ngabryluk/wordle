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
    wordlist = [j for j in wordlist if j != '']
    

    # These two words contain the 10 most commonly used letters in the English language
    # If it's the first guess, return a hard-coded first word
    if len(guesses) == 0:
        wordlist = utils.readwords("allwords5.txt")
        return 'STAIN'
    else:
        # Remove previous guesses from the wordlist so they aren't picked multiple times 
        for word in guesses:
            wordlist.remove(word)
    
    # If the first word had no correct letters, hard-code another word
    if len(guesses) == 1 and feedback[len(feedback) - 1] == [0, 0, 0, 0, 0]:
        return 'CEORL'

    last_guess = guesses[len(guesses) - 1]
    last_feedback = feedback[len(feedback) - 1]
    
    # Create a list of length 5 representing the amount of possible letters that a given space could have
    #   - We will remove letters from ALL these alphabet strings if not in the word
    #   - We will remove letters from the spot they were in but not the others if yellow
    #   - We will remove all but the letter in the spot but not the others if green
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # valid letters to guess
    lettersPerWord = []
    for i in range(5):
        lettersPerWord.append(ALPHABET)

    almostCorrect = [] # Keep a list of almost correct letters to make sure that they are always in the next guess
    # Test out removing letters from 
    # word = 'WORLD'
    # feedback = '20010'

    # Update the possible letters that could be in each spot

    # Looping through each of the 5 letter spots in the word
    for i in range(5):
        # If correct make the possible letters list at that spot just the letter (Because it's the correct one)
        # Keep in mind this doesn't remove it from other possible spots
        if last_feedback[i] == 2:
            lettersPerWord[i] = last_guess[i]
        # If almost correct (in the word but not the correct spot), remove from list at that spot
        elif last_feedback[i] == 1:
            lettersPerWord[i] = lettersPerWord[i].replace(last_guess[i], "")
            almostCorrect.append(last_guess[i]) # Add to almost correct letter list
        # If incorrect, remove the wrong letter from all possible letter lists
        else:
            # There is a case where if a letter appears twice in the secret word and one of those letters
            # has been correctly guessed but not the other; what happened before is that we would remove 
            # that letter from all the lettersPerWord strings, which includes the string that has the only
            # correct letter in it, breaking the algorithm.

            # Solution: Check if letter has already been guessed correctly in another spot by checking if
            # it is the only char in another spot. If it is, only remove it as a possibility in the current spot.
            # If not, it's not in the word so remove it from all possible spots
            alreadyInWord = False
            for group in lettersPerWord:
                if len(group) == 1 and group[0] == last_guess[i]:
                    lettersPerWord[i] = lettersPerWord[i].replace(last_guess[i], "")
                    alreadyInWord = True
                    break

            if not alreadyInWord:
                lettersPerWord = [list.replace(last_guess[i], "") for list in lettersPerWord]
            
    # Filter down the wordlist based on the updated possible letters

    # Flags that will store whether or not the letter is already correct so that we don't need to check
    # that spot in the wordlist
    # correctSpots = []

    # if len(feedback) > 1:
    #     for i in range(5):
    #         correctSpots.append(feedback[len(feedback) - 2][i] == 2)
    
    # pdb.set_trace()
    # Loop through each letter spot
    for i in range(5):

        # If there is only one possible letter, that is the letter
        if len(lettersPerWord[i]) == 1:
            for j in range(len(wordlist)):
                if lettersPerWord[i][0] != wordlist[j][i]:
                    wordlist[j] = ''
            wordlist = [j for j in wordlist if j != '']
        
        elif len(lettersPerWord[i]) > 1:
            for j in range(len(wordlist)):
                # If the letter in the current spot is not in the list of possible letters, remove the word
                if wordlist[j][i] not in lettersPerWord[i]:
                    wordlist[j] = ''
            wordlist = [j for j in wordlist if j != '']

        # If the letter in this spot is correct...
        # if last_feedback[i] == 2:
            # Remove all words that don't have the correct letter in this spot
            
            # correctSpots[i] = True # Update the flag for the current spot
        
        # If the letter in this spot is almost correct...
        # elif last_feedback[i] == 1:
        #     # Get rid of every word that has a letter in this spot
        #     for j in range(len(wordlist)):
        #         if last_guess[i] == wordlist[j][i]:
        #             wordlist[j] = ''
        #     wordlist = [j for j in wordlist if j != '']
       

    # Make a random guess from the remaining possible words

    guess = random.choice(wordlist)
    allYellowsInGuess = False # Flag determining whether or not all the yellow letters are in the guess
    while not allYellowsInGuess:
        invalidGuess = False # Flag to help break the for loop and continue the while loop
        # Loop through each of the yellow letters
        for letter in almostCorrect:
            if letter not in guess:
                guess = random.choice(wordlist)
                invalidGuess = True
                break
        
        if invalidGuess:
            continue

        allYellowsInGuess = True # If we make it to this point, the word has all the previous yellow letters
    wordlist = utils.readwords("allwords5.txt")
    return guess


if __name__ == "__main__":
    wordlist = utils.readwords("allwords5.txt")
    print(f"AI: \"My next choice would be {makeguess(wordlist)}\"")