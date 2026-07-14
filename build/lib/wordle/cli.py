"""Interactive command-line Wordle."""
from __future__ import annotations

import sys

from wordle.game import GuessResult, InvalidGuessError, LetterStatus, WordleGame

_COLOR = {
    LetterStatus.CORRECT: "\033[42m\033[30m",
    LetterStatus.PRESENT: "\033[43m\033[30m",
    LetterStatus.ABSENT: "\033[100m\033[37m",
}
_RESET = "\033[0m"


def render(result: GuessResult) -> str:
    return "".join(f"{_COLOR[s]} {ch.upper()} {_RESET}" for ch, s in zip(result.guess, result.statuses))


def main() -> int:
    game = WordleGame()
    print(f"Guess the 5-letter word. You have {game.max_attempts} attempts.")

    while not game.is_over:
        raw = input(f"[{game.attempts_left} left] guess: ").strip()
        try:
            result = game.guess(raw)
        except InvalidGuessError as exc:
            print(f"  {exc}")
            continue
        print("  " + render(result))

    if game.is_won:
        print(f"Solved in {game.attempts_used} guesses! The word was {game.answer.upper()}.")
        return 0
    print(f"Out of attempts. The word was {game.answer.upper()}.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
