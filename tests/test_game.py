import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wordle.game import InvalidGuessError, LetterStatus as S, WordleGame


class WordleGameTests(unittest.TestCase):
    def test_exact_match_is_correct(self):
        game = WordleGame(answer="apple")
        result = game.guess("apple")
        self.assertEqual(result.statuses, (S.CORRECT,) * 5)
        self.assertTrue(result.is_win)
        self.assertTrue(game.is_won)

    def test_no_overlap_is_absent(self):
        game = WordleGame(answer="apple")
        result = game.guess("truck")
        self.assertEqual(result.statuses, (S.ABSENT,) * 5)

    def test_present_but_wrong_position(self):
        game = WordleGame(answer="apple", word_pool=frozenset({"apple", "plead"}))
        result = game.guess("plead")
        self.assertEqual(
            result.statuses,
            (S.PRESENT, S.PRESENT, S.PRESENT, S.PRESENT, S.ABSENT),
        )

    def test_duplicate_guess_letter_single_in_answer(self):
        # answer "chase" has one 'a'; guess "arena" has two -> only one is credited
        game = WordleGame(answer="chase")
        result = game.guess("arena")
        self.assertEqual(
            result.statuses,
            (S.PRESENT, S.ABSENT, S.PRESENT, S.ABSENT, S.ABSENT),
        )

    def test_correct_duplicate_then_extra_marked_present_not_double_correct(self):
        # answer "algae" has two 'a's (idx 0 and 3)
        game = WordleGame(answer="algae", word_pool=frozenset({"algae", "aroma"}))
        result = game.guess("aroma")
        self.assertEqual(result.statuses[0], S.CORRECT)
        self.assertEqual(result.statuses[1], S.ABSENT)
        self.assertEqual(result.statuses[2], S.ABSENT)
        self.assertEqual(result.statuses[3], S.ABSENT)
        self.assertEqual(result.statuses[4], S.PRESENT)

    def test_invalid_length_raises(self):
        game = WordleGame(answer="apple")
        with self.assertRaises(InvalidGuessError):
            game.guess("ab")

    def test_word_not_in_pool_raises(self):
        game = WordleGame(answer="apple", word_pool=frozenset({"apple", "grape"}))
        with self.assertRaises(InvalidGuessError):
            game.guess("zzzzz")

    def test_game_ends_after_max_attempts(self):
        game = WordleGame(answer="apple", max_attempts=2, word_pool=frozenset({"apple", "grape"}))
        game.guess("grape")
        self.assertFalse(game.is_over)
        game.guess("grape")
        self.assertTrue(game.is_over)
        self.assertFalse(game.is_won)

    def test_guess_after_game_over_raises(self):
        game = WordleGame(answer="apple", max_attempts=1)
        game.guess("apple")
        with self.assertRaises(InvalidGuessError):
            game.guess("apple")

    def test_as_string(self):
        game = WordleGame(answer="apple")
        result = game.guess("apple")
        self.assertEqual(result.as_string(), "GGGGG")


if __name__ == "__main__":
    unittest.main()
