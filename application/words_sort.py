async def w_sort(letter: str, words_tuple, result_dict: dict): # create dictionary where keys are all alphabet
    # letters, and values are all words, where these letters are present
    for word in words_tuple:
        if letter in word.lower():
            # result_dict[letter].add(word.lower())
            result_dict[letter].append(word.lower())
