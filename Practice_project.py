# Function kind_fermet, takes 3 positive integers, testing if equality holds.
def kinda_fermat(a, b, c):
    # numbers = [a, b, c]
    n = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    values_of_n = []
    # looping through the values of n to check if equation holds
    for i in range(len(n)):
        cur_number_n = n[i]
        if (a**cur_number_n + b**cur_number_n) == c**cur_number_n:
            values_of_n.append(cur_number_n)
            break
    # returning the smallest value of n, stopping the loop at the first value
    # with keyword 'break' to avoid running extra lines of code
    if values_of_n:
        return values_of_n[0]
    else:
        return False

    

# Function counts number of words in wlist whose length is > or = to wlen
def unique_long_words(wlist, wlen):
    num_of_unique_words = 0
    needed_words = []
    # Loop through list of words to ensure no word is repeated twice.
    # If word has already been seen, it is ignored. 
    for word in wlist:
        # print(word)
        if word in needed_words:
            pass
        else:
            needed_words.append(word)

    for element in needed_words:
        word_len = len(element)
        if word_len == wlen:
            num_of_unique_words += 1
        elif word_len > wlen:
            num_of_unique_words += 1
        else:
            pass
    return num_of_unique_words


#function that finds if a word is symmetric
def symmetric_words(wlist):
    odd_nums = ['1', '3', '5', '7', '9']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_reverse = alphabet[::-1]
    # print(alphabet_reverse)
    even_words = []
    symm_words = []
    
    # Getting the list of even words, which can be symmetric.
    for element in wlist:
        if element == " ":
            even_words.append(element)
        elif str(len(element)) in odd_nums:
            pass
        else:
            even_words.append(element)
    # Comparing characters in the first part of the word with the second part
    for word in even_words:
        check = True
        half = int(len(word) / 2)
        first_half = word[:half]
        second_half = word[half:]
        second_half = second_half[::-1]
        # pos_in_alphabet = alphabet.find(word)
        for i in range(len(first_half)):
            
            pos_in_alphabet = alphabet.find(first_half[i])
            sec_pos_in_alphabet = alphabet_reverse.find(second_half[i])
                
            # print(f"{first_half[i]} at {pos_in_alphabet}")
            # print(f"{second_half[i]} at {sec_pos_in_alphabet}")
            # (i == len(first_half - 1))
            if (pos_in_alphabet != sec_pos_in_alphabet):
                check = False
                break
        if check:
            symm_words.append(word)
                
    return symm_words


#Find the words with the least vowels
def least_vowel_words(text):
    min_vowel_proportion = 1
    VOWELS = 'aeiou'
    vowel_proportion = {}
    word_with_min = 'aeiou'
    more_words_with_min = []
    text = text.strip(''',.:;!?'"-''')
    text = text.split()
    
    for word in text:
        if word[0] not in ''',.:;!?'"-''':
            vowel_count = 0
            for char in word:
                if char in VOWELS:
                    vowel_count += 1
            proportion = vowel_count/len(word)
            vowel_proportion[word] = proportion
    # print(vowel_proportion)
    for element in vowel_proportion:
        if vowel_proportion[element] < min_vowel_proportion:
            word_with_min = element
    for thing in vowel_proportion:
        if vowel_proportion[thing] == min_vowel_proportion:
            more_words_with_min.append(thing)
    return more_words_with_min

print(least_vowel_words("the rhythm of life"))
print(least_vowel_words("The quality of mercy is not strain'd ... mercy Percy."))def least_vowel_words(text):
    min_vowel_proportion = 1
    VOWELS = 'aeiou'
    vowel_proportion = {}
    word_with_min = 'aeiou'
    more_words_with_min = []
    text = text.strip(''',.:;!?'"-''')
    text = text.split()
    
    for word in text:
        if word[0] not in ''',.:;!?'"-''':
            vowel_count = 0
            for char in word:
                if char in VOWELS:
                    vowel_count += 1
            proportion = vowel_count/len(word)
            vowel_proportion[word] = proportion
    # print(vowel_proportion)
    for element in vowel_proportion:
        if vowel_proportion[element] < min_vowel_proportion:
            word_with_min = element
    for thing in vowel_proportion:
        if vowel_proportion[thing] == min_vowel_proportion:
            more_words_with_min.append(thing)
    return more_words_with_min

print(least_vowel_words("the rhythm of life"))
print(least_vowel_words("The quality of mercy is not strain'd ... mercy Percy."))
