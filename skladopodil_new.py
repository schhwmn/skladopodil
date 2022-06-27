vowels = ['a', 'o', 'u', 'e', 'y', 'i', "'", "-", "’"]
consonants_sonorant = ['v', 'm', 'l', 'n', 'r', 'j', 'ł', 'ń', 'ŕ', 'ĭ', 'ў']
consonants_voiced = ['b', 'd', 'z', 'ǳ', 'ž', 'ǆ', 'g', 'h', 'ď', 'ź', 'ʥ']
consonants_voiceless = ['p', 't', 's', 'c', 'š', 'č', 'k', 'x', 'ť', 'ś', 'ć', 'f']
consonants_hissing = ['s', 'z', 'ǳ', 'c']
consonants_hissing_soft = ['ʥ', 'ć', 'ź', 'ś']
consonants_plosive = ['b', 'p', 'd', 't', 'g', 'k', 'ď', 'ť']
consonants_affricate = ['ǳ', 'c', 'ʥ', 'ǆ', 'ć', 'č']
consonants_fricative = ['f', 's', 'z', 'ž', 'š', 'x', 'h', 'ć', 'ź', 'ś']

def transliteration(newword: str, back=False) -> str:
    newword = newword.lower()

    transliteration_dict = {'а':'a', 'б':'b', 'в':'v', 'г':'h', 'ґ':'g',         # Using available UNICODE symbols
                            'д':'d', 'е':'e', 'ж':'ž', 'з':'z', 'и':'y',         # to transliterate the word for further use
                            'і':'i', 'й':'j', 'к':'k', 'л':'l', 'м':'m',
                            'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s',
                            'т':'t', 'у':'u', 'ф':'f', 'х':'x', 'ц':'c',
                            'ч':'č', 'ш':'š', 'щ':'šč'}
    if back == False:
        for item in transliteration_dict:
            newword = newword.replace(item, transliteration_dict[item])
    elif back == True:
        for item in transliteration_dict:
            newword = newword.replace(transliteration_dict[item], item)
    return newword

def soften_transliteration(newword: str)->str:
    double_meaning_dict = {'я':"a", "ю":"y", "є":"e", "ї":"i", "ь":"", "i":"i"}  # Transliterating vowels that soften the
    for item in double_meaning_dict:                                             # previous consonant
        newword = newword.replace('d%s' % (item), 'ď%s' % (double_meaning_dict[item]))
        newword = newword.replace('z%s' % (item), 'ź%s' % (double_meaning_dict[item]))
        newword = newword.replace('l%s' % (item), 'ł%s' % (double_meaning_dict[item]))
        newword = newword.replace('n%s' % (item), 'ń%s' % (double_meaning_dict[item]))
        newword = newword.replace('r%s' % (item), 'ŕ%s' % (double_meaning_dict[item]))
        newword = newword.replace('s%s' % (item), 'ś%s' % (double_meaning_dict[item]))
        newword = newword.replace('t%s' % (item), 'ť%s' % (double_meaning_dict[item]))
        newword = newword.replace('c%s' % (item), 'ć%s' % (double_meaning_dict[item]))
    return newword

def double_meaning_transliteration(newword:str)->str:
    double_meaning_dict_2 = {'я':"a", "ю":"y", "є":"e", "ї":"i", "ь":""}
    for item in double_meaning_dict_2:                                           # Transliterating DM-vowels when they start
        if len(newword)>0:                                                       # the syllable
            for vowel in vowels:
                newword = newword.replace('%s%s' % (vowel, item), '%sj%s' % (vowel, double_meaning_dict_2[item]))
            if newword[0] == item:
                newword = 'j' + double_meaning_dict_2[item] + newword[1:]
            newword = newword.replace(item, double_meaning_dict_2[item])
    return newword

def exceptions(newword: str) -> str:
    newword = newword.replace('lehk', 'lexk')  # Full assimilation exceptions
    newword = newword.replace('vohk', 'voxk')
    newword = newword.replace('ďohť', 'ďoxť')
    newword = newword.replace('ńihť', 'ńixť')
    newword = newword.replace('kihť', 'kixť')
    newword = newword.replace("'", '')  # Getting rid of punctuation
    newword = newword.replace('’', '')
    newword = newword.replace("-", '')
    newword = newword.replace('dz', 'ǳ')  # Using special symbols for double-symbolled consonants
    newword = newword.replace('dź', 'ʥ')
    newword = newword.replace('dž', 'ǆ')
    return newword

def end_vocalization(newword:str)->str:
    if newword.endswith('j'):                                                    # Vocalization in the end of the word
        newword = newword[:-1] + 'ĭ'
    if newword.endswith('v'):
        newword = newword[:-1] + 'ў'
    return newword

def inside_vocalization(newword:str)->str:
    for n in range(len(newword)-1):                                              # Vocalization inside of the word
        if newword[n] == 'j' and \
            (newword[n+1] in consonants_voiced or
            newword[n+1] in consonants_sonorant or
            newword[n+1] in consonants_voiceless):
            newword = newword[:n] + 'ĭ' + newword[n+1:]
        if newword[n] == 'v' and \
            (newword[n+1] in consonants_voiced or
            newword[n+1] in consonants_sonorant or
            newword[n+1] in consonants_voiceless):
            newword = newword[:n] + 'ў' + newword[n+1:]
    return newword

