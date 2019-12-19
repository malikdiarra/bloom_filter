import argparse
import math
import random
import hashlib


class BloomFilter():
    """
    A simple implemention of a bloom filter for string
    """
    def __init__(self, length, hashes):
        self.length = length
        self.hashes = hashes
        self.m = length
        self.k = hashes
        self.bits = [False] * self.length
        salts = (bytes([random.randint(0, 255)]) for _ in range(self.hashes))
        self.hash_functions = [self._build_hash_function(salt, length) for salt in salts]

    @staticmethod
    def build_for_target_fp(items_count, false_positive_rate):
        """
        Build a bloom filter appropriate for a target performance
        """
        if not 0.0 < false_positive_rate < 1:
            raise ValueError("False positive rate should be between 0.0 and 1.0")
        m = int(- 1.44 * math.log(false_positive_rate, 2) * items_count)
        k = int(- math.log(false_positive_rate, 2))
        return BloomFilter(m, k)

    @staticmethod
    def _build_hash_function(salt, length):
        """
        Build a hash function that returns a position in the array
        """
        def hash_to_position(digest):
            max_position = math.ceil(math.log(length, 2))
            position = 0
            for i in range(max_position // 8):
                position = position * 256 + digest[i]
            remaining_bits = (max_position % 8)
            position = position * (2 ** remaining_bits) + digest[max_position // 8] % (2 ** remaining_bits)
            # TODO: Find another way to avoid out of bound access to the array.
            # we take the remainder of the division by length to ensure we do not attempt
            # to access position outside of the array bound. Unfortunately this will prevent our hash from
            # being uniform.
            return position % length

        def hash_function(word):
            base_hash = hashlib.md5()
            base_hash.update(salt)
            base_hash.update(word.encode('utf-8'))
            digest = base_hash.digest()
            return hash_to_position(digest)

        return hash_function

    def add(self, word):
        for hash_function in self.hash_functions:
            position = hash_function(word)
            self.bits[position] = True

    def __contains__(self, word):
        for hash_function in self.hash_functions:
            position = hash_function(word)
            if not self.bits[position]:
                return False
        return True
