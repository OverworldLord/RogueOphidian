"""
---------------------------------------------
Project: Snake Game
File Name: scene.py
Created by: OverworldLord
---------------------------------------------
This program implements the 'Snake' game,
       as described in README.md.
---------------------------------------------
PYLINT NOTES
Code style checked with pylint. Since pylint
has an issue with certain pygame elements
(doesn't understand keyboard input), pylint
was run using the following:

    pylint scene.py -d no-member

This resulted in a rating of 9.92/10. Pylint
also discourages object oriented program by
using a 'no-self-use' requirement; this can
be disabled by using the following command:
same line:

    pylint scene.py
                   -d no-member
                   -d no-self-use

Disabling this results in a rating of 10/10.
---------------------------------------------
This file defines all classes used for the
snake game. Classes are as follows:
INPUT - Enumerator used for valid types of
        input from the user.

RunStats - Holds stats about a game instance
           and has functions to output those
           stats.

DisplayUpdater - Handles anything related to
                 the screen's display both
                 in the game itself and in
                 a menu.

PlayerInput - Handles anything related to
              input from the player both in
              the game and in a menu.

GameRules - Handles the logic behind the
            game itself, including what
            should happen if the snake eats
            food, when they win or lose.

NonPlayerEntityHandler - Handles the logic
                         behind entities
                         within the game,
                         such as food or
                         other things with
                         a... peculiar AI.

AudioPlayer - Handles all audio in the game.
---------------------------------------------
"""

#Used in order to remove print syntax messages from pylint
from __future__ import print_function

#Used to get the current date
from datetime import date as dt

#Used for all random decisions
import random as rng

#Used for enumerator involving user input
from enum import Enum

#Used for file I/O
import json

#Used to check python version
import sys

#Used for display, sound, time, etc.
import pygame

class INPUT(Enum):
    """Enumerator, used for getting user input"""
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
    ENTER = 5
    BACKSPACE = 6
    SPACE = 7
    ESCAPE = 8
    C = 9

#Minimum and maximum game speed in ms
LOWER_BOUND, UPPER_BOUND = 100, 300

#Size of the entire grid
GRID_SIZE_X, GRID_SIZE_Y = 600, 600

#Additional size of the Y axis below the grid
MENU_SIZE = 50

#Size of every cell on the grid
CELL_SIZE = 24

#Amount of fat the snake should start with
STARTING_FAT = 0

#Whether or not to make things impossibly difficult
IMPOSSIBLE_MODE = False

#Number of demons to spawn
DEMONS_TO_SPAWN = 1 + 99*IMPOSSIBLE_MODE

#Game's current version, used for leaderboards
GAME_VERSION = "1.0 Release"

#Default audio volumes
MUSIC_VOLUME = .05
EFFECT_VOLUME = .1

class RunStats():
    """ Holds stats about the current run, to be output to a file """
    def __init__(self):
        self.run_date = dt.today()
        self.run_start = pygame.time.get_ticks()
        self.run_end = pygame.time.get_ticks()
    def output_to_file(self, score):
        """ Outputs data to the output file, separated by | """
        self.run_end = pygame.time.get_ticks()
        run_info = {'score': score,
                    'version': GAME_VERSION,
                    'date': str(self.run_date),
                    'time played': str((self.run_end - self.run_start)/1000)}
        try:
            with open('db/scores.json', 'r') as score_file:
                data = score_file.read()
            datalist = json.loads(data)
        except json.decoder.JSONDecodeError:
            datalist = []

        datalist.append(run_info)
        output = json.dumps(datalist)
        with open('db/scores.json', 'w') as score_file:
            score_file.write(output)
    def print_to_console(self, score):
        """ Outputs data to the console """
        print("Total Score:", score)
        print("Date of Run:", self.run_date)
        print("Total Time Played (Seconds):", int((self.run_end - self.run_start)/1000))

