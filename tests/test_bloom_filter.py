from unittest import TestCase
from bloom_filter.bloom_filter import BloomFilter

class TestBloomFilter(TestCase):
    def test_inserted_element(self):
        bf = BloomFilter(1000, 2)
        bf.add('test')
        bf.add('another')

        assert 'test' in bf
        assert 'another' in bf


    def test_inserteds_element_build_with_target_fp(self):
        bf = BloomFilter.build_for_target_fp(1000, .01)
        bf.add('word')

        assert 'word' in bf


    def test_inserted_element_build_with_target_fp(self):
        bf = BloomFilter.build_for_target_fp(10000, .01)
        bf.add('word')

        assert 'some_other_word' not in bf


    def test_two_fp(self):
        with self.assertRaises(ValueError):
            bf = BloomFilter.build_for_target_fp(10000, 0.0)


    def test_zero_fp(self):
        with self.assertRaises(ValueError):
            bf = BloomFilter.build_for_target_fp(10000, 2.0)
