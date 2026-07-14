# Wordle Clone

This is a Wordle clone I'm working on to act as a test puzzle for a Wordle solver I'm also working on ([wordle-ai](../wordle-ai)) that implements a Bayesian filter to optimize guesses and solve the puzzle in the shortest number of moves.

The game logic is deliberately I/O-free so it can be driven two ways: a human typing guesses at a terminal, or a solver calling it directly as a library. `wordle-ai` now does the latter — it installs this project as an editable package and imports `WordleGame`/`score_guess` straight from `wordle`.

## How to Start

Start the game with

```python play.py```

The application will select a five letter word at random from its library in `wordle/words.py`.

The user will be prompted to guess the word and receive back classic Wordle-style feedback showing which letters are part of the word (yellow), which letters are part of the word and in the correct position (green), or are not part of the word at all (gray).

### Example
Guess the 5-letter word. You have 6 attempts. <BR>
[6 left] guess: laser<BR>
<span style="background-color: #787c7e; color: white; padding: 5px; font-weight: bold;">L</span>
<span style="background-color: #6aaa64; color: white; padding: 5px; font-weight: bold;">A</span>
<span style="background-color: #c9b458; color: white; padding: 5px; font-weight: bold;">S</span>
<span style="background-color: #6aaa64; color: white; padding: 5px; font-weight: bold;">E</span>
<span style="background-color: #787c7e; color: white; padding: 5px; font-weight: bold;">R</span>

## Code Overview

Everything lives under `wordle/`:

- **`words.py`** — `WORD_LIST`, a plain list of ~550 common 5-letter English words. This is the raw source data; nothing else in the package edits it.

- **`game.py`** — the whole game engine:
  - `LetterStatus` — an enum for the three feedback states: `CORRECT` (green), `PRESENT` (yellow), `ABSENT` (gray).
  - `VALID_WORDS` — `WORD_LIST` deduplicated, lowercased, and frozen into a `frozenset`. This is the default word pool for both picking an answer and validating guesses.
  - `score_guess(guess, answer)` — the pure scoring function. Given any two 5-letter strings it returns a tuple of `LetterStatus`, one per letter position. It scores in two passes: first it marks exact-position matches and removes those letters from the answer's pool, then it marks remaining guess letters as `PRESENT` if they're still unclaimed in what's left of the answer. That two-pass, consume-as-you-go order is what makes duplicate letters score correctly (e.g. guessing `ARENA` against an answer with a single `A` only credits one of the `A`s). Because it takes an explicit `answer` rather than reading game state, a solver can call it directly to simulate "what feedback would this guess produce if the answer were X?" without playing a real round.
  - `GuessResult` — an immutable record of one guess: the word guessed and its `statuses` tuple. `is_win` checks if every position is `CORRECT`; `as_string()` renders the pattern as a compact `G`/`Y`/`X` string (e.g. `"GYXXG"`).
  - `InvalidGuessError` — raised for a guess of the wrong length, a guess outside the word pool, or a guess submitted after the game is already over.
  - `WordleGame` — the stateful game session. Constructed with an optional fixed `answer` (random from `VALID_WORDS` if omitted), a `max_attempts` limit (default 6), and an optional custom `word_pool`. `guess(word)` validates the input, scores it via `score_guess`, appends a `GuessResult` to `history`, and returns that result. `attempts_left`, `is_won`, and `is_over` derive from `history` rather than tracked separately, so there's a single source of truth for game state.

- **`cli.py`** — the interactive terminal front-end. Wraps a `WordleGame` in a loop: prompt for a guess, catch `InvalidGuessError` and re-prompt, otherwise render the `GuessResult` as colored terminal tiles. This is the only place in the package that does any printing or reads `input()`.

- **`__init__.py`** — the public surface re-exported for consumers: `WordleGame`, `GuessResult`, `LetterStatus`, `InvalidGuessError`, `score_guess`, and `VALID_WORDS`.

`play.py` at the repo root is just a thin entry point that calls `wordle.cli.main()`.

## Programmatic Interface

The package is pip-installable (`pyproject.toml` at the repo root) so another project can depend on it without copying code. From a sibling project:

```bash
pip install -e ../wordle-clone
```

Then drive a round directly:

```python
from wordle import WordleGame, InvalidGuessError

game = WordleGame(answer="chase")  # omit answer to pick one at random
result = game.guess("place")
print(result.as_string())  # e.g. "YYYXG"
```

`wordle-ai`'s solver goes one step further and calls `score_guess(guess, candidate)` directly (without a `WordleGame` instance) to simulate feedback against every word it's still considering, which is how it narrows down the answer.

## Future Work

1. Expand the library of possible words
2. CLI option for running the game with a pre-selected word
