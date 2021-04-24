> OverworldLord

# Rogue Ophidian

This game was created to be similar to the 1976 arcade game Blockade. It is meant to be a clone of the game 'Snake,' and has several rules.
## Prerequisites
*This game requires python3.7 or greater to work properly*. Additional prerequisites are placed within the 'requirements.txt' file, which can be accessed by using the following command from the same directory:
```
python -m pip install -r requirements.txt
```
or by using the rogue-env virtual environment (from the same directory as snake.py, unzip rogue-env and use the following command:
```
source rogue-ophidian-env/bin/activate
```
From there, the game can be run by using the following command:
```
python snake.py
```
## External Credits
 * This game was written in [Python](http://www.python.org) using [Pygame](http://www.pygame.org).
 * This game was coded by OverworldLord. All code within this program was developed from scratch.
 * All music and sound effects in this game were created by OverworldLord using [Ableton Live 11](https://www.ableton.com). The MIDI used to create both the soundtrack and sound effects are completely original.
 * This game makes use of art from [Westeh!](http://www.deviantart.com/twowestex), an artist who was inspired by my game and wanted to help in its development. He has given me permission to use his art in my game, and has made the art specifically to be used in my game.
 * Special thanks to MadMasterGamer for being the lead game tester and providing ['quality' feedback](#reported-bugs).
 * This game makes use of [pylint](https://www.pylint.org/) to conform to [PEP-8](https://www.python.org/dev/peps/pep-0008).

## Features
This game makes use of graphics in order to display the game 'Rogue Ophidian,' a snake clone (see [bugs](#reported-bugs) for unconfirmed issues involving graphical glitches).
 * In this game, the player controls the snake (and makes selections on the menus) using the keyboard.
	 * The player can move the snake's head up, down, left, or right by using either WASD or the arrow keys. The snake acts as a train.
 * The objective of the game is to score as many points as possible.
	 * Every three seconds, the player's score increases slightly.
	 * When the player eats food, their score increases and the snake gains 'fat.'
		 * Their score and fat increases more if they eat food while they still have fat, and if they eat food whilst they have a higher score.
		 * Fat is burned by adding a new segment to the end of the snake. If the player has fat, they will burn it until they run out.
 * The player's snake dies when the snake touches itself, a boundary, or a hazard (see [bugs](#reported-bugs) for information pertaining to an unconfirmed and unintentional hazard).
	* The boundary is the limit of the game board.
* Food is added/moved when the player eats food. If the snake is long enough, multiple food might even spawn in the board!
* This game has a main menu, leaderboard, and credits screen in addition to the game itself.
* The player has only one life; if they lose their life, they are brought to the leaderboard to see the top five scores they've gotten. From there, they may choose to play again.
* This game uses music and sound effects both in the menus and in the game itself. Volume can be increased and decreased from within the menus.
* While unlikely, it is possible to win the game by getting long enough and becoming (almost) as big as the board.


## Reported Bugs
**It should be noted that I have been unable to reproduce any of the bugs mentioned in this section.** However, based on reports these glitches appear to happen randomly depending on several factors, including:

#### User's Operating System
In Windows, the glitch reports are fairly consistent, while Mac has less reported occurrences and Linux has had no reported occurrences thus far. Allow me to remind the reader that this game is best played on the *Linux* Operating System, and other systems are not supported.
#### Version of Python
The game requires python 7 or above, and is expected to crash if using an earlier version due to a confirmed error with [pygame.mixer](http://www.pygame.org/docs/ref/mixer.html). If the game is not crashing when the user plays with an outdated version, other bugs could hypothetically result. I used python 3.7.5 and python 3.7.9 when developing this game, users may be using different versions.
#### Time of Day
More instances of these glitches appear to happen between 11pm-4am. There may be an issue with [pygame.time](http://www.pygame.org/docs/ref/time.html); however, I have not found any errors after my own exhaustive testing.
#### Other Bugs
When these bugs are reported, they are commonly reported with other bugs simultaneously. This leads me to believe that **some (if not all) reports are fake**; I am confident that my code isn't generating several errors at the same time.
#### Player Score
Testers claim that bugs will start occurring when their snake has 'enough fat' (food). This is likely the placebo effect, since my score function is fairly straightforward and shouldn't affect gameplay.

### Bugs
With that out of the way, here are the bugs that have been reported (**unconfirmed and as of yet not reproducible**) in order of importance (increasing from top to bottom):
- The snake's body may fail to remain within the lines generated by the display
- The grid (which should be invisible) can be seen
- The background of the game slightly changes color
- The food may significantly change color
- Sound may stutter or otherwise become 'corrupted' to the point where it sounds like a different audio file entirely
- Some pixels may randomly (but temporarily) 'disappear,' regardless of their initial type
- The snake's body may randomly change color, but trends around orange
- The game may speed up as the player collects more food
- Before being taken to the leaderboard, the player is shown a corrupted 'image,' which players report as being disturbed by
- A 'moving hazard' appears on the screen and 'chases' the players; if the hazard 'attacks' the player then they are immediately brought to a fail state. The hazard appears to get faster as the player eats more food, and moves very quickly diagonally (but slowly in the X or Y direction)

