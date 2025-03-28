import curses
import json

def final(stdscr) -> None:

    stdscr.clear()
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)

    moves = jdata["total_moves"]

    
    if moves <= 300:
        msg = '???: I respect your intelligence. I\'ll let you guys go...'
        action = 'Press any key to leave this horrible place...'
        corner_msg = '(I guess I will find another victim)'

    else:
        msg = '???: Making more than 300 moves!? I announce your BAD LUCK in this semester!'
        action = 'Press any key to accept your FAILURE...'
        corner_msg = '(or you dare entering again)'


    '''
    -------------------------
        Screens Variables
    -------------------------
    '''

    screen_resize = True                                        # flag that indicates screen resize
    screen_status = -2
    
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
        ----------------------
            Display Screen
        ----------------------
        '''   

        if screen_status == 1:     

                stdscr.addstr(0, 0, '╭'+'─'*(width-2)+'╮')
                for i in range(1, height-2):
                    stdscr.addstr(i, 0, '│'+' '*(width-2)+'│')
                stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')
                stdscr.addstr(center_height - 4, center_width - 8, f'Total Moves: {moves:^4}', curses.A_BOLD)
                stdscr.addstr(center_height - 2, center_width - len(msg) // 2, msg)  
                stdscr.addstr(center_height + 1, center_width - len(action) // 2, action)
                stdscr.addstr(height - 3, width - 2 - len(corner_msg), corner_msg)
        
        stdscr.refresh()


        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()

        if screen_status == 1:     

                if c != curses.KEY_RESIZE and c != -1:
                    break
                        
        if c == curses.KEY_RESIZE:      # set the flag to True when screen is resized
            screen_resize = True


    stdscr.keypad(False)


if __name__ == '__main__':
    curses.wrapper(final)
