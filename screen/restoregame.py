import curses
import json
from kits.json_operations import *
from kits.matrix_operations import *

def restore(stdscr) -> bool:

    stdscr.clear()
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)

    oldgame = (jdata["in_puzzle"]) or (jdata["level"] != -1) or (jdata["slide"] != 0)

    '''
    -------------------------
        Screens Variables
    -------------------------
    '''

    screen_resize = True                                        # flag that indicates screen resize
    screen_status = -2
    restore_menu = True
    
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
        center_height, center_width = height // 2, width // 2   # get the center point of screen
        
        
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

        if screen_resize:                                       # clear the screen only when screen status changed 
            screen_resize = False
            stdscr.clear()

            if screen_status == -1:
                stdscr.addstr(0, 0, '⇱')                        # display "⇱⇲" to ask user to enlarge screen
                stdscr.addstr(1, 2, '⇲')
            elif screen_status == 0:
                stdscr.addstr(0, 0, '⇱')
                stdscr.addstr(1, 2, 'Please enlarge your screen')
                stdscr.addstr(2, 29, '⇲')

            stdscr.refresh()

        '''
        -----------------------------
            Display Prompt Screen
        -----------------------------
        '''   

        if screen_status == 1:                                    

                stdscr.addstr(0, 0, '╭'+'─'*(width-2)+'╮')
                for i in range(1, height-2):
                    stdscr.addstr(i, 0, '│'+' '*(width-2)+'│')
                stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')
                stdscr.addstr(center_height - 2, center_width - 7, 'Resume Game?', curses.A_BOLD)   
                if restore_menu:
                    stdscr.addstr(center_height, center_width-10, ' YES ', curses.A_REVERSE)
                    stdscr.addstr(center_height, center_width+5, ' NO ')
                else:
                    stdscr.addstr(center_height, center_width-10, ' YES ')
                    stdscr.addstr(center_height, center_width+5, ' NO ', curses.A_REVERSE)
                stdscr.addstr(center_height + 1, center_width - 12, 'Press SPACE to confirm.')
        
        stdscr.refresh()


        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()

        if screen_status == 1:     

                if c == ord(' '):

                        if not restore_menu:
                            restart_game()
                        break
            
                elif c == curses.KEY_LEFT:
                    
                        restore_menu = not restore_menu
                        continue
                 
                elif c == curses.KEY_RIGHT:

                        restore_menu = not restore_menu
                        continue

                        
        if c == curses.KEY_RESIZE:      # set the flag to True when screen is resized
            screen_resize = True


    stdscr.keypad(False)
    return restore_menu


if __name__ == '__main__':
    curses.wrapper(restore)
