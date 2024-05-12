from collections import Counter
import asyncio
import os
import json
from random import choice,randint
# from .words_sort import w_sort
print(os.getcwd())
def rand_test():
    alph = 'abcdefghijklmnopqrstuvwxyz'
    letter = choice(alph)
    length = choice(range(1,50))
    return {'letter':letter, 'string_length':length}
def words_taking(val_dict:dict[str,int]):
    with open('application/sorted_words.json', 'r') as json_f:
        json_words_dict = json.load(json_f)
        return [json_words_dict[val_dict['letter']][randint(0, len(json_words_dict[val_dict['letter']]))] for _ in range(val_dict['string_length'])]

def word_freq_sort(): # sort words by most frequent letter
    from collections import Counter
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alph_dict = {i:[] for i in alph}
    with open('application/words_dictionary.json', 'r') as file:
        d_file = json.load(file).keys()
        for word in d_file:
            most_freq_letter = Counter(word).most_common(1)[0][0]
            alph_dict[most_freq_letter].append(word)
        with open('application/sorted_words.json','w') as file: # create json file with sorted letters
            json_file = json.dump(alph_dict,fp=file)
