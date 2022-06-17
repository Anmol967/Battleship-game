# Built a human vs AI game of Battleship using object oriented programming from scratch !

**Gameplay**:

The game is designed with the idea that there will be a 10x10 grid for both the player as well as
the AI the player shall be playing against. Each player has to set a total of 5 ships, these ships
are:

&emsp;● One Carrier (Occupy five blocks)

&emsp;● One Battleships (Occupy 4 blocks)

&emsp;● Two Cruiser’s (Occupy three blocks)

&emsp;● One Submarine (Occupy 2 blocks)

In our game, the placement of the human’s battleship can be selected by the player and the
placement of the AI’s battleships are random.
The rules of the game are:

&emsp;● The ships can be placed horizontally or vertically not diagonally and they must be placed
within the coordinates of the board.

&emsp;● The ships can touch each other but they are not allowed to occupy the same gridspace.

&emsp;● The position of the ships cannot be changed once the game begins.

The objective of the game is to try and sink all of the other player’s ships before they sink all of
yours. You try to hit them by calling out the coordinates of one of the squares on the board.
Players alternate turns calling out coordinates on the board. Once you have hit all the coordinates
of a particular ship on the opponent’s board, that ship is considered sunk.

**Algorithm:**

The algorithm employed to play this game with AI is a combination of the Knowledge and
Search units that were studied in our course.

The main “intelligence” here uses the fact that if the AI randomly scores a hit, then the other
parts of the battleship should be nearby and therefore the AI shouldn’t guess cells that are further
away from the first hit location (of a particular ship).

&emsp;● The decision (i.e., the guess) which the AI will make will either be random(denoted by
hit_var = 0) or intelligent(denoted by hit_var = 1) i.e., using some problem specific
knowledge.

&emsp;● When the game first starts, hit_var is 0 so the AI player guesses randomly and as soon as
it scores a hit, the value of hit_var becomes 1, implying that now the AI will have to
make decisions using some knowledge available. The general knowledge (in the game of
Battleship) is that battleships can be arranged in only horizontal or vertical manner (not
diagonally) or any other manner. Thus, the AI will have to decide between the horizontal
and vertical direction. This decision is made not on the basis of the number of unexplored
(i.e., not guessed) consecutive cells in a direction, but on the basis of how many ships (of
different sizes) can be arranged in that direction.

&emsp;● If the number of consecutive unexplored cells in one horizontal direction is greater, but
an equal number of ships can be arranged in both the vertical and horizontal direction
then both have equal probability of getting selected and in that case the AI will choose
any one of them randomly. The AI has to choose between the up and down directions (or
left and right in case of horizontal direction). This will again be based upon the number
of ships that can be fit in the up vs the down direction and in case of a tie, any one is
chosen randomly.

&emsp;● If the AI makes a move in a direction and it doesn’t score a hit then it has to go in the
opposite direction (but in the same line), because battleships can't be arranged in a
discontinuous manner. If the AI scores a miss again, it will have to change its line
altogether (from vertical to say horizontal or vice versa). If it scores a hit in a particular
direction, then it will continue in that direction provided there are unexplored cells, else it
will again reverse its direction.

&emsp;● If the AI guesses a cell, it can’t take a guess at it again. This process repeats itself for
each ship, so if the AI sinks/destroys a ship completely then the value of hit_var again
changes to 0 and it goes back to randomly guessing cells.

This is a human vs the computer (AI) game and each player will get an equal number of moves
(which depends upon who sinks all the ships first). If one of the players has played one move
less then the player will get one last move to try and complete the game, if yes then the game
ends in a tie, if no the other player wins.
