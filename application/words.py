from collections import Counter
import os
import json
from random import choice,randint
print(os.getcwd())
def rand_test(): # get random letter and word quantity for typing practice
    alph = 'abcdefghijklmnopqrstuvwxyz'
    letter = choice(alph)
    length = choice(range(1,50))
    return {'letter':letter, 'string_length':length}
def words_taking(val_dict:dict[str,int]): # get words from dictionary file using letter and string_length parameters. String length - amount of words taken from dictionary.
    with open('var/www/keyboard_trainer/application/sorted_words.json', 'r') as json_f: #Change the path according to your settings
        json_words_dict = json.load(json_f)
        return [json_words_dict[val_dict['letter']][randint(0, len(json_words_dict[val_dict['letter']]))] for _ in range(val_dict['string_length'])]

def word_freq_sort(): # sort words by most frequent letter
    from collections import Counter
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alph_dict = {i:[] for i in alph}
    with open('var/www/keyboard_trainer/application/words_dictionary.json', 'r') as file: #Change the path according to your settings
        d_file = json.load(file).keys()
        for word in d_file:
            m_freq_cntr = Counter(word).most_common(len(word)) # letter frequency in a word
            m_freq_lst = [i[0] for i in m_freq_cntr if i[1]==m_freq_cntr[0][1]] # list with the most freq letters
            for letter in m_freq_lst: # add dict value to most freq letter key
                alph_dict[letter].append(word)
        with open('var/www/keyboard_trainer/application/sorted_words.json','w') as file: # create json file with sorted letters. Change the path according to your settings
            json_file = json.dump(alph_dict,fp=file)
