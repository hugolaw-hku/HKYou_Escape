import curses
import json
from screen.tutorial_1 import tut_1
from screen.tutorial_2 import tut_2
from screen.template import lock, generate_level
from screen.endscreen import final
import os
from kits.json_operations import *
from screen.restoregame import restore
from screen.menu import menu
from screen.map_ import _map

os.environ['TERM'] = "xterm-256color"


def mid_load(exit):
    if exit:
        return -1, 999
    return load_prog()



'''
------------------------------
    Game Level Information
------------------------------
Each list contains the argument passed to generate_level(core, pattern, rand_int, duplicate, place, name, level)

Difficulty guideline:
-   core:               larger  --> harder
-   pattern:            larger  --> harder
-   rand_int:           True    --> harder
-   duplciate:          False   --> harder
'''

game_level_information = [
    [(3, 3), 4, False, True, 'HW. Room501', 'Tom', 0],
    [(3, 3), 4, True, True, 'HW. Room502', 'Sam', 1],
    [(3, 3), 4, True, False, 'HW. Room503', 'Amy', 2],

    [(3, 3), 6, False, True, 'MB. MB102', 'Dias', 3],
    [(3, 3), 6, True, True, 'MB. MB103', 'Abay', 4],
    [(3, 3), 6, True, False, 'MB. MB104', 'Asset', 5],

    [(3, 4), 7, False, True, 'CYM. CYPP2', 'Ali', 6],
    [(3, 4), 7, True, True, 'CYM. CYPP3', 'Tair', 7],
    [(3, 4), 7, True, False, 'CYM. CYPP4', 'Sophia', 8],

    [(4, 4), 9, False, True, 'KK. KKLG101', 'Alikhan', 9],
    [(4, 4), 9, True, True, 'KK. KKLG102', 'Jooh', 10],
    [(4, 4), 9, True, False, 'KK. KKLG103', 'Amy', 11],

    [(4, 4), 10, False, True, 'CPD. LG-01', 'Dirk', 12],
    [(4, 4), 10, True, True, 'CPD. LG-02', 'Kelvin', 13],
    [(4, 4), 10, True, False, 'CPD. LG-03', 'Hugo', 14],
]



if __name__ == '__main__':

    try:
        
        while True:

            menu_index = curses.wrapper(menu)

            if menu_index == 0:
                if not 'gamedata.json' in os.listdir('./'):             
                    create_game()                                       # create json file for saving player's game data

                check_error()                                           
                level, slide = load_prog()                              # load progress from json file

                if (level == -1 and slide == 999):
                    if not load_pass():                                 # run tutorial if not passed before
                        curses.wrapper(tut_1)  
                        curses.wrapper(tut_2)
                        pass_tutorial()

                    load_n_save(level=0, slide=1)
                else:
                    if curses.wrapper(restore):                         # resume previous game
                        level, slide = load_prog()
                    else:                                               # play from the start (and override previous game data)
                        load_n_save(level=0, slide=1)

                map_path = './map'
                prompt_pos = [1, 2, 3, 4, 15, 16, 24, 25, 32, 33, 41, 42, 53]
                building_pos_list = [4, 16, 25, 33, 42, 54]

                level, slide = load_prog()
                play_puzzle = check_in_puzzle()                         # check whether player was in the puzzle screen previously                                                                                                                                    
                exit = False

                while slide < 53:

                    for pos in building_pos_list:
                        if slide < pos:
                            slide_end = pos - 1
                            break

                    if not play_puzzle:                                 # display the map
                        exit = curses.wrapper(_map, map_path, slide, slide_end, prompt_pos)     
                        level, slide = mid_load(exit)

                    else:                                               # display the puzzle
                        for i in range(level % 3, 3):
                            exit = curses.wrapper(lock, *generate_level(*game_level_information[level]))
                            level, slide = mid_load(exit)
                            if exit:
                                break

                    play_puzzle = not play_puzzle

                if level != -1 and slide != 999:
                    curses.wrapper(final)                               # final screen
                    restart_game()

            if menu_index == 1:
                if not 'gamedata.json' in os.listdir('./'):             
                    create_game()                                       # create json file for saving player's game data

                curses.wrapper(tut_1)
                curses.wrapper(tut_2)
                pass_tutorial()

            if menu_index == 2:
                break

    except KeyboardInterrupt:
        restart_game()
