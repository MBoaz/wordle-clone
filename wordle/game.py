"""Core Wordle game logic, decoupled from any I/O so a solver can drive it directly."""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .words import WORD_LIST

WORD_LENGTH = 5
VALID_WORDS = frozenset(w.lower() for w in WORD_LIST if len(w) == WORD_LENGTH)


class LetterStatus(Enum):
    CORRECT = "correct"  # right letter, right position
    PRESENT = "present"  # right letter, wrong position
    ABSENT = "absent"    # letter not in the word (or already accounted for)


class InvalidGuessError(ValueError):
    pass


@dataclass(frozen=True)
class GuessResult:
    guess: str
    statuses: tuple

    @property
    def is_win(self) -> bool:
        return all(s == LetterStatus.CORRECT for s in self.statuses)

    def as_string(self) -> str:
        symbols = {LetterStatus.CORRECT: "G", LetterStatus.PRESENT: "Y", LetterStatus.ABSENT: "X"}
        return "".join(symbols[s] for s in self.statuses)


class WordleGame:
    """A single Wordle round.

    Feedback is returned from guess(), never printed, so this can be driven
    interactively (see cli.py) or programmatically by a solver.
    """

    def __init__(
        self,
        answer: Optional[str] = None,
        max_attempts: int = 6,
        word_pool: Optional[frozenset] = None,
    ):
        self._word_pool = word_pool if word_pool is not None else VALID_WORDS
        if answer is None:
            answer = random.choice(tuple(self._word_pool))
        answer = answer.lower()
        if len(answer) != WORD_LENGTH:
            raise ValueError(f"answer must be {WORD_LENGTH} letters, got {answer!r}")
        self.answer = answer
        self.max_attempts = max_attempts
        self.history: list = []

    @property
    def attempts_used(self) -> int:
        return len(self.history)

    @property
    def attempts_left(self) -> int:
        return self.max_attempts - self.attempts_used

    @property
    def is_won(self) -> bool:
        return bool(self.history) and self.history[-1].is_win

    @property
    def is_over(self) -> bool:
        return self.is_won or self.attempts_used >= self.max_attempts

    def guess(self, word: str) -> GuessResult:
        if self.is_over:
            raise InvalidGuessError("game is already over")
        word = word.lower()
        if len(word) != WORD_LENGTH:
            raise InvalidGuessError(f"guess must be {WORD_LENGTH} letters, got {word!r}")
        if word not in self._word_pool:
            raise InvalidGuessError(f"{word!r} is not in the word list")

        result = GuessResult(guess=word, statuses=self._score(word))
        self.history.append(result)
        return result

    def _score(self, guess: str) -> tuple:
        answer_chars = list(self.answer)
        statuses = [LetterStatus.ABSENT] * WORD_LENGTH

        # Pass 1: exact position matches, consuming those answer letters first.
        for i, ch in enumerate(guess):
            if ch == answer_chars[i]:
                statuses[i] = LetterStatus.CORRECT
                answer_chars[i] = None

        # Pass 2: remaining letters score PRESENT, consumed left-to-right so a
        # duplicate guess letter is never credited more times than it occurs
        # in the answer.
        for i, ch in enumerate(guess):
            if statuses[i] == LetterStatus.CORRECT:
                continue
            if ch in answer_chars:
                statuses[i] = LetterStatus.PRESENT
                answer_chars[answer_chars.index(ch)] = None

        return tuple(statuses)
