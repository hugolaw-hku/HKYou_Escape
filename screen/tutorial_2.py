import curses
import copy
from kits.matrix_operations import *
from kits.json_operations import *
import random

def tut_2(stdscr) -> None:

    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.nodelay(1)                   # Set the getch() to non-blocking 
    stdscr.timeout(15)                  # Wait 100ms between screen refreshes
    stdscr.keypad(True)
    
    matrix = [                         
        [0, 0, 0, 0, 0],                
        [0, 0, 0, 1, 0], 
        [0, 0, 0, 0, 0],
        [0, 'A', 'A', 'A', 0],
        [0, 0, 0, 0, 0],
    ]
    core = (3, 3)                       
    h_margin = 1
    v_margin = 1

    win_con = [
        [0, 'A', 0],
        [0, 'A', 0],
        [1, 'A', 0],
    ]

    description = generate_description(win_con)

    def check(matrix):
        return get_core(matrix, core, h_margin, v_margin) == win_con
        
    '''
    -------------------------
        In-Game Variables
    -------------------------
    '''

    board_size = (core[0] + v_margin*2, core[1] + h_margin*2)   # the whole board size
    matrix_original = copy.deepcopy(matrix)                     # store for use in case of restarting game state
                                                                # NOTE: cannot use .copy() because it is a nested list
    row_mode = not (board_size[1] == 1)                         # True: row mode / False: column mode
    current = [0, 0]                                            # [current row position, current column position] (ignore margins)
    move_count = 0   
    win = False                                            


    '''
    -------------------------
        Screens Variables
    -------------------------
    '''
    screen_resize = True                                        # flag that indicates screen resize
    screen_status = -2
    
    def compute_screen_variable():
        global box_width, target_rows, content_height, content_width
        box_width = max(map(len, description))
        if box_width < 10:
            box_width = 10
        target_rows = len(description) - 1
        content_height, content_width = 3*board_size[0] + 4, 15 + 5*board_size[1] + box_width

    compute_screen_variable()


    '''
    ---------------------------
        Tutorials Variables
    ---------------------------
    '''       

    welcome_str = [
        ['Throughout your rescue, you will often encounter square locks with multiple columns and rows.', 'Press any key to continue...'],
        ['We still call the bold grids as \"CORE\" and others as \"MARGINS\".', 'Press any key to continue...'],
        ['Each time you see a lock, a TARGET is provided. Your goal is to match the CORE with the TARGET.', 'Press any key to continue...'],
        ['I will now introduce you with a few more controls before you start the rescue.', 'Press any key to continue...']
    ]

    msg_str = [
        ['Whenever we move a row, we are rotating it. Let\'s rotate the current row once.', 'Press LEFT arrow (5 times)...'],
        ['We can surely select a different row. Select the 3rd row in the CORE.', 'Press DOWN arrow (2 times)...'],
        ['We can press SPACE to switch between [column mode] and [row mode].', 'Press SPACE...'],
        ['The mechanics are basically the same for columns. Rotate the current row once.', 'Press UP arrow (5 times)...'],
        ['Select the 3rd column in the CORE.', 'Press RIGHT arrow (2 times)...'],
        ['We may sometimes want to RESET the lock and the move counts.', 'Press \'R\'...']
    ]

    display_str = welcome_str + msg_str
    display_trigger = 1
                                 
    playable = False                            # user can play without any restriction
    
    animation_played = [False]* (len(display_str) + 2)
    animation_char = 1
    leave = False


    '''
    -------------------------
        Screens Functions
    -------------------------
    '''
    def below_select(row) -> bool:
        return row_mode and row > v_margin + current[0]

    def is_select(row) -> bool:
        return row_mode and row == v_margin + current[0]
    
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
        ---------------------------
            Display Game Screen
        ---------------------------
        '''   

        if screen_status == 1: 

            '''
            ---------------------------
                Display Main Board
            ---------------------------
            '''

            start_index = center_width - (content_width // 2) - 1
            if start_index < 0:
                start_index = 0

            # display top and bottom line boundary
            stdscr.addstr(0, start_index, '╔' + '═'*(6 + 5*board_size[1]) + '╗')         
            stdscr.addstr(content_height - 1, start_index, '╚' + '═'*(6 + 5*board_size[1]) + '╝')

            if row_mode:
                stdscr.addstr(3*(v_margin + current[0]) + 1, start_index, '║  ╭' + '─'*(5*board_size[1]) + '╮  ║')
                stdscr.addstr(3*(v_margin + current[0]) + 5, start_index, '║  ╰' + '─'*(5*board_size[1]) + '╯  ║')
            else:
                stdscr.addstr(1, start_index, '║  ' + '     '*h_margin + ''.join(['╭─────╮' if current[1] == i else '     ' for i in range(core[1])]) + '     '*h_margin + '  ║')
                stdscr.addstr(content_height - 2, start_index, '║  ' + '     '*h_margin + ''.join(['╰─────╯' if current[1] == i else '     ' for i in range(core[1])]) + '     '*h_margin + '  ║')         


            # display the rest row by row
            for row, items in enumerate(matrix):   

                # turning matrix items into formatted strings for display
                # each row is splited into THREE parts since the core grids will be displayed bold while margins will not
                list1 = [f'│ {items[i]} │' if core[0] + v_margin > row >= v_margin else '     ' for i in range(h_margin)]
                list2 = [f'┃ {items[h_margin + i]} ┃' if core[0] + v_margin > row >= v_margin else f'│ {items[h_margin + i]} │' for i in range(core[1])]
                if not row_mode:
                    list2[current[1]] = '│' + list2[current[1]] + '│'
                list3 = [f'│ {items[h_margin + core[1] + i]} │' if core[0] + v_margin > row >= v_margin else '     ' for i in range(h_margin)]
                temp1 = '║  ' + ' '*(row_mode - is_select(row)) + '│'*(is_select(row)) + ''.join(list1)
                temp2 = ''.join(list2)
                temp3 = ''.join(list3) + ' '*(row_mode - is_select(row)) + '│'*(is_select(row)) + '  ║'

                # display
                if core[0] + v_margin > row >= v_margin:                                                # rows with core grids
                    height_index = 3*(row) + (is_select(row)) + (below_select(row))*2 + (not row_mode)
                    width_index = [3 + h_margin*5 + row_mode, 3 + h_margin*5 + core[1]*5 + row_mode + (not row_mode)*2]

                    stdscr.addstr(height_index + 1, start_index, '║  ' + ' '*(row_mode-is_select(row)) + '│'*(is_select(row)) + '┌───┐'*h_margin)
                    stdscr.attron(curses.A_BOLD)
                    cap = ['┏━━━┓']*core[1]
                    if not row_mode:
                        cap[current[1]] = '│' + cap[current[1]] + '│'
                    stdscr.addstr(height_index + 1, start_index + width_index[0], ''.join(cap))
                    stdscr.attroff(curses.A_BOLD)
                    stdscr.addstr(height_index + 1, start_index + width_index[1], '┌───┐'*h_margin + ' '*(row_mode-is_select(row)) + '│'*(is_select(row)) + '  ║')

                    stdscr.addstr(height_index + 2, start_index, temp1)
                    stdscr.attron(curses.A_BOLD)
                    stdscr.addstr(height_index + 2, start_index + width_index[0], temp2)
                    stdscr.attroff(curses.A_BOLD)
                    stdscr.addstr(height_index + 2, start_index + width_index[1], temp3)

                    stdscr.addstr(height_index + 3, start_index, '║  ' + ' '*(row_mode-is_select(row)) + '│'*(is_select(row)) + '└───┘'*h_margin)
                    stdscr.attron(curses.A_BOLD)
                    bottom = ['┗━━━┛']*core[1]
                    if not row_mode:
                        bottom[current[1]] = '│' + bottom[current[1]] + '│'
                    stdscr.addstr(height_index + 3, start_index + width_index[0], ''.join(bottom))
                    stdscr.attroff(curses.A_BOLD)
                    stdscr.addstr(height_index + 3, start_index + width_index[1], '└───┘'*h_margin + ' '*(row_mode-is_select(row)) + '│'*(is_select(row)) + '  ║')

                else:                                                                                   # margin rows
                    height_index = 3*(row) + (below_select(row))*2 + (not row_mode)
                    cap = ['┌───┐']*core[1]
                    if not row_mode:
                        cap[current[1]] = '│' + cap[current[1]] + '│'
                    stdscr.addstr(height_index + 1, start_index, '║  ' + ' '*(5*h_margin+row_mode) + ''.join(cap) + ' '*(5*h_margin+row_mode) + '  ║')
                    stdscr.addstr(height_index + 2, start_index, temp1 + temp2 + temp3)
                    bottom = ['└───┘']*core[1]
                    if not row_mode:
                        bottom[current[1]] = '│' + bottom[current[1]] + '│'
                    stdscr.addstr(height_index + 3, start_index, '║  ' + ' '*(5*h_margin+row_mode) + ''.join(bottom) + ' '*(5*h_margin+row_mode) + '  ║')

            right_index = start_index + 10 + 5*board_size[1]

            # display the description of the winning comdition
            stdscr.addstr(0, right_index, '╭' + '─'*(box_width//2-3) + ' TARGET ' + '─'*(box_width//2 + box_width%2 -3) + '╮')
            stdscr.addstr(1, right_index, '│ ' + ' '*(box_width) + ' │')
            for i, v in enumerate(description):
                stdscr.addstr(2 + i, right_index, '│ ' + f'{v:^{box_width}}' + ' │')
            stdscr.addstr(3 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')

            # display move count
            stdscr.addstr(4 + target_rows, right_index, '├' + '─'*(box_width//2-5) + ' MOVE COUNT ' + '─'*(box_width//2 + box_width%2 -5) + '┤')
            stdscr.addstr(5 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')
            stdscr.addstr(6 + target_rows, right_index, '│ ' + ' '*(box_width//2-5) + f'{move_count:^10}' + ' '*(box_width//2 + box_width%2 -5) + ' │')
            stdscr.addstr(7 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')
            stdscr.addstr(8 + target_rows, right_index, '╰─' + '─'*box_width + '─╯')

            # display instruction
            stdscr.addstr(8 + target_rows, right_index, '├─' + '─'*box_width + '─┤')
            stdscr.addstr(9 + target_rows, right_index, '│ ' + f"{'R: reset':^{box_width}}" + ' │')
            stdscr.addstr(10 + target_rows, right_index, '╰─' + '─'*box_width + '─╯')


            '''
            ---------------------------
                Win Condition Check
            ---------------------------
            '''
            if playable:
                win = check(matrix)       
                if win:
                    playable = False
                    continue
                

            '''
            --------------------------------
                Display Tutorial Content  
            --------------------------------
            '''

            # boundaries
            stdscr.addstr(height - 7, 0, '╭'+'─'*(width-2)+'╮')
            for i in range(6, 2, -1):
                stdscr.addstr(height - i, 0, '│'+' '*(width-2)+'│')
            stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')
            

            # tutorial content
            if not playable and not win:
                    
                if not animation_played[display_trigger-1]:
                    animation_played[display_trigger-1] = True
                    animation_char = 0
                    msg_str = display_str[display_trigger-1][0]
                    action = display_str[display_trigger-1][1]

                else:
                    if animation_char < len(msg_str):
                        stdscr.addstr(height - 6, 1, msg_str[0:animation_char])
                        animation_char += 1
                    else:
                        stdscr.addstr(height - 6, 1, msg_str)
                        stdscr.addstr(height - 3, 1, action)

            elif playable:

                if not animation_played[-2]:
                    animation_played[-2] = True
                    animation_char = 0
                    tut_str = 'Let\'s match the CORE with the TARGET!'
                else:
                    if animation_char < len(tut_str):
                        stdscr.addstr(height - 6, 1, tut_str[0:animation_char])
                        animation_char += 1
                    else:
                        stdscr.addstr(height - 6, 1, tut_str)
                        stdscr.addstr(height - 5, 1, 'hint: [1] move the 1 to the upper left corner, [2] move the middle A to center, [3] move the right A to top ', curses.A_BOLD)
                        stdscr.addstr(height - 3, 1, f'Solve the puzzle to continue...')
            else:

                if not animation_played[-1]:
                    animation_played[-1] = True
                    animation_char = 0
                    tut_str = 'Well done! Let\'s go rescue all your friends! Good luck!'
                else:
                    if animation_char < len(tut_str):
                        stdscr.addstr(height - 6, 1, tut_str[0:animation_char])
                        animation_char += 1
                    else:
                        stdscr.addstr(height - 6, 1, tut_str)
                        stdscr.addstr(height - 3, 1, f'Press any key to continue...')
                        leave = True
                        stdscr.nodelay(0)          # getch() to blocking again

        
        stdscr.refresh()


        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()

        if c == curses.KEY_RESIZE:      # set the flag to True when screen is resized
            screen_resize = True
        elif c == -1:
            continue

        if leave:
            break

        if screen_status == 1:                  # input signals in game screen   

            if display_trigger < len(welcome_str) + 1:
                display_trigger += 1

            else:   
                offset = len(welcome_str)

                if c == ord('r') and (playable or display_trigger == offset + 6):                                   # reset the game
                    matrix = copy.deepcopy(matrix_original)
                    row_mode = True
                    current = [0, 0]
                    move_count = 0
                    win = False

                    if not playable:
                        display_trigger += 1
                        playable = True
                        
                if c == ord(' ') and (playable or display_trigger == offset + 3):
                    row_mode = not row_mode
                    if not playable:
                        display_trigger += 1
            
                elif c == curses.KEY_LEFT and (playable or display_trigger == offset + 1):

                    if row_mode:    
                        matrix[v_margin + current[0]] = matrix[v_margin + current[0]][1:] + matrix[v_margin + current[0]][:1]
                        move_count += 1
                        if move_count == 5:
                            display_trigger += 1
                    else:
                        if current[1] > 0 :
                            current[1] -= 1
                    
                elif c == curses.KEY_RIGHT and (playable or display_trigger == offset + 5):

                    if row_mode:    
                        matrix[v_margin + current[0]] = matrix[v_margin + current[0]][-1:] + matrix[v_margin + current[0]][:-1]
                        move_count += 1
                    else:
                        if current[1] < core[1] - 1:
                            current[1] += 1
                        if (current[1] == core[1] - 1) and not playable:
                            display_trigger += 1

                elif c == curses.KEY_UP and (playable or display_trigger == offset + 4):

                    if row_mode:    
                        if current[0] > 0:
                            current[0] -= 1
                    else: 
                        matrix = transpose(matrix)
                        matrix[h_margin + current[1]] = matrix[h_margin + current[1]][1:] + matrix[h_margin + current[1]][:1]
                        matrix = transpose(matrix)
                        move_count += 1

                        if move_count == 10:
                            display_trigger += 1

                elif c == curses.KEY_DOWN and (playable or display_trigger == offset + 2):

                    if row_mode:    
                        if current[0] < core[0] - 1:
                            current[0] += 1
                        if (current[0] == core[0] - 1) and not playable:
                            display_trigger += 1
                    else:
                        matrix = transpose(matrix)
                        matrix[h_margin + current[1]] = matrix[h_margin + current[1]][-1:] + matrix[h_margin + current[1]][:-1]
                        matrix = transpose(matrix)
                        move_count += 1


    stdscr.keypad(False)



if __name__ == '__main__':
    curses.wrapper(tut_2)

