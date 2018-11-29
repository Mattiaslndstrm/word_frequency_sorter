import sys
import re
import argparse


def get_command_line_input():
    parser = argparse.ArgumentParser(
        description=('Outputs a list of all words in the choosen file with the'
                     ' in the order of most common words to least common.'
                     ))
    parser.add_argument('filename', help='Filename for the input text')
    parser.add_argument('--filter', help='(optional) Filename for the filter')

    return parser.parse_args()


def process_file(filename, filter):
    with open(filename, encoding='utf-8') as file:
        if filter:
            print_result(filter_words(filter, generate_count(generate_words(generate_lines(file)))))
        else:
            print_result(generate_count(generate_words(generate_lines(file))))


def generate_lines(file):
    symbol_lines = re.compile(r'^[\d\W]+$')
    return [line for line in file.readlines()
            if not symbol_lines.search(line)]


def generate_words(lines):
    symbols = re.compile(r'\W')
    return [word.lower() for line in lines for
            word in symbols.sub(' ', line).split()]


def generate_count(words):
    count = {}
    for word in words:
        count.setdefault(word, 0)
        count[word] += 1
    return count


def filter_words(filename, wordlist):
    with open(filename) as file:
        filter_words = [word.rstrip() for word in file.readlines()]
        return {w: c for w, c in wordlist.items() if w not in filter_words}


def print_result(d):
    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        print(k)


if __name__ == '__main__':
    a = get_command_line_input()
    process_file(a.filename, a.filter if a.filter else '')
