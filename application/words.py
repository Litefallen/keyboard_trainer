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
    # print(letter,string_length)
    with open('application/final_file.json', 'r') as json_f:
        json_words_dict = json.load(json_f)
        # for _ in range(string_length):
            # randint(0, len(json_words_dict[letter]))
            # print(json_words_dict[letter][randint(0, len(json_words_dict[letter]))])
        return [json_words_dict[val_dict['letter']][randint(0, len(json_words_dict[val_dict['letter']]))] for _ in range(val_dict['string_length'])]
        # json_words_dict[letter]


# async def main():
    # words_dict = {i: [] for i in 'abcdefghijklmnopqrstuvwxyz'}
    # with open('words.txt', 'r') as f:
    #     f = tuple([i.lower().strip() for i in f]) # create tuple with all lowercased words
    #     await asyncio.gather(*[w_sort(i, f, words_dict) for i in 'abcdefghijklmnopqrstuvwxyz'])
    # with open('final_file.json','w') as f2:
    #     json_str = json.dumps(words_dict)
    #     f2.write(json_str) # create json file with organized dictionary with words
# asyncio.run(main())
    
with open('application/final_file.json','r') as json_f:
    json_words_dict = json.load(json_f)