class DisplayUpdater():
    """ Holds functions that will be used to create and update the display """
    def __init__(self):
        """Load required visual assets"""
        #Load death image
        self.image = pygame.image.load("img/spookdestroy.jpg")
        self.image = pygame.transform.scale(self.image,
                                            (GRID_SIZE_X, GRID_SIZE_X + MENU_SIZE))
        #Load main menu
        self.main_menu = pygame.image.load("img/main_menu.jpg")
        self.main_menu = pygame.transform.scale(self.main_menu,
                                                (GRID_SIZE_X, GRID_SIZE_X + MENU_SIZE))
        #Load leaderboard
        self.leaderboard = pygame.image.load("img/leaderboard.jpg")
        self.leaderboard = pygame.transform.scale(self.leaderboard,
                                                  (GRID_SIZE_X, GRID_SIZE_X + MENU_SIZE))
        #Load credits
        self.credits = pygame.image.load("img/credits.jpg")
        self.credits = pygame.transform.scale(self.credits,
                                              (GRID_SIZE_X, GRID_SIZE_X + MENU_SIZE))
        #Load screen
        self.screen = pygame.display.set_mode((GRID_SIZE_X, GRID_SIZE_Y + MENU_SIZE))

        #Load all fonts
        spooky_font = pygame.font.SysFont('javanesetext', CELL_SIZE*4)
        self.spooky_font = spooky_font.render('NO ESCAPE', False, (0, 0, 0))
        self.score_font = pygame.font.Font('font/upheavtt.ttf', int(MENU_SIZE/2))
    def __del__(self):
        pygame.display.quit()
    def generate_display(self):
        """fills the display with nothing"""
        self.screen.fill((0, 0, 0))
        pygame.display.update()
    def show_image(self):
        """ displays an image to the screen """
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.spooky_font,
                         (GRID_SIZE_X - int(GRID_SIZE_X/1.2),
                          (GRID_SIZE_Y)))
        pygame.display.update()
    def show_main_menu(self):
        """ displays the main menu to the user """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.main_menu, (0, 0))
        pygame.display.update()
    def show_leaderboard(self):
        """ displays the leaderboard to the user """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.leaderboard, (0, 0))
        display_scores = []
        try:
            with open('db/scores.json', 'r') as score_file:
                data = score_file.read()
            datalist = json.loads(data)
            scores = []
            for elem in datalist:
                scores.append(elem['score'])
            scores.sort(reverse=True)
            if len(scores) >= 1:
                display_scores.append(self.score_font.render(str(scores[0]),
                                                             False, (139, 69, 19)))
            if len(scores) >= 2:
                display_scores.append(self.score_font.render(str(scores[1]),
                                                             False, (139, 69, 19)))
            if len(scores) >= 3:
                display_scores.append(self.score_font.render(str(scores[2]),
                                                             False, (139, 69, 19)))
            if len(scores) >= 4:
                display_scores.append(self.score_font.render(str(scores[3]),
                                                             False, (139, 69, 19)))
            if len(scores) >= 5:
                display_scores.append(self.score_font.render(str(scores[4]),
                                                             False, (139, 69, 19)))
        except json.decoder.JSONDecodeError:
            display_scores.append(self.score_font.render("Press ENTER",
                                                         False, (139, 69, 19)))
            display_scores.append(self.score_font.render("to play and",
                                                         False, (139, 69, 19)))
            display_scores.append(self.score_font.render("add a score",
                                                         False, (139, 69, 19)))

        for score_num, score in enumerate(display_scores):
            self.screen.blit(score,
                             (int(GRID_SIZE_X/1.8),
                              int((GRID_SIZE_Y + MENU_SIZE)/2.06) + GRID_SIZE_Y/8.9*score_num))
        pygame.display.update()
    def show_credits(self):
        """ Shows the user the credits screen """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.credits, (0, 0))
        pygame.display.update()
    def redraw(self, snake, food, demon, score):
        """redraws the display within the game from scratch"""

        #Fill the screen with the background
        self.screen.fill((int(len(snake) / 10),
                          min(100, rng.randrange(0, 1 + int(len(snake)/10))),
                          min(100, rng.randrange(0, 1 + int(len(snake)/10)))))
        #Draw the snake
        self.draw_snake(snake)
        #Draw the food
        self.draw_food(snake, food)
        #Draw the grid
        self.draw_grid(snake)
        #Draw the demon
        self.draw_demon(demon, snake)
        #Draw the score
        self.draw_score(score)

        pygame.display.update()
    def draw_snake(self, snake):
        """ Draws the snake to the screen"""
        #Prints every segment of the snake. Traditionally, this was in a nested for loop that
        #checked if a snake body segment was in every cell before printing it.
        #Previous complexity: GRID_SIZE_X*GRID_SIZE_X*len(snake)/CELL_SIZE^2
        #Current complexity:  len(snake)

        #Draw the snake if it is present
        for body_segment in snake:
            seg_x, seg_y = body_segment
            if len(snake) > 80 and rng.randrange(1, 100) == 50:
                rect = pygame.Rect(seg_x, seg_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, rng.randrange(120, 180), 0), rect)
            elif len(snake) > 80:
                rect = pygame.Rect(seg_x + min(rng.randrange(-2, 2)*(len(snake) - 80)/80, 10),
                                   seg_y + min(rng.randrange(-2, 2)*(len(snake) - 80)/80, 10),
                                   CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, rng.randrange(120, 180), 0), rect)
            else:
                rect = pygame.Rect(seg_x, seg_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 0), rect)
    def draw_food(self, snake, food):
        """" Draws food to the screen """
        #Prints food. Traditionally, this was in a nested for loop that
        #checked if food was in a cell before printing it.
        #Previous complexity: GRID_SIZE_X*GRID_SIZE_X*len(food)/CELL_SIZE^2
        #Current complexity:  len(food)

        #Get the position of the food
        for food_item in food:
            food_x, food_y = food_item
            if len(snake) > 100:
                rectsize = rng.randrange(0, int(CELL_SIZE/2))
                rect = pygame.Rect(food_x + rng.randrange(-5, 5),
                                   food_y + rng.randrange(-5, 5),
                                   CELL_SIZE - rectsize,
                                   CELL_SIZE - rectsize)
                pygame.draw.rect(self.screen,
                                 (rng.randrange(100, 255),
                                  rng.randrange(100, 255),
                                  rng.randrange(100, 255)),
                                 rect)
            else:
                rect = pygame.Rect(food_x, food_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
    def draw_grid(self, snake):
        """ Draws the grid to the screen """
        #Prints every cell; in actuality, prints a rectangle for every other x and y cell
        #that makes up the grid. This method is highly efficient compared to the previous
        #version, which printed every cell individually.
        #Previous number of prints:         (GRID_SIZE_X * GRID_SIZE_Y) / CELL_SIZE ^ 2
        #Current number of prints required: (GRID_SIZE_X + GRID_SIZE_Y) / (2 * CELL_SIZE)

        #Prints every column in the grid for cells
        for col in range(0, GRID_SIZE_X, 2*CELL_SIZE):
            rect = pygame.Rect(col, 0, CELL_SIZE, GRID_SIZE_Y)
            pygame.draw.rect(self.screen, (0, min(255, int(len(snake) / 2)), 0), rect, 1)
        #Prints every row in the grid for cells
        for row in range(0, GRID_SIZE_Y, 2*CELL_SIZE):
            rect = pygame.Rect(0, row, GRID_SIZE_X, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, min(255, int(len(snake) / 2)), 0), rect, 1)
    def draw_demon(self, demon, snake):
        """ Draws the demon to the screen, while modifying cells near the demon """
        #Corrupts cells near the demon. Previously, this checked all cells to see if the
        #demon was in their bounds.
        #Previous Complexity: GRID_SIZE_X*GRID_SIZE_X*len(food)/CELL_SIZE^2
        #Current Complexity: 4*4 = 16
        head_x, head_y = snake[0]
        for indiv_demon in demon:
            demon_x, demon_y = indiv_demon

            #Add chance to corrupt the cell if it is near the demon
            cell_under_demon_x = demon_x - (demon_x % CELL_SIZE)
            cell_under_demon_y = demon_y - (demon_y % CELL_SIZE)

            #Corrupt cells near the demon
            for cell_near_demon_x in range(-2*CELL_SIZE, 2*CELL_SIZE, CELL_SIZE):
                for cell_near_demon_y in range(-2*CELL_SIZE, 2*CELL_SIZE, CELL_SIZE):
                    if rng.randrange(0, 25) == 0:
                        rect = pygame.Rect(cell_near_demon_x + cell_under_demon_x,
                                           cell_near_demon_y + cell_under_demon_y,
                                           CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (0, 0, 0), rect)

            #Draws the demon. No change from previous iteration.

            #Draw the demon's outer and inner circles
            pygame.draw.circle(self.screen,
                               (rng.randrange(0, 255),
                                rng.randrange(0, 55),
                                rng.randrange(0, 55)),
                               indiv_demon, 25, 5)
            pygame.draw.circle(self.screen,
                               (rng.randrange(0, 255),
                                rng.randrange(0, 55),
                                rng.randrange(0, 55)),
                               indiv_demon, 20, 5)

            if abs(demon_x - head_x)/CELL_SIZE < 2 and abs(demon_y - head_y)/CELL_SIZE < 2:
                pygame.draw.circle(self.screen,
                                   (rng.randrange(0, 255),
                                    rng.randrange(0, 100),
                                    rng.randrange(0, 100)),
                                   (demon_x + rng.randrange(-7, 7),
                                    demon_y + rng.randrange(-7, 7)), 6)
    def draw_score(self, score):
        """Draws the user's current score to the screen in the menu"""
        rect = pygame.Rect(0, GRID_SIZE_Y, GRID_SIZE_X, MENU_SIZE)
        pygame.draw.rect(self.screen, (0, 0, 255), rect, int(MENU_SIZE/10))
        out_score = self.score_font.render(str(score), False, (255, 255, 255))
        self.screen.blit(out_score, (GRID_SIZE_X/2 - CELL_SIZE,
                                     (GRID_SIZE_Y + int(MENU_SIZE*1/10))))
