from collections import Counter
import json
# alph = 'abcdefghijklmnopqrstuvwxyz'
# alph_dict = {i:[] for i in alph}

# with open('application/words_dictionary.json', 'r') as file:
#     d_file = json.load(file).keys()
#     for word in d_file:
#         most_freq_letter = Counter(word).most_common(1)[0][0]
#         alph_dict[most_freq_letter].append(word)
#         # print(alph_dict[most_freq_letter])
# with open('application/sorted_words.json','r') as file:
#     json_file = json.load(file)
#     counter = 0
#     for i in json_file['a']:
#         if counter == 30:
#             break
#         print(Counter(i).most_common(2)[0][0])
#         print(Counter(i))

#         counter+=1

a = 'aaabbb'
cont = Counter(a).most_common(len(a))
print(cont)
print([i[0] for i in cont if i[1]==cont[0][1]])