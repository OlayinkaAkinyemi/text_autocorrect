# import libraries
import re
from collections import Counter
import numpy as np
import pandas as pd

def process_data(file_name):
    """
    Input:
        A file_name which is found in your current directory. You just have to read it in.
    Output:
        words: a list containing all the words in the corpus (text file you read) in lower case.
    """
    words = [] # return this variable correctly

    ### START CODE HERE ###
    
    #Open the file, read its contents into a string variable
    with open(file_name) as file:
        string = file.read()
    # convert all letters to lower case
        string = string.lower()
            
    #Convert every word to lower case and return them in a list.
        word_list = re.findall(r"\w+", string)
        words = word_list
    ### END CODE HERE ###
    
    return words

def get_count(word_l):
    '''
    Input:
        word_l: a set of words representing the corpus.
    Output:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    '''
    
    word_count_dict = {}  # fill this with word counts
    ### START CODE HERE
    for word in word_l:
        if word in word_count_dict:
            word_count_dict[word]+=1
        else:
            word_count_dict[word] =1
    ### END CODE HERE ###
    return word_count_dict


def get_probs(word_count_dict):
    '''
    Input:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    Output:
        probs: A dictionary where keys are the words and the values are the probability that a word will occur.
    '''
    probs = {}  # return this variable correctly
    
    ### START CODE HERE ###
    
    # get the total count of words for all words in the dictionary
    
    total_word_count = np.sum([word_count_dict[key] for key in word_count_dict])
    for key in word_count_dict:
        probs[key] = word_count_dict[key]/total_word_count
    
    ### END CODE HERE ###
    return probs
    
def delete_letter(word, verbose=False):
    '''
    Input:
        word: the string/word for which you will generate all possible words
                in the vocabulary which have 1 missing character
    Output:
        delete_l: a list of all possible strings obtained by deleting 1 character from word
    '''
    
    delete_l = []
    #split_l = []
    
    ### START CODE HERE ###
    
    split_l = [(word[0:i], word[i:]) for i in range(len(word)+1)]
    for L,R in split_l:
        if R:             ### if R is not an empty string
            delete_l.append(L+R[1:])
    ### END CODE HERE ###

    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return  delete_l
    
def switch_letter(word, verbose=False):
    '''
    Input:
        word: input string
     Output:
        switches: a list of all possible strings with one adjacent charater switched
    '''
    
    switch_l = []
    #split_l = []
    
    ### START CODE HERE ###
    split_l = [(word[0:i] , word[i:]) for i in range(len(word))]
    for L,R in split_l:
        if len(R)>1:
            switch_l.append(L+R[1]+R[0]+R[2:])
            
        else:
            pass
    
    ### END CODE HERE ###
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}")
    
    return switch_l


def replace_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word
    Output:
        replaces: a list of all possible strings where we replaced one letter from the original word.
    '''
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    replace_l = []
    split_l = []
    
    ### START CODE HERE ###
    
    split_l = [(word[0:i], word[i:]) for i in range(len(word)+1)]
    for L,R in split_l:
        for letter in letters:
            if R and letter != R[0]:        #### if R is not an empty string and letter is not R[0] (the letter to be replaced)
                replace_l.append(L+letter+R[1:])


    ### END CODE HERE ###
    
    # turn the set back into a list and sort it, for easier viewing
    replace_l = sorted(list(replace_l))
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")
    
    return replace_l


def insert_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word
    Output:
        inserts: a set of all possible strings with one new letter inserted at every offset
    '''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    #split_l = []
    
    ### START CODE HERE ###
    
    split_l = [(word[0:i], word[i:]) for i in range(len(word)+1)]
    for L,R in split_l:
        new_words = [L+letter+R for letter in letters]
        insert_l.extend(new_words)
        
    ### END CODE HERE ###
    
    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return sorted(insert_l)
    

def edit_one_letter(word, allow_switches = True):
    """
    Input:
        word: the string/word for which we will generate all possible wordsthat are one edit away.
    Output:
        edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
    """
    
    edit_one_set = set()
    
    ### START CODE HERE ###
    
    if allow_switches:
        edit_one_set.update(delete_letter(word) + insert_letter(word) + replace_letter(word)
                    + switch_letter(word))
    else:
        edit_one_set.update(delete_letter(word) + insert_letter(word) + replace_letter(word))
        
    
    ### END CODE HERE ###
    
    # return this as a set and not a list
    return set(edit_one_set)
    

def edit_two_letters(word, allow_switches = True):
    '''
    Input:
        word: the input string/word
    Output:
        edit_two_set: a set of strings with all possible two edits
    '''
    
    edit_two_set = set()
    
    ### START CODE HERE ###
    edit_one_set = edit_one_letter(word, allow_switches)
    for editted_word in edit_one_set:
        edit_two_set.update(edit_one_letter(editted_word, allow_switches))
        
    ### END CODE HERE ###
    
    # return this as a set instead of a list
    return set(edit_two_set)
    
    
def get_corrections(word, probs, vocab, n=2, verbose = False):
    '''
    Input:
        word: a user entered string to check for suggestions
        probs: a dictionary that maps each word to its probability in the corpus
        vocab: a set containing all the vocabulary
        n: number of possible word corrections you want returned in the dictionary
    Output:
        n_best: a list of tuples with the most probable n corrected words and their probabilities.
    '''
    
    #suggestions = []
    #n_best = []
    
    ### START CODE HERE ###
    #Step 1: create suggestions as described above
    #suggestions = None
    if word in vocab:
        suggestions=[word]
    else:
        suggestions = edit_one_letter(word) or edit_two_letters(word) or [word]
        
        
                    
    #Step 2: determine probability of suggestions
    prob_dict = {suggestion:0 for suggestion in suggestions} ### initialize prob to 0
    for suggestion in suggestions:
        if suggestion in vocab:
            prob_dict[suggestion] = probs[suggestion]
    
    # sort the dictionary by its values, in descending order
    sorted_prob = sorted(prob_dict.items(), key=lambda x:x[1], reverse=True)  ## returns a list
    
    #Step 3: Get all your best words and return the most probable top n_suggested words as n_best
    # get the keys of the first n items in the dictionary
    
    n_best = [i for i in sorted_prob[0:n]]
    
    # select the first n most probable words
    suggestions = [i[0] for i in sorted_prob[0:n]]
    ### END CODE HERE ###
    
    if verbose: print("entered word = ", word, "\nsuggestions = ", suggestions)

    return n_best

word_list = process_data("./data/shakespeare.txt")
vocab = set(word_list)  ### get unique words in vocabulary
word_count_dict = get_count(word_list)
word_probs = get_probs(word_count_dict)
word = "dys"
corrections = get_corrections(word, word_probs, vocab, 6, verbose=True)

