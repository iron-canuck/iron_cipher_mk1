"""
1- error handling: in case the user enters a character that ain't supported
"""

import string
import random


# encryption function : core function
def encrypt(word):
    """
    for each letter in our word, go to our dictionary look for the letter in our keys, and add its
    VALUE to encrypted_word
    """

    # 1- get all the characters that are allowed, assign them to a string called keys.
    keys = string.ascii_letters + string.digits + string.whitespace + string.punctuation
    # print(type(keys))        # check what is the type of keys

    # 2- convert the string keys to a list of characters, each character will be a key and have its encrypted value
    keys = list(keys)

    # 3- create another list that's going to have the values for our keys. Shuffling is the core of this algorithm
    values = keys.copy()
    random.shuffle(values)
    print(keys)
    print(values)

    # 4- create a dictionary of {keys:values}
    cipher_map = dict(zip(keys, values))
    # print(cipher_map)
    new_word = ''
    for letter in word:
        new_word += cipher_map.get(letter)

    print('encrypted:', new_word, '\n\n')
    # print(cipher_map)
    return new_word, cipher_map


def decrypt(word, dictionary):
    """
    for each letter in our word, go to our dictionary look for the letter in our keys, and add its
    VALUE to reveal. The trick here is creating a new dictionary where the keys in the old dictionary are now values,
    and the values in the old dictionary are now keys in the new dictionary.
    """

    print('Decrypting:', word)
    # new_dict = dict()
    # for k, v in dictionary.items():
    #   new_dict.update({v: k})
    new_dict = {v: k for k, v in dictionary.items()}        # dictionary compr. method of writing the past 3 lines
    print(list(new_dict.keys()))
    print(list(new_dict.values()))

    reveal = ""

    for letter in word:
        reveal += new_dict.get(letter)
    print('decrypted:', reveal, '\n\n')
    return reveal


if __name__ == '__main__':
    password = input('Enter a word: ')
    print(f'Password: {password}')
    encrypted_word, dictionary = encrypt(password)
    print('\n')
    secret = decrypt(encrypted_word, dictionary)