class PlayerInput():
    """ Used in order to get and respond to player inputs/interactions """
    def __init__(self):
        pygame.event.get()
        self.pressed = pygame.key.get_pressed()
        if sys.version_info[1] < 7:
            print("  Please use python 3.7+. Using python 3.6 or below")
            print("  will cause the game to crash as soon as a sound")
            print("  effect plays!")
        else:
            print("Welcome to snake!")
    def clear_menu_input(self):
        """ Checks whether the player is not pressing anything """
        user_pressing_button = True
        while user_pressing_button:
            pygame.event.get()
            self.pressed = pygame.key.get_pressed()
            user_pressing_button = (self.pressed[pygame.K_RETURN] or self.pressed[pygame.K_SPACE] or
                                    self.pressed[pygame.K_BACKSPACE] or self.pressed[pygame.K_c] or
                                    self.pressed[pygame.K_ESCAPE] or self.pressed[pygame.K_z] or
                                    self.pressed[pygame.K_x])
    def get_menu_input(self, sound):
        """ Gets input from the main menu"""
        user_input = INPUT.NONE
        while user_input == INPUT.NONE:
            pygame.event.get()
            self.pressed = pygame.key.get_pressed()
            if self.pressed[pygame.K_RETURN]:
                user_input = INPUT.ENTER
            elif self.pressed[pygame.K_SPACE]:
                user_input = INPUT.SPACE
            elif self.pressed[pygame.K_BACKSPACE]:
                user_input = INPUT.BACKSPACE
            elif self.pressed[pygame.K_c]:
                user_input = INPUT.C
            elif self.pressed[pygame.K_ESCAPE]:
                user_input = INPUT.ESCAPE
            elif self.pressed[pygame.K_z]:
                sound.change_volume(False)
                self.clear_menu_input()
            elif self.pressed[pygame.K_x]:
                sound.change_volume(True)
                self.clear_menu_input()
        self.clear_menu_input()
        if user_input != INPUT.NONE:
            sound.play_menu_select()
        return user_input
    def get_movement(self):
        """gets a movement signal from the player"""
        pygame.event.get()
        self.pressed = pygame.key.get_pressed()

        user_input = INPUT.NONE
        if self.pressed[pygame.K_a] or self.pressed[pygame.K_LEFT]:
            user_input = INPUT.LEFT
        elif self.pressed[pygame.K_w] or self.pressed[pygame.K_UP]:
            user_input = INPUT.UP
        elif self.pressed[pygame.K_d] or self.pressed[pygame.K_RIGHT]:
            user_input = INPUT.RIGHT
        elif self.pressed[pygame.K_s] or self.pressed[pygame.K_DOWN]:
            user_input = INPUT.DOWN
        elif self.pressed[pygame.K_ESCAPE]:
            user_input = INPUT.ESCAPE
        return user_input

