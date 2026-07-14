# Wordle Clone

This is a Wordle clone that I am working on to act as a test puzzle for a Wordle solver I am also working on that implementes a recurssive Beysian filter function to optimize guesses and solve the puzzle in the shortest number of moves.

## How to Start

Start the game with 

```python play.py```

The application will select a five letter word from its library in wordle/words.py

The user will be prompted to guess the word and receive back classic wordle style feedback showing which letters part of the word (yellow), which letters are part of the word and in the correct position (green), or are not part of the word at all (gray)

### Example
Guess the 5-letter word. You have 6 attempts. <BR>
[6 left] guess: laser<BR>
<span style="background-color: #787c7e; color: white; padding: 5px; font-weight: bold;">L</span>
<span style="background-color: #6aaa64; color: white; padding: 5px; font-weight: bold;">A</span>
<span style="background-color: #c9b458; color: white; padding: 5px; font-weight: bold;">S</span>
<span style="background-color: #6aaa64; color: white; padding: 5px; font-weight: bold;">E</span>
<span style="background-color: #787c7e; color: white; padding: 5px; font-weight: bold;">R</span>

## Future Work

1. Expand the library of possible words
1. Create and validate a direct programatic access by an AI solver
1. CLI Option for running the game with a pre-selected word