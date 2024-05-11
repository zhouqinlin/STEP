import unittest
from anagram1 import find_anagram, read_file


class TestFindAnagram(unittest.TestCase):

    def setUp(self):
        self.dictionary = read_file("words.txt")

    def test_find_anagram_basic(self):
        # 簡単なケース
        dictionary = ["ape", "apple", "pale", "pealp"]
        self.assertEqual(find_anagram("leap", dictionary), ["pale"])

    def test_find_anagram_multiple_anagrams(self):
        # anagramが複数ある場合
        dictionary = ["ape", "apple", "leap", "pale", "peal", "plea"]
        self.assertEqual(
            find_anagram("leap", dictionary), ["leap", "pale", "peal", "plea"]
        )

    def test_find_anagram_no_anagram(self):
        # anagramが見つからない場合
        dictionary = ["ape", "apple", "pealp"]
        self.assertEqual(find_anagram("leap", dictionary), [])

    def test_find_anagram_short_input(self):
        # 与えられた単語がとても短い場合
        self.assertEqual(find_anagram("p", self.dictionary), ["p"])

    def test_find_anagram_long_input(self):
        # 与えられた単語がとても長い場合
        dictionary = ["antidisestablishmentarianism", "anti", "aaaab"]
        self.assertEqual(
            find_anagram("antidisestablishmentarianism", dictionary),
            ["antidisestablishmentarianism"],
        )

    def test_find_anagram_empty_input(self):
        # 空の文字列が与えられた時
        dictionary = ["ape", "apple", "pale"]
        self.assertEqual(find_anagram("", dictionary), [])


if __name__ == "__main__":
    unittest.main()
