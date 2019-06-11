import sys
import re
import argparse
from collections import Counter
import time


def get_command_line_input():
    """Return an argparse.Namespace from command line arguments."""
    parser = argparse.ArgumentParser(
        description=('Outputs a list of all words in the choosen file with the'
                     ' in the order of most common words to least common.'
                     ))
    parser.add_argument('filename', help='Filename for the input text')
    parser.add_argument('--filter', help='(optional) Filename for the filter')
    return parser.parse_args()


def process_file(filename, word_filter):
    """Passes a dictionary with the words and their frequency count to print_result.

    Input:
    filename (str): filename of textfile containing the text from which the
                    list of words ordered by frequency should be generated
    word_filter (str): Filename of the file containing the words to be filtered
                       out. Can be an empty string in which case the filter is
                       not applied
    """
    encoding = 'utf-8'
    while True:
        try:
            with open(filename, encoding=encoding) as file:
                if word_filter:
                    print_result(filter_words(word_filter, Counter(generate_words(generate_lines(file)))))
                else:
                    print_result(Counter(generate_words(generate_lines(file))))
        except (UnicodeDecodeError, LookupError):
            encoding = input(f'Decoding error: {encoding} can\'t decode.'
                              ' Please specify encoding: ')
        except:
            print('Unexpected error:', sys.exc_info()[0])
            break
        else:
            break



def generate_lines(file):
    """Returns the lines of the file, removing all lines consisting of symbols.

    Parameters:
    file (fileobject): The file passed to process_file()

    Output:
    list: A list of each line as a string with all lines consisting of only
          symbols removed.
    """
    symbol_lines = re.compile(r'^[\d\W]+$')
    return [line for line in file.readlines()
            if not symbol_lines.search(line)]


def generate_words(lines):
    """Returns a list of words.

    Parameters:
    lines (list): A list of each line as a string

    Output:
    list: A list of words with all symbols removed
    """
    symbols = re.compile(r'\W')
    return [word.lower() for line in lines for
            word in symbols.sub(' ', line).split()]


def filter_words(filename, wordlist):
    """Returns a list of words where each word in wordlist is removed.

    Parameters:
    filename (str): The filname of the words that should be removed. One word
                    per line.
    wordlist (list): A list of words

    Output:
    dictonary: word as key and the frequency count as value where every word in
               the file is removed.
    """
    try:
        with open(filename) as file:
            filter_words = {word.rstrip() for word in file.readlines()}
            return {w: c for w, c in wordlist.items() if w not in filter_words}
    except IOError as e:
        print('IOError: ', e)
    except:
        print('Unexpected error: ', sys.exc_info()[0])


def print_result(d):
    """Prints the words sorted by frequency in decreasing order.

    Parameters:
    d (dict): A dictionary with the keys being words and the values the
              frequency count.

    Prints:
    One word per line starting with the most frequent word.
    """
    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        print(k)


if __name__ == '__main__':
    a = get_command_line_input()
    process_file(a.filename, a.filter if a.filter else '')
