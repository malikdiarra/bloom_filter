import argparse
import random
import string
import sys

from .bloom_filter import BloomFilter


def spellchecker():

    parser = argparse.ArgumentParser(description='Start a small spellchecker')
    parser.add_argument('-d', '--dictionary', required=True,
                        help='Path to the word dictionary to use for spell checking',
                        metavar='/path/to/word/list')
    parser.add_argument('--fp', type=float, required=False, default=0.01,
                        help='False positive rate between 0.0 and 1.0', metavar='0.01')
    args = parser.parse_args()

    print('loading dictionary...')
    dictionary = set()
    with open(args.dictionary) as f:
        for word in f:
            dictionary.add(word.strip().lower())

    n = len(dictionary)
    bloom_filter = BloomFilter.build_for_target_fp(n, args.fp)
    for word in dictionary:
        bloom_filter.add(word)

    print('Ready!')
    for line in sys.stdin:
        words = line.split(' ')
        correction = []
        for word in words:
            c = ' '
            if word.strip().lower() not in bloom_filter:
                c = '^'
            correction.append(c * len(word.strip()))
        print(' '.join(correction))


def check():

    parser = argparse.ArgumentParser(description='Verify bloom filter performance by generating random words')
    parser.add_argument('-d', '--dictionary', required=True,
                        help='Path to the word dictionary to use for spell checking',
                        metavar='/path/to/word/list')
    parser.add_argument('--word-length', type=int, required=False, default=5,
                        help='length of the random words generated')
    parser.add_argument('--samples', type=int, required=False, default=10000,
                        help='number of random words sampled')
    parser.add_argument('--fp', type=float, required=False, default=0.01,
                        help='False positive rate between 0.0 and 1.0', metavar='0.01')
    args = parser.parse_args()

    dictionary = set()
    with open(args.dictionary) as f:
        for word in f:
            dictionary.add(word.strip().lower())

    n = len(dictionary)
    bloom_filter = BloomFilter.build_for_target_fp(n, args.fp)

    for word in dictionary:
        bloom_filter.add(word)

    def generate_words(samples, word_length):
        for i in range(samples):
             yield ''.join([random.choice(string.ascii_lowercase) for _ in range(word_length)])

    print(f"Generating {args.samples} words of length {args.word_length}")
    fp = sum(word in bloom_filter and word not in dictionary
             for word in generate_words(args.samples, args.word_length))

    print(f"False positive rate {(fp / args.samples) * 100:.2f} %, k: {bloom_filter.k}, m/n: {bloom_filter.m/n:.2f}")
