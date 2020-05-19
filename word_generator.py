"""Word generator using Markov chain algorithm."""
import sys
import random
from string import ascii_lowercase as letters
from collections import defaultdict
# -------------------------------------------------------
# USER INPUT:

# dictionary file to compare:
DICT_FILE = 'dictionary.txt'

# number of words to generate:
NUM_WORDS = 5

# size of generated words:
MIN_SIZE = 4
MAX_SIZE = 12

# END OF USER INPUT - DO NOT EDIT BELOW THIS LINE!
# -------------------------------------------------------


def main():
    """Run other functions."""
    word_list = load_dict(DICT_FILE)

    # create suffix maps for keys length from 1 to 3:
    suffix_maps = [train_chain(word_list, i) for i in range(1, 5)]

    # generate words:
    gen_words = generate_word(suffix_maps, NUM_WORDS)

    # display:
    print("Generated words:", *gen_words, sep="\n\t")


def load_dict(filename: str) -> list:
    """Return list of words from dictionary file."""
    try:
        with open(filename) as in_file:
            word_list = in_file.read().lower().split()
            return word_list
    except IOError:
        print(f"File {filename} not found! Terminating...", file=sys.stderr)
        sys.exit(1)


def train_chain(word_list: list, key_length: int) -> defaultdict:
    """Load list & use dictionary to map letters to letter.

    :param word_list: list of words to train
    :param key_length: size of key
    """
    dict_keys = defaultdict(list)

    for word in word_list:

        limit = len(word) - key_length
        if limit <= 0:  # means word is too small
            continue

        # adds trailing letter for given letters
        for i in range(limit):
            key = word[i:key_length + i]
            dict_keys[key].append(word[key_length + i])

    return dict_keys


def generate_word(suffix_maps: list, amount: int) -> list:
    """Generate given amount of words using suffix map."""
    # init empty list
    gen_words = []

    for _ in range(amount):
        # init word with first letter and it's size:
        word = random.choice(letters)
        size = random.randint(MIN_SIZE, MAX_SIZE)

        for _ in range(1, size):
            if len(word) < 5:
                map_list = (suffix_maps[len(word) - 1]).get(word)
            else:
                new_word = word[-4:]
                map_list = (suffix_maps[3]).get(new_word)

            # to avoid case when no values for given key found:
            try:
                word = word + random.choice(map_list)
            except TypeError:
                size += 1

        gen_words.append(word)

    return gen_words


if __name__ == '__main__':
    main()