class GameRules():
    """ Holds game rules, determines what should happen upon game interaction """
    def __init__(self):
        self.score = 0
        self.fat = STARTING_FAT
    def add_to_score(self, score):
        """ add points to our score """
        self.score += score
    def get_score(self):
        """ return our current score """
        return self.score
    def player_eats_food(self, snake, food):
        """Check whether the player is currently eating food, add fat and return true if so"""
        head = snake[0]
        head_x, head_y = head
        for food_item in food:
            food_x, food_y = food_item
            #Return whether or not the player's received food, adds fat if they have
            if head_x == food_x and head_y == food_y:
                #We've eaten food, update our score
                self.score += int(150 + int(len(snake)/10)*5)

                #Add more fat to the user if they already have some or they have a decent score
                self.fat += 8 + int(self.fat/4) + int(self.score/500)
                return True
        return False

    def player_loss(self, snake, demon):
        """Checks if the player has lost, returns true if so"""
        #Get the snake's head, as well as the rest of its body
        head = snake[0]
        body = snake[1:]

        #Get the head's x and y location
        head_x, head_y = head

        #If the head has moved out of bounds, we've lost
        if head_x < 0 or head_x >= GRID_SIZE_X or head_y < 0 or head_y >= GRID_SIZE_Y:
            return True

        #If the head has hit the body, we've lost
        for body_segment in body:
            if head == body_segment:
                return True

        #If the demon's too close to the head
        for indiv_demon in demon:
            demon_x, demon_y = indiv_demon
            if (head_x < demon_x < head_x + CELL_SIZE and
                head_y < demon_y < head_y + CELL_SIZE):
                return True

        #Since none of the above conditions have applied, we haven't lost yet
        return False
    def player_win(self, snake):
        """ whether the player has met a win condition """
        return len(snake) >= GRID_SIZE_X/CELL_SIZE*GRID_SIZE_Y/CELL_SIZE - 1
    def player_burn_fat(self):
        """ burns fat from the snake """
        #If the player has fat, burn it and make them grow
        if self.fat > 0:
            #Slightly increase our score counter
            self.score += int(int(self.fat/5)*5 + 20)
            self.fat -= 1
            return True
        return False

