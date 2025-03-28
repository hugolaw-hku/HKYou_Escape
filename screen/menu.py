import curses
import json
import os

os.environ['TERM'] = "xterm-256color"

def menu(stdscr) -> int:

    stdscr.clear()                                              # clear the screen
    stdscr.keypad(True)                                         # enable keypad mode
    curses.curs_set(0)                                          # hides cursor

    '''all colors used'''                                     
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_color(37, 800, 600, 500)
    curses.init_pair(6, 37, curses.COLOR_BLACK)
    stdscr.bkgd(' ',curses.color_pair(1))


    '''
    -------------------------
        Screens Variables
    -------------------------
    -   For now, we have three screens: (1) Warning when Screen Size <= 10x40 (height x width), (2) Warning when Screen Size <= 25x110 & (3) Main Menu
    -   screen_status is added to avoid clearing the screen everytime, which is not efficient
    '''
    screen_resize = True                                        # flag that indicates screen resize
    screen_status = -2
    menu_index = 0                                              

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
        -   For curses, error will be raised if the screen size is not big enough to display
        -   We have to detect the screen size and tell user to enlarge it when it is too small
        '''
        height, width = stdscr.getmaxyx()                       # get the screen size
        center_height, center_width = height // 2, width // 2   # get the center point of screen
        
        if (height < 10) or (width < 40):                       
            screen_status = -1                                  # -1 for screen size <= 10x40 (height x width), 0 for screen size <= 25x120, 1 for the else
        elif (height < 28) or (width < 120):
            screen_status = 0
        else:
            screen_status = 1

        '''
        ---------------
            Display
        ---------------
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
            else:                                               # display the game name in ASCII art format
                with open('./screen/logo.txt', 'r', encoding='utf-8') as f:
                    logo = list(f)
                logo_height = center_height - 13
                for i, v in enumerate(logo):
                    if i % 2 == 0:
                        stdscr.addstr(logo_height + i, center_width - (len(v)//2), v, curses.color_pair(6))
                    else:
                        stdscr.addstr(logo_height + i, center_width - (len(v)//2), v, curses.color_pair(6))
                stdscr.attroff(curses.A_BOLD)

            stdscr.refresh()
        
        if screen_status == 1:                               # display the menu only when the screen is big enough
            if menu_index == 0:
                stdscr.addstr(center_height+2, center_width-7, '🎮 Play       ', curses.color_pair(2))   # change the background and font color for item being selected
                                                                                              # curses.A_REVERSE is the reverse color pair of the default color pair
            else:
                stdscr.addstr(center_height+2, center_width-7, '🎮 Play       ')
            

            if menu_index == 1:
                stdscr.addstr(center_height+3, center_width-7, '📖 How to Play', curses.color_pair(2))
            else:
                stdscr.addstr(center_height+3, center_width-7, '📖 How to Play')

            # deprecated
            '''if menu_index == 2:
                stdscr.addstr(center_height+4, center_width-7, '💾 Save Game  ', curses.color_pair(2))
            else:
                stdscr.addstr(center_height+4, center_width-7, '💾 Save Game  ')'''


            if menu_index == 2:
                stdscr.addstr(center_height+4, center_width-7, '👋 Quit      ', curses.color_pair(2))
            else:
                stdscr.addstr(center_height+4, center_width-7, '👋 Quit      ')
            
            stdscr.refresh()

        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()                                      # get keyboard input

        if screen_status == 1:                                  # enable key actions only when screnn is big enough
            if c == curses.KEY_UP:             
                menu_index -= 1                                 # use mod to cycle through menu 
                menu_index %= 3                      
            elif c == curses.KEY_DOWN:
                menu_index += 1
                menu_index %= 3                               
            elif c in [10, 13] or c == ord(' '):                # detect ENTER key / space
                break                                           # actions to be added
        if c == curses.KEY_RESIZE:                              # set the flag to True when screen is resized
            screen_resize = True

    stdscr.keypad(False)                                        # disable keypad mode after exiting the main loop
    return menu_index

if __name__ == '__main__':
    m = -1
    while m != 2:
        m = curses.wrapper(menu)
