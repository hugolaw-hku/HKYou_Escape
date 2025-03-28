import curses
import json
from kits.json_operations import *
import os

def _map(stdscr, map_path, start, end, prompt_pos=[]) -> bool:

    stdscr.clear()
    curses.curs_set(0)                  # disable the cursor
    curses.use_default_colors()
    stdscr.nodelay(1)                   # Set the getch() to non-blocking 
    stdscr.timeout(500)                 # Wait 500ms between screen refreshes
    stdscr.keypad(True)

    '''
    --------------------------
        Function Arguemnts              
    --------------------------
    
    -   map_path   [str]    the directory that stores the map slides
    -   start      [int]    the number of starting map slide
    -   end        [int]    the number of ending map slide
    -   prompt_pos [list]   the list that stores the slides that need to prompt (in ascending order)
    
    '''

    folder = os.listdir(map_path)

    for i in range(start, end+1):                                                   # number in map name must be consecutive integers                  
        if f'{i}.txt' not in folder:
            raise Exception(f'Non-continuous map slides: slide {i} is missing')
    
    if 'prompt.txt' in folder:                                                      # get prompts
        with open(f'{map_path}/prompt.txt', 'r', encoding='utf-8') as f:
            prompt_txt = [i[:-1] for i in list(f)]
    else:
        prompt_txt = [] 
    
    if len(prompt_pos) > len(prompt_txt):
        raise Exception(f'Unmatch prompts: {len(prompt_pos)} prompts expected, but only {len(prompt_txt)} prompts found')

    del folder

    '''
    ---------------------
        Map Variables
    ---------------------
    '''
    position = start-1                                          # slide of the map
    map_box = []                                                # array that stores the map in strings
    c_index = [0, 0]                                            # index of the coordinate of character
    prompts = {a: b for a,b in zip(prompt_pos, prompt_txt)}     # {index of slide: prompt text}

    '''
    -------------------------------------
        Character Animation Variables
    -------------------------------------
    '''

    last_pos = [0, 0]
    charc_facing = False                                        # False: left, True: right (affect head / body)
    charc_head = ['Ó','Ò']
    charc_body = ['├█\\', '/█┤']
    charc_moving = False                                        # alternating between True & False during movement (affect legs)
    charc_legs = ['║', '/ \\']

    

    '''
    -------------------------
        Screens Variables
    -------------------------
    '''
    screen_status = -2    
    quit_confirm = False
    quit_menu = True

    '''
    ---------------------
        The Main Loop
    ---------------------
    '''

    while True:   
        
        '''
        -----------------------------
            Screen Size Detection
        -----------------------------
        '''

        height, width = stdscr.getmaxyx()                       # get the screen size
        center_height, center_width = (height-4) // 2, (width-10) // 2   # get the center point of screen
        
        if (height < 10) or (width < 40):                       
            screen_status = -1                                  # -1 for screen size <= 10x40 (height x width), 0 for screen size <= 25x100, 1 for the else
        elif (height < 28) or (width < 120):
            screen_status = 0
        else:
            screen_status = 1

        '''
        --------------------------------------
            Display Screen Size Adjustment
        --------------------------------------
        '''   
        stdscr.erase()

        if screen_status == -1:
            stdscr.addstr(0, 0, '⇱')                            # display "⇱⇲" to ask user to enlarge screen
            stdscr.addstr(1, 2, '⇲')
        elif screen_status == 0:
            stdscr.addstr(0, 0, '⇱')
            stdscr.addstr(1, 2, 'Please enlarge your screen')
            stdscr.addstr(2, 29, '⇲')
            

        '''
        --------------------------
            Display Map Screen
        --------------------------
        '''   
        if screen_status == 1:
            if not quit_confirm:
                position += 1
            if position > end:                                                                  # stop animation after displaying all slides
                load_n_save(slide=end+1)
                break

            with open(f'{map_path}/{position}.txt', 'r', encoding='utf-8') as f:                # open respective map slide file
                map_box = list(f)

            for i, line in enumerate(map_box):
                map_box[i] = line[:-1]
                if 'X' in line:
                    c_index = [i-1, line.find('X')]                                             # find the coordinate of the character

            for i, line in enumerate(map_box):
                y = center_height-c_index[0]+i
                x = center_width-c_index[1]
                if (y < 0) or (y >= height-1):                                                  # ignore out-boundary parts for display to avoid curses error
                    continue
                stdscr.addstr(y, (x if x >= 0 else 0), line[(-1*x if x<=0 else 0):width-x-1])   # display the game map with the character in center
    

            # display the character

            if last_pos[1] < c_index[1]:
                charc_facing = True
            elif last_pos[1] > c_index[1]:
                charc_facing = False

            if last_pos != c_index:
                charc_moving = not charc_moving

            stdscr.addstr(center_height, center_width, charc_head[int(charc_facing)])                         
            stdscr.addstr(center_height+1, center_width-1, charc_body[int(charc_facing)])
            stdscr.addstr(center_height+2, center_width-int(charc_moving), charc_legs[int(charc_moving)])

            last_pos = c_index                                                      # save for next loop


            # display the prompts for specific slides

            if position in prompt_pos:                                              
                stdscr.addstr(height - 7, 0, '╭'+'─'*(width-2)+'╮')
                for i in range(6, 2, -1):
                    stdscr.addstr(height - i, 0, '│'+' '*(width-2)+'│')
                p_temp = prompts[position].split('+')
                for i, v in enumerate(p_temp):
                    stdscr.addstr(height - 6 + i, 1, v)
                stdscr.addstr(height - 3, 1, 'Press any key to continue.')
                stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')


            # display the Pause Game prompts (when player presses 'm')

            if quit_confirm:
                stdscr.addstr(height - 7, 0, '╭'+'─'*(width-2)+'╮')
                for i in range(6, 2, -1):
                    stdscr.addstr(height - i, 0, '│'+' '*(width-2)+'│')
                stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')
                stdscr.addstr(height - 6, center_width-6, 'Pause Game?', curses.A_BOLD)
                if quit_menu:
                    stdscr.addstr(height - 4, center_width-10, ' YES ', curses.A_REVERSE)
                    stdscr.addstr(height - 4, center_width+5, ' NO ')
                else:
                    stdscr.addstr(height - 4, center_width-10, ' YES ')
                    stdscr.addstr(height - 4, center_width+5, ' NO ', curses.A_REVERSE)
                stdscr.addstr(height - 3, center_width-11, 'Press SPACE to confirm')

        stdscr.refresh()


        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()
        if (position in prompt_pos) and (not quit_confirm) and (screen_status == 1) and ((c == curses.KEY_RESIZE) or (c == -1)):                   # keep the current slide when screen is resized
            position -= 1
            
        if c == ord('m'):
            quit_confirm = True
            if (position == 0):
                position += 1

        if (quit_confirm) and (c == ord(' ')):
            if quit_menu:
                load_n_save(slide=position)
                break
            quit_confirm = False
            stdscr.clear()
            continue

        if ((c == curses.KEY_RIGHT) or (c == curses.KEY_LEFT)) and quit_confirm:
            quit_menu = not quit_menu
            continue


    stdscr.keypad(False)
    return (quit_confirm and quit_menu)


if __name__ == '__main__':
    start = 1
    end = 15
    map_path = './map_1'
    prompt_pos = [3, 12]

    curses.wrapper(_map, map_path, start, end, prompt_pos)
