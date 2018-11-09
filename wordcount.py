import sys
import re


def process_file(filename):
    with open(filename, encoding='utf-8') as file:
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


def print_result(d):
    for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        print(v, k)


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Include filename')

    process_file(filename)