def voiceless_assimilation(newword:str)->str:
    voiceless_dict = {'p':'b', 't':'d', 's':'z', 'c':'ǳ', 'ć':'ʥ', 'ť':'ď', 'ś':'ź'} # Full voiceless assimilation
    for n in range(len(newword) - 1):
        for item in voiceless_dict:
            if newword[n] == item and newword[n+1] in consonants_voiced:
                newword = newword[:n] + voiceless_dict[item] + newword[n+1:]
    return newword


def creation_assimilation(newword:str)->str:
    for n in range(len(newword) - 1):
        if (newword[n] == 'd' or newword[n] == 'ď') and \
            (newword[n+1] == 'ǆ' or newword[n+1] == 'č'):                     # Place and way of creation assimilation
            newword = newword[:n] + 'ǆ' + newword[n+1:]
        if (newword[n] == 't' or newword[n] == 'ť') and \
            (newword[n+1] == 'ǆ' or newword[n+1] == 'č'):
            newword = newword[:n] + 'č' + newword[n+1:]
        if newword[n] == 'd' and newword[n+1] in consonants_hissing:
            newword = newword[:n] + 'ǳ' + newword[n+1:]
        if newword[n] == 'd' and newword[n+1] in consonants_hissing_soft:
            newword = newword[:n] + 'ʥ' + newword[n+1:]
        if newword[n] == 't' and newword[n+1] in consonants_hissing:
            newword = newword[:n] + 'c' + newword[n+1:]
        if newword[n] == 't' and newword[n+1] in consonants_hissing_soft:
            newword = newword[:n] + 'ć' + newword[n+1:]
    return newword

def soften_assimilation(newword:str)->str:
    soft_dict = ['ń', 'ď', 'ť']                                          # Full softness assimilation
    can_be_softened_dict = {'s': 'ś', 'z': 'ź', 'ǳ': 'ʥ', 'c': 'ć', 'l': 'ł', 'r': 'ŕ'}
    for n in range(len(newword) - 1):
        if newword[n] == 'n' and newword[n+1] in soft_dict:
            newword = newword[:n] + 'ń' + newword[n+1:]
        if newword[n] == 'd' and newword[n+1] in soft_dict:
            newword = newword[:n] + 'ď' + newword[n+1:]
        if newword[n] == 't' and newword[n+1] in soft_dict:
            newword = newword[:n] + 'ť' + newword[n+1:]
        for key in can_be_softened_dict:
            if newword[n] == key and newword[n+1] == can_be_softened_dict[key]:
                newword = newword[:n] + can_be_softened_dict[key] + newword[n+1:]

    return newword

def full_assimilation(newword:str)->str:
    if len(newword) > 1:                                                    # First-place position full assimilation
        if newword[0] == 'z' and newword[1] == 's':
            newword = 's' + newword[1:]
        elif newword[0] == 'z' and newword[1] == 'ś':
            newword = 'ś' + newword[1:]
        elif newword[0] == 'z' and newword[1] == 'š':
            newword = 'š' + newword[1:]
        elif newword[0] == 'z' and newword[1] == 'č':
            newword = 'š' + newword[1:]
        elif newword[0] == 'z' and newword[1] == 'c':
            newword = 's' + newword[1:]
        elif newword[0] == 'z' and newword[1] == 'ć':
            newword = 's' + newword[1:]
    return newword

def formulae_maker(word:str)->list:
    function_list = [transliteration, soften_transliteration, double_meaning_transliteration,
                     exceptions, end_vocalization, inside_vocalization, voiceless_assimilation,
                     creation_assimilation, soften_assimilation, full_assimilation]
    newword = word
    for function in function_list:
        newword = function(newword)
    formulae = [word, newword]
    return formulae

def first_division(word: str):
    only_vowels = ['a', 'o', 'u', 'e', 'y', "i"]
    index_list = []
    start = formulae_maker(word)
    base_word, formulae_word = start[0], start[1]

    for n in range(len(formulae_word) - 1):
        if formulae_word[n] in only_vowels and formulae_word[n+1] in only_vowels:
            index_list.append(n+1)

        if formulae_word[n] in consonants_sonorant and (formulae_word[n+1] in consonants_sonorant or
                                                         formulae_word[n+1] in consonants_voiced or
                                                         formulae_word[n+1] in consonants_voiceless):
            index_list.append(n+1)

        if (formulae_word[n] in consonants_voiced and formulae_word[n] in consonants_plosive) and \
            formulae_word[n+1] in consonants_voiceless:
            index_list.append(n+1)

        if (formulae_word[n] in consonants_voiced and formulae_word[n] in consonants_fricative) and \
                (formulae_word[n+1] in consonants_voiceless or
                (formulae_word[n+1] in consonants_voiced and (formulae_word[n+1] in consonants_plosive or
                                                              formulae_word[n+1] in consonants_affricate))):
            index_list.append(n+1)

        if formulae_word[n-1] in only_vowels and (formulae_word[n] in consonants_voiced or
                                             formulae_word[n] in consonants_voiceless or
                                             formulae_word[n] in consonants_sonorant) and \
            formulae_word[n+1] in only_vowels:
            index_list.append(n)
    return index_list, formulae_word

