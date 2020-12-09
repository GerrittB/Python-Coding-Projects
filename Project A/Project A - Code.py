# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
        if char not in letters_guessed:
            return False
        else:
            return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed = []
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            guessed.append(secret_word[i])

        else:
            guessed.append('_ ')
    return ''.join(guessed)

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    lowercase = string.ascii_lowercase
    a = []
    for char in lowercase:
        if char not in letters_guessed:
            a.append(char)
    return ''.join(a)

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('Lets play Hangman!')
    print('I am thinking of a word that is %d letters long.' % (len(secret_word)))
    print('You have 3 warnings remaining.')
    letters_guessed = []
    num_warnings = 0
    i = 0
    while i < 6:
        print('-------------')
        print('You have %d guesses remaining.' % (6-i))
        print('Available letters:', get_available_letters(letters_guessed))
        new_guess = input(str('Please guess a letter:'))
        if str.isalpha(new_guess):
            if str.isupper(new_guess):
                new_guess = str.lower(new_guess)
            if new_guess in letters_guessed:
                num_warnings += 1
                if num_warnings < 4:
                    print('You\'ve already guessed that letter.You now have %d warnings remaining: %s' \
                        % ((3 - num_warnings), get_guessed_word(secret_word, letters_guessed)))
                elif num_warnings == 4:
                    print('You\'ve already guessed that letter.You now have no warnings remaining:\n ' 
                          'so you lose one guess: %s' % (get_guessed_word(secret_word, letters_guessed)))
                    i += 1
                else:
                    break

            else: 
                letters_guessed.append(new_guess)
                if is_word_guessed(new_guess, secret_word):
                    print('Good guess:', get_guessed_word(secret_word, letters_guessed))
                    if get_guessed_word(secret_word, letters_guessed) == secret_word:
                        print('------------\nCongratulations you won!\n'
                              'Your total score for this game is: %d' % (len(set(secret_word)) * (6 - i)))
                        break

                else:
                    if new_guess in ['a', 'e', 'i', 'o', 'u']:
                        print('That letter is not in the word:', \
                              get_guessed_word(secret_word, letters_guessed))
                        i += 2
                    else:
                        print('That letter is not in the word:\n'
                              'Please guess a letter:', \
                              get_guessed_word(secret_word, letters_guessed))
                        i += 1

        else:
            num_warnings += 1
            if num_warnings < 3:
                print('That is not a valid letter. You have %d warnings remaining: %s' \
                      % ((3-num_warnings), get_guessed_word(secret_word, letters_guessed)))
            else:
                break

    if i == 6:
        print('-----------\n'
              'You ran out of guesses.'
              ' The word was %s.' % secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    num = 0
    my_word = my_word.replace(' ', '')
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] == '_' or my_word[i] == other_word[i]:
                pass
            else:
                num += 1
        if num == 0:
            return True
        else:
            return False
    else:
        return False

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    list = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            list.append(word)

    if len(list) != 0:
        print(' '.join(list))
    else:
        print('No matches found')

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('Lets play Hangman!')
    print('I am thinking of a word that is %d letters long.' % (len(secret_word)))
    print('You have 3 warnings remaining.')
    letters_guessed = []
    num_warnings = 0
    i = 0
    while i < 6:
        print('-------------')
        print('You have %d guesses remaining.' % (6 - i))
        print('Available letters:', get_available_letters(letters_guessed))
        new_guess = input(str('Please guess a letter:'))
        if str.isalpha(new_guess):
            if str.isupper(new_guess):
                new_guess = str.lower(new_guess)
            if new_guess in letters_guessed:
                num_warnings += 1
                if num_warnings < 4:
                    print('You\'ve already guessed that letter.You now have %d warnings remaining: %s' \
                          % ((3 - num_warnings), get_guessed_word(secret_word, letters_guessed)))
                elif num_warnings == 4:
                    print('You\'ve already guessed that letter.You now have no warnings remaining:\n '
                          'so you lose one guess: %s' % (get_guessed_word(secret_word, letters_guessed)))
                    i += 1
                else:
                    break

            else:
                letters_guessed.append(new_guess)
                if is_word_guessed(new_guess, secret_word):
                    print('Good guess:', get_guessed_word(secret_word, letters_guessed))
                    if get_guessed_word(secret_word, letters_guessed) == secret_word:
                        print('------------\nCongratulations you won!\n'
                              'Your total score for this game is: %d' % (len(set(secret_word)) * (6 - i)))
                        break

                else:
                    if new_guess in ['a', 'e', 'i', 'o', 'u']:
                        print('That letter is not in the word:', \
                              get_guessed_word(secret_word, letters_guessed))
                        i += 2
                    else:
                        print('That letter is not in the word:\n'
                              'Please guess a letter:', \
                              get_guessed_word(secret_word, letters_guessed))
                        i += 1

        elif new_guess == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))

        else:
            num_warnings += 1
            if num_warnings < 3:
                print('That is not a valid letter. You have %d warnings remaining: %s' \
                      % ((3 - num_warnings), get_guessed_word(secret_word, letters_guessed)))
            else:
                break

    if i == 6:
        print('-----------\n'
              'You ran out of guesses.'
              ' The word was %s.' % secret_word)

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass


    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)