class NonPlayerEntityHandler():
    """ Handles all non-player entities (food, demon) """
    def __init__(self, snake):
        """ Class Constructor """
        self.set_food_position(snake)
        self.demon = []
        for indiv_demon in range(0, DEMONS_TO_SPAWN):
            demon_x = -50 + (GRID_SIZE_X + 100)*rng.randrange(0, 2)
            demon_y = -50 + 10*indiv_demon + (GRID_SIZE_Y + 100)*rng.randrange(0, 2)
            self.demon.append([demon_x, demon_y])
    def set_food_position(self, snake):
        """ Moves the food to a new board location """
        valid_position = False
        self.pos = []

        #While the food is within the snake
        food_item = 0
        while food_item in range(0, 1 + int(len(snake)/80)):
            while(not valid_position and
                  len(snake) < (GRID_SIZE_X*GRID_SIZE_Y)/CELL_SIZE - (1 + int(len(snake)/80))):
                #Set a new position for the food
                food_x = rng.randrange(0, GRID_SIZE_X, CELL_SIZE)
                food_y = rng.randrange(0, GRID_SIZE_Y, CELL_SIZE)
                valid_position = True

                #Check if the new position is in the snake
                for body_segment in snake:
                    seg_x, seg_y = body_segment
                    if seg_x == food_x and seg_y == food_y:
                        valid_position = False
            food_item += 1
            valid_position = False
            self.pos.append([food_x, food_y])
    def demon_active(self, snake):
        """ Checks and returns whether or not the demon is active """
        #Return whether or not the demon should be active
        return len(snake) > 50
    def set_demon_position(self, snake):
        """ Sets the demon's current position """
        #Only move the demon if the snake is long enough
        if self.demon_active(snake):
            #Get snake's x and y values
            head = snake[0]
            head_x, head_y = head
            for demon_index in range(0, len(self.demon)):
                #Get demon's x and y values
                demon_x, demon_y = self.demon[demon_index]

                #Set amount to move in x, y
                move_x = rng.randrange(2, int(len(snake) / 12))
                move_y = rng.randrange(2, int(len(snake) / 12))

                if abs(demon_x - head_x) > abs(demon_y - head_y):
                    move_x /= 2
                    move_y += 2*IMPOSSIBLE_MODE
                else:
                    move_x += 2*IMPOSSIBLE_MODE
                    move_y /= 2

                #Move closer to the player in the x INPUTection
                if head_x + CELL_SIZE/2 > demon_x:
                    demon_x += move_x
                else:
                    demon_x -= move_x

                #Move closer to the player in the y INPUTection
                if head_y + CELL_SIZE/2 > demon_y:
                    demon_y += move_y
                else:
                    demon_y -= move_y

                self.demon[demon_index] = [demon_x, demon_y]
    def get_demon_position(self):
        """ Gets the demon's current position """
        return self.demon
    def get_food_position(self):
        """ Gets the food's current position """
        return self.pos

class AudioPlayer():
    """ Handles all audio functionality """
    def __init__(self):
        """ Class Constructor """
        #If the mixer hasn't been initialized, initialize it
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        #Set the volume of music and sfx
        self.effect_volume = EFFECT_VOLUME
        self.music_volume = MUSIC_VOLUME

        #Load menu, food, entity sounds
        self.menu_select = pygame.mixer.Sound("wav/MenuSelect.wav")
        self.passive_food_collected = pygame.mixer.Sound("wav/FoodCollectPassive.wav")
        self.hunting_food_collected = pygame.mixer.Sound("wav/FoodCollectHunting.wav")
        self.demon_move = pygame.mixer.Sound("wav/DemonMove.wav")

        #Set audio volumes for the previously loaded sounds and music
        pygame.mixer.music.set_volume(self.music_volume)
        self.menu_select.set_volume(self.effect_volume)
        self.passive_food_collected.set_volume(self.effect_volume)
        self.hunting_food_collected.set_volume(self.effect_volume)
        self.demon_move.set_volume(.4*self.effect_volume)

        #Set the filename of the first music file
        self.filename = "ogg/SnakeP1.ogg"
    def change_volume(self, increase):
        """ Updates volume based on user input """
        if increase:
            self.music_volume += 0.05
            self.effect_volume += 0.1
        else:
            self.music_volume -= 0.05
            self.effect_volume -= 0.1

        #If the volume isn't greater than 0 and less than 1, fix it
        self.music_volume = min(1, max(0, self.music_volume))
        self.effect_volume = min(1, max(0, self.effect_volume))

        #Update the volume for effects and music
        pygame.mixer.music.set_volume(self.music_volume)
        self.menu_select.set_volume(self.effect_volume)
        self.passive_food_collected.set_volume(self.effect_volume)
        self.hunting_food_collected.set_volume(self.effect_volume)
        self.demon_move.set_volume(.4*self.effect_volume)
    def play_food_collected(self, demon_active):
        """ Play a sound when food is collected """
        #Play a different sound depending on whether the demon is active or not
        if not demon_active:
            self.passive_food_collected.play()
        else:
            self.hunting_food_collected.play()
    def play_demon_move(self):
        """ Play a sound when the demon moves """
        self.demon_move.play()
    def play_menu_music(self, play_demon_music=False):
        """ Plays music on the main menu, passed in is the type to play """
        #Change the song we're playing based on how far the snake made it
        if play_demon_music:
            self.filename = "ogg/SnakeHuntJinnMini.ogg"
        else:
            self.filename = "ogg/SnakeHuntFood.ogg"
        #Load the music and start playing it
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play(loops=-1)
    def play_menu_select(self):
        """ Replays a sound when selecting something on the main menu """
        self.menu_select.stop()
        self.menu_select.play()
    def play_alive(self, snake):
        """ Play a different song depending on the current 'phase' """
        if(self.filename == "ogg/SnakeHuntJinnMini.ogg" or
           self.filename == "ogg/SnakeHuntFood.ogg" or not
           pygame.mixer.music.get_busy()):
            #Play specific music based on how long the snake is
            if len(snake) < 20:
                self.filename = "ogg/SnakeP1.ogg"
            elif len(snake) < 50:
                self.filename = "ogg/SnakeP1B1.ogg"
            elif len(snake) < 80:
                self.filename = "ogg/SnakeP2B2.ogg"
            elif len(snake) < 120:
                self.filename = "ogg/SnakeP2B2H1.ogg"
            elif len(snake) < 160:
                self.filename = "ogg/SnakeP2B2H1D1.ogg"
            else:
                self.filename = "ogg/SnakeP2B2H1D1G1.ogg"
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play()
    def play_dead(self, snake):
        """ Play a sound if the player is dying """
        #Play different music depending on if the snake has encountered the boss
        if len(snake) < 50:
            self.filename = "ogg/SnakeLoss.ogg"
        else:
            self.filename = "ogg/SnakeDeath.ogg"
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()

        #wait for the music to end before stopping the game
        while pygame.mixer.music.get_busy():
            self.filename = "HELP"
    def play_win(self):
        """ Plays a sound upon winning the game """
        #Play a noise if you somehow, SOMEHOW, win the game
        self.filename = "ogg/SnakeVictory.ogg"
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        #wait for the music to end before stopping the game
        while pygame.mixer.music.get_busy():
            self.filename = "HELP"
