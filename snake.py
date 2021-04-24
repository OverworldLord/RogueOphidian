"""
---------------------------------------------
Project: Snake Game
File Name: snake.py
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

    pylint snake.py -d no-member

This resulted in a rating of 10/10.
---------------------------------------------
This file contains the driver, and makes use
of classes defined in scene.py in order to
run the snake game.
---------------------------------------------
"""
#Import pygame
import pygame

#Imports all classes and modules used in the program
from scene import INPUT
from scene import RunStats
from scene import DisplayUpdater
from scene import AudioPlayer
from scene import PlayerInput
from scene import GameRules
from scene import NonPlayerEntityHandler

#Imports the required constants from scene (not all are required)
from scene import GRID_SIZE_X
from scene import GRID_SIZE_Y
from scene import CELL_SIZE
from scene import UPPER_BOUND
from scene import LOWER_BOUND

def main():
    """ Driver program, used to run the snake game """
    #Initialize pygame
    pygame.init()

    #Set up the display and draw it to screen
    display = DisplayUpdater()
    display.generate_display()

    #Set up the audio player
    sound = AudioPlayer()

    sound.play_menu_music()
    #Set up the controls
    controls = PlayerInput()

    #Start off in the main menu, can go to credits, leaderboard, or game
    display.show_main_menu()
    user_input = controls.get_menu_input(sound)
    #While the user hasn't quit from the main menu
    while user_input != INPUT.ESCAPE:
        #If the player hits ENTER, launch the game
        if user_input == INPUT.ENTER:
            play_demon_music = game(display, sound, controls)
            sound.play_menu_music(play_demon_music)
            controls.clear_menu_input()
            user_input = INPUT.SPACE

        #If the player hits SPACE, go to the leaderboard
        if user_input == INPUT.SPACE:
            display.show_leaderboard()
            user_input = controls.get_menu_input(sound)
        #If the player hits C, go to the credits
        if user_input == INPUT.C:
            display.show_credits()
            user_input = controls.get_menu_input(sound)

        #If the player hits ESC, return to the main menu.
        #must be in own if statement so we don't quit
        if user_input in (INPUT.ESCAPE, INPUT.SPACE, INPUT.C):
            display.show_main_menu()
            user_input = controls.get_menu_input(sound)

def game(display, sound, controls):
    """ Used to run the actual game part of the program """

    #Get the game rules
    ruleset = GameRules()

    #Create a new snake that will act as a queue, the head is location 0 and tail is location n.
    snake = []
    snake.append([GRID_SIZE_X/2 - GRID_SIZE_X/2 % CELL_SIZE,
                  GRID_SIZE_Y/2 - GRID_SIZE_Y/2 % CELL_SIZE])

    #Create a food handler
    food = NonPlayerEntityHandler(snake)

    #Set a INPUTection to start off with
    new_direction = INPUT.RIGHT

    #Redraw the entire display
    display.redraw(snake, food.get_food_position(), food.get_demon_position(), ruleset.get_score())


    #Game's about to start, add the run info
    run_stats = RunStats()

    add_score_time = pygame.time.get_ticks()

    #While the player hasn't hit escape or lost
    while(new_direction != INPUT.ESCAPE and
          not ruleset.player_loss(snake, food.get_demon_position()) and
          not ruleset.player_win(snake)):

        #Wait as either a function of length of the snake or, if it's too small, 50 ms
        wait_until = pygame.time.get_ticks() + max(UPPER_BOUND - len(snake)/2, LOWER_BOUND)
        while (wait_until > pygame.time.get_ticks() and new_direction != INPUT.ESCAPE and
               not ruleset.player_loss(snake, food.get_demon_position())):
            #Update the audio player
            sound.play_alive(snake)

            #Get the snake's new direction
            current_direction = controls.get_movement()
            if current_direction != INPUT.NONE:
                new_direction = current_direction

            #Move the demon multiple times per round
            if pygame.time.get_ticks() % 100 == 0:
                food.set_demon_position(snake)
                display.redraw(snake,
                               food.get_food_position(),
                               food.get_demon_position(),
                               ruleset.get_score())

        #If the demon hasn't caught the player
        if not ruleset.player_loss(snake, food.get_demon_position()):
            #Add score to the player every three seconds
            if add_score_time <= pygame.time.get_ticks():
                ruleset.add_to_score(5)
                add_score_time += 3000

            #Update the new head
            snake.insert(0, movement_handler(new_direction, snake))

            #Check if the player's eaten food
            if ruleset.player_eats_food(snake, food.get_food_position()):
                food.set_food_position(snake)
                sound.play_food_collected(food.demon_active(snake))
            #If the demon has spawned in, play it's sound
            elif food.demon_active(snake):
                sound.play_demon_move()

            #If the snake isn't burning fat to grow, remove the old position of the tail
            if not ruleset.player_burn_fat():
                snake.pop()

    #Play the death music and possibly show an image
    if(ruleset.player_loss(snake, food.get_demon_position())
       or new_direction == INPUT.ESCAPE and food.demon_active(snake)):
        if food.demon_active(snake):
            display.show_image()
        sound.play_dead(snake)
    #If the player somehow wins, play victory music
    elif ruleset.player_win(snake):
        sound.play_win()

    #Output run to file
    run_stats.output_to_file(ruleset.get_score())

    return food.demon_active(snake)

def movement_handler(new_direction, snake):
    """ Handles movement for the snake """
    #Get the head of the snake
    new_head = snake[0].copy()
    #Update the new head position based on where the snake moved
    if new_direction == INPUT.LEFT:
        new_head[0] -= CELL_SIZE
    elif new_direction == INPUT.UP:
        new_head[1] -= CELL_SIZE
    elif new_direction == INPUT.RIGHT:
        new_head[0] += CELL_SIZE
    else: #new_direction == INPUT.DOWN:
        new_head[1] += CELL_SIZE

    #We will update the position of the snake's head
    new_x, new_y = new_head
    if len(snake) >= 2:
        old_x, old_y = snake[1]
    else:
        old_x, old_y = [-1, -1]

    #If the player is running into themselves, reverse their INPUTection
    if new_x == old_x and new_y == old_y:
        if new_direction == INPUT.LEFT:
            new_head[0] += CELL_SIZE*2
        elif new_direction == INPUT.UP:
            new_head[1] += CELL_SIZE*2
        elif new_direction == INPUT.RIGHT:
            new_head[0] -= CELL_SIZE*2
        else: #new_direction == INPUT.DOWN:
            new_head[1] -= CELL_SIZE*2
    return new_head

#Call main
main()