def first_insertion(inserted:tuple)->list:
    places = inserted[0]
    word = inserted[1]
    character_list = [x for x in word]
    for index in reversed(places):
        character_list.insert(index, '-')
    divided_first_time = ''.join(character_list).split('-')
    return divided_first_time

def second_division(new_list:list)->tuple:
    places_list, item_inside_list = [], []
    for item in new_list:
        for n in range(len(item) - 1):
            if (item[n] in consonants_voiceless or item[n] in consonants_voiced) and \
                            item[n + 1] in consonants_sonorant:
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

            if (item[n] in consonants_voiced and item[n] in consonants_plosive) and \
                    (item[n + 1] in consonants_voiced and (item[n + 1] in consonants_plosive or
                                                           item[n + 1] in consonants_fricative)):
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

            if (item[n] in consonants_voiceless and item[n] in consonants_plosive) and \
                            item[n + 1] in consonants_voiceless:
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

            if (item[n] in consonants_voiceless and item[n] in consonants_fricative) and \
                    (item[n + 1] in consonants_voiceless and item[n + 1] in consonants_fricative):
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

            if item[n] in consonants_affricate and (item[n + 1] in consonants_sonorant or
                                                    item[n + 1] in consonants_voiced or
                                                    item[n + 1] in consonants_voiceless):
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

            if (item[n] in consonants_voiceless and item[n] in consonants_fricative) and \
                    (item[n + 1] in consonants_voiceless and (item[n + 1] in consonants_plosive or
                                                                      item[n + 1] in consonants_affricate)):
                places_list.append(new_list.index(item))
                item_inside_list.append(n)

    return places_list, item_inside_list

def mistake_check(indexed:tuple)->tuple:
    places_list = indexed[0]
    item_inside_list = indexed[1]
    fake_list_1 = []
    fake_list_2 = []
    for n in range(len(item_inside_list)-1):
        if item_inside_list[n+1] - item_inside_list[n] == 1 and places_list[n] == places_list[n+1]:
            fake_list_1.append(n)
            fake_list_2.append(n+1)
    for item in reversed(fake_list_2):
        item_inside_list.pop(item)
    for item in reversed(fake_list_1):
        places_list.pop(item)
    return places_list, item_inside_list

def second_insertion(indexed:tuple, new_list:list)->list:
    place_index_list = zip(reversed(indexed[0]), reversed(indexed[1]))

    for item in place_index_list:
        new_list[item[0]] = new_list[item[0]][:item[1]] + '-' + new_list[item[0]][item[1]:]

    for item in new_list:
        new_item = item.split('-')
        new_list[new_list.index(item)] = new_item

    final_splitted = [item for sublist in new_list for item in sublist]
    return final_splitted


def mistake_check_2(last_list:list)->list:
    only_vowels = ['a', 'o', 'u', 'e', 'y', "i"]
    flag_1 = True
    if len(last_list) > 1:
        for character in last_list[0]:
            if character in only_vowels:
                flag_1 = False
                break

        if flag_1:
            last_list[0] = last_list[0] + last_list[1]
            last_list.pop(1)


    flag_2 = True
    if len(last_list) > 1:
        for character in last_list[-1]:
            if character in only_vowels:
                flag_2 = False
                break

        if flag_2:
            last_list[-1] = last_list[-2] + last_list[-1]
            last_list.pop(-2)


    flag_3 = True
    if len(last_list) > 1:
        for item in last_list:
            if last_list.index(item) != 0 and last_list.index(item) != -1:
                for character in item:
                    if character in only_vowels:
                        flag_3 = False
                        break

                if flag_3:
                    index = last_list.index(item)
                    last_list[last_list.index(item)] = item + last_list[last_list.index(item)+1]
                    last_list.pop(index+1)

    while '' in last_list:
        last_list.remove('')
    return last_list

def mistake_check_3(something:list)->list:
    syllables = something
    correct_list = syllables.copy()
    for syllable in syllables:
        if syllables.index(syllable) != 0:
            if syllables[syllables.index(syllable) - 1][-1] == syllable[0]:
                correct_list[syllables.index(syllable)] = syllables[syllables.index(syllable) - 1][-1] + syllable
                correct_list[syllables.index(syllable) - 1] = syllables[syllables.index(syllable)-1][:-1]

    return correct_list

def full_syllable_division(word:str)->list:

    indexes_and_word = first_division(word)
    with_defices_inbetween = first_insertion(indexes_and_word)
    items_and_places = second_division(with_defices_inbetween)
    checked_items_and_places = mistake_check(items_and_places)
    with_defices_before = second_insertion(checked_items_and_places, with_defices_inbetween)
    all_syllables_divided = mistake_check_2(with_defices_before)
    result = mistake_check_3(all_syllables_divided)

    return result