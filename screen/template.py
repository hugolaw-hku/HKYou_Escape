import curses
import copy
from kits.json_operations import *
from kits.matrix_operations import *
import os
import random

os.environ['TERM'] = "xterm-256color"

def lock(stdscr, matrix, core, h_margin, v_margin, description, check, level, place, name) -> bool:

    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.keypad(True)

    '''
    --------------------------
        Function arguments   
    --------------------------

    -   matrix      [nested list]   the matrix used for the LOCK during the game
    -   core        [tuple]         the dimension of the core grids
    -   h_margin    [int]           the number of column margins (to the left and right of the core grids)
    -   v_margin    [int]           the number of row margins (to the top and bottom of the core grids)
    -   description [str]           a short description of the game win condition
    -   check       [function]      a callable function that is used to check win condition (takes in one argument: matrix)

    -   level       [int]           the level
    -   place       [str]           the trapped location
    -   name        [str]           the name of the trapped friend
    '''

    board_size = (core[0] + v_margin*2, core[1] + h_margin*2)   # the whole board size

    # check validity of matrix (for internal implementation purpose)
    if (len(matrix), len(matrix[0])) != board_size:
        raise Exception(f'Matrix does not match the board size {board_size}: core={core}, h_margin={h_margin}, v_margin={v_margin}')
    
    for i, row in enumerate(matrix):
        if len(row) != board_size[1]:
            raise Exception(f'Row {i} in matrix does not match the board size {board_size}: core={core}, h_margin={h_margin}, v_margin={v_margin}')

        
    '''
    -------------------------
        In-Game Variables
    -------------------------
    '''

    matrix_original = copy.deepcopy(matrix)                     # store for use when player resets game state by pressing 'r'
                                                                # (NOTE: cannot use .copy() since it is a nested list)

    row_mode = not (board_size[1] == 1)                         # True: row mode / False: column mode
    current = [0, 0]                                            # [current row position, current column position] (index for the CORE NOT the whole board)

    info = load_info()                                          # load previous game info (if any)
    if info["seed"] != 0:
        move_count = info["moves"]
    else:
        move_count = 0   

    win = False                                                 # flag that indicates whether a player has won                         


    '''
    -------------------------
        Screens Variables
    -------------------------
    '''

    screen_resize = True                                        # flag that indicates screen resize
    screen_status = -2
    box_width = max(map(len, description + [place]))
    if box_width < 10:
        box_width = 10
    target_rows = len(description) - 1                                     
    content_height, content_width = 3*board_size[0] + 4, 15 + 5*board_size[1] + box_width
                                                                # the height and width of the content
    height_lim, width_lim = (content_height if content_height > 28 else 28), (content_width if content_width > 120 else 120)

    # variables for pausing game
    quit_confirm = False
    quit_menu = True

    # variables for character animation in winning screen 
    ending_animation_played = False
    animation_pos = 0
    charc_moving = False
    charc_head, charc_body, charc_legs = 'Ò', '/█┤', ['/ \\', '║']

    
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
        -   Curses will raise error if screen size is not big enough to display the called function
        -   We have to detect the screen size and tell user to enlarge it when it is too small
        '''
        
        height, width = stdscr.getmaxyx()                           # get the screen size
        center_height, center_width = height // 2, width // 2       # get the center point of screen
        
        
        if (height < 10) or (width < 40):                       
            screen_status = -1                                      # -1 for screen size <= 10x40 (height x width), 0 for screen size <= 25x100, 1 for the else
        elif (height < height_lim) or (width < width_lim):
            screen_status = 0
        else:
            screen_status = 1                                       # flag for displaying game screen

        '''
        --------------------------------------
            Display Screen Size Adjustment
        --------------------------------------
        '''   

        if screen_resize:                                           # clear the screen only when screen status changed 
            screen_resize = False
            stdscr.clear()

            if screen_status == -1:
                stdscr.addstr(0, 0, '⇱')                            # display "⇱⇲" to ask user to enlarge screen
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
            ------------------------
                Display The Lock
            ------------------------
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
                # each row is splited into THREE parts since the CORE grids will be displayed bold while MARGINS will not
                list1 = [f'│ {items[i]} │' if core[0] + v_margin > row >= v_margin else '     ' for i in range(h_margin)]
                list2 = [f'┃ {items[h_margin + i]} ┃' if core[0] + v_margin > row >= v_margin else f'│ {items[h_margin + i]} │' for i in range(core[1])]
                if not row_mode:
                    list2[current[1]] = '│' + list2[current[1]] + '│'
                list3 = [f'│ {items[h_margin + core[1] + i]} │' if core[0] + v_margin > row >= v_margin else '     ' for i in range(h_margin)]
                temp1 = '║  ' + ' '*(row_mode - is_select(row)) + '│'*(is_select(row)) + ''.join(list1)
                temp2 = ''.join(list2)
                temp3 = ''.join(list3) + ' '*(row_mode - is_select(row)) + '│'*(is_select(row)) + '  ║'

                # display
                if core[0] + v_margin > row >= v_margin:                                                # rows in the CORE
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

                else:                                                                                   # rows in the MARGINS
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

            '''
            ---------------------------------------------------
                Display Target / Move Count / Instructions
            ---------------------------------------------------
            '''

            # display level and place
            stdscr.addstr(0, right_index, '╭' + '─'*(box_width//2-2) + f' Lv{level+1:>2} ' + '─'*(box_width//2 + box_width%2 -2) + '╮')
            stdscr.addstr(1, right_index, '│ ' + ' '*(box_width) + ' │')
            stdscr.addstr(2, right_index, '│ ' + f"{place:^{box_width}}" + ' │')
            stdscr.addstr(3, right_index, '│ ' + ' '*(box_width) + ' │')

            # display target
            stdscr.addstr(4, right_index, '├' + '─'*(box_width//2-3) + ' TARGET ' + '─'*(box_width//2 + box_width%2 -3) + '┤')
            stdscr.addstr(5, right_index, '│ ' + ' '*(box_width) + ' │')
            for i, v in enumerate(description):
                stdscr.addstr(6 + i, right_index, '│ ' + f'{v:^{box_width}}' + ' │')
            stdscr.addstr(7 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')

            # display move count
            stdscr.addstr(8 + target_rows, right_index, '├' + '─'*(box_width//2-5) + ' MOVE COUNT ' + '─'*(box_width//2 + box_width%2 -5) + '┤')
            stdscr.addstr(9 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')
            stdscr.addstr(10 + target_rows, right_index, '│ ' + ' '*(box_width//2-5) + f'{move_count:^10}' + ' '*(box_width//2 + box_width%2 -5) + ' │')
            stdscr.addstr(11 + target_rows, right_index, '│ ' + ' '*(box_width) + ' │')

            # display instruction
            stdscr.addstr(12 + target_rows, right_index, '├─' + '─'*box_width + '─┤')
            stdscr.addstr(13 + target_rows, right_index, '│ ' + f"{'R: reset':^{box_width}}" + ' │')
            stdscr.addstr(14 + target_rows, right_index, '│ ' + f"{'M: pause':^{box_width}}" + ' │')
            stdscr.addstr(15 + target_rows, right_index, '╰─' + '─'*box_width + '─╯')


            '''
            ------------------------------------
                Display 'Pause Game?' Prompt
            ------------------------------------
            '''

            if quit_confirm:
                # boundaries
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

            '''
            --------------------------
                Win Condtion Check
            --------------------------
            '''  
            win = check(matrix)       
            
            if win:
                '''
                ------------------------------
                    Display Winning Screen
                ------------------------------
                ''' 

                win_msg = f'{place} is opened! Your friend {name} is free now!'


                if not ending_animation_played:
                    stdscr.clear()                          # for Full Screen display
                    ending_animation_played = True

                # display boundaries
                stdscr.addstr(0, 0, '╭'+'─'*(width-2)+'╮')
                for i in range(1, height-2):
                    stdscr.addstr(i, 0, '│'+' '*(width-2)+'│')
                stdscr.addstr(height - 2, 0, '╰'+'─'*(width-2)+'╯')

                # display messages
                stdscr.addstr(center_height - 2, center_width - len(win_msg) // 2, win_msg, curses.A_BOLD)   
                stdscr.addstr(center_height, center_width - 16, f'You solved the lock in {move_count} moves!')
                stdscr.addstr(center_height + 1, center_width - 12, 'Press \'c\' to continue.')

                # display animation of the friend escaping
                if animation_pos + 1 < width:
                    stdscr.nodelay(1)   # nonblocking
                    stdscr.timeout(75)

                    stdscr.addstr(center_height - 5, animation_pos + 1, charc_head)
                    stdscr.addstr(center_height - 4, animation_pos, charc_body)
                    stdscr.addstr(center_height - 3, animation_pos + 1*int(charc_moving), charc_legs[int(charc_moving)]) 

                    charc_moving = not charc_moving

                    animation_pos += 1
                else:
                    stdscr.nodelay(0)   # blocking
                    for i in range(3, 6):                      # clear lines
                        stdscr.move(center_height - i, 1)
                        stdscr.clrtoeol()
        
        stdscr.refresh()


        '''
        --------------------
            Input Signal
        --------------------
        '''
        c = stdscr.getch()

        if c == curses.KEY_RESIZE:                              # set the flag to True whenever screen is resized
            screen_resize = True


        if screen_status == 1:                                  # input signals in game screen (when screen size is alrge enough)  

            if (not win):                                       # controls allowed when not yet win

                if c == ord('m'):                               # pause game
                    quit_confirm = True

                if c == ord('r'):                               # reset game
                    matrix = copy.deepcopy(matrix_original)
                    row_mode = True
                    current = [0, 0]

                    if info["seed"] != 0:
                        move_count = info["moves"]
                    else:
                        move_count = 0
                    
                    win = False
                    stdscr.clear()

                if c == ord(' '):                              

                    if quit_confirm:                            # (1) as a confirm button when "pausing game" prompt is displayed
                        if quit_menu:
                            load_n_save(in_puzzle=True, matrix=matrix, moves=move_count)
                            break
                        quit_confirm = False
                        stdscr.clear()
                        continue
                        
                    if (1 not in board_size):                   # row and column mode cannot be changed for single row or column board
                        row_mode = not row_mode                 # (2) as a switch mode button
            
                elif c == curses.KEY_LEFT:
                    
                    if quit_confirm:                            # (1) as a control button when "pausing game" prompt is displayed
                        quit_menu = not quit_menu
                        continue

                    if row_mode:                                # (2) as a row rotation button under row mode
                        matrix[v_margin + current[0]] = matrix[v_margin + current[0]][1:] + matrix[v_margin + current[0]][:1]
                        move_count += 1
                    else:                                       # (3) as a column selection button under column mode
                        if current[1] > 0 :
                            current[1] -= 1
                 
                elif c == curses.KEY_RIGHT:

                    if quit_confirm:                            # (1) as a control button when "pausing game" prompt is displayed
                        quit_menu = not quit_menu
                        continue

                    if row_mode:                                # (2) as a row rotation button under row mode
                        matrix[v_margin + current[0]] = matrix[v_margin + current[0]][-1:] + matrix[v_margin + current[0]][:-1]
                        move_count += 1
                    else:                                       # (3) as a column selection button under column mode
                        if current[1] < core[1] - 1:
                            current[1] += 1

                elif (c == curses.KEY_UP) and (not quit_confirm):

                    if row_mode:                                # (1) as a row selection button under row mode
                        if current[0] > 0:
                            current[0] -= 1
                    else:                                       # (2) as a column rotation button under column mode
                        matrix = transpose(matrix)
                        matrix[h_margin + current[1]] = matrix[h_margin + current[1]][1:] + matrix[h_margin + current[1]][:1]
                        matrix = transpose(matrix)
                        move_count += 1

                elif (c == curses.KEY_DOWN) and (not quit_confirm):

                    if row_mode:                                # (1) as a row selection button under row mode
                        if current[0] < core[0] - 1:
                            current[0] += 1
                    else:                                       # (2) as a column rotation button under column mode
                        matrix = transpose(matrix)
                        matrix[h_margin + current[1]] = matrix[h_margin + current[1]][-1:] + matrix[h_margin + current[1]][:-1]
                        matrix = transpose(matrix)
                        move_count += 1
            
            elif c == ord('c'):
                load_n_save(in_puzzle=False, total_moves=move_count, moves=0, matrix=[], seed=0, level=level+1)        # save the result to game file
                break



    stdscr.keypad(False)
    return (quit_confirm and quit_menu)



def generate_level(core, pattern, rand_int, duplicate, place, name, level=0):

    '''
    --------------------------
        Function arguments   
    --------------------------

    [Level Diffuclty settings]

    -   core        [tuple]         the dimension of the CORE grids
    -   pattern     [int]           the number of specific grids in the randomly generated win condition
                                        i.e. 
                                        pattern=5           --> the (randomly generated) win condition will contain a pattern of 5 grids
    -   rand_int    [bool]          the switch for whether the pattern contains only the same or random integer(s)
                                        i.e. 
                                        rand_int = False    --> pattern with same integer
                                        rand_int = True     --> pattern with random integer
    -   duplicate   [bool]          the switch for whether other (supporting) grids contains the integers already in the win condtions
    
    [Story settings]
    -   place       [str]           the trapped location
    -   name        [function]      the name of the trapped friend
    -   level       [int]           the level
    '''

    info = load_info()
    if info["seed"] != 0:
        random.seed(info["seed"])
    else:
        rseed = str(os.urandom(16))
        load_n_save(seed=rseed)
        random.seed(rseed)

    h_margin = 1                        # we only use margin = 1 in the game for now
    v_margin = 1                        # BUT it can potentially contain more margins


    # see explainer/level_generation.txt for more details
    def generate_matrix(wincon):        
        flat_con = [item for row in wincon for item in row] 
        row, col = len(wincon), len(wincon[0])
        board_size = (row+2)*(col+2)

        if not duplicate:
            used_integers = set(flat_con)
            available_integers = ['A', 'B'] + list(set(range(0, 10)) - used_integers)
        else:
            available_integers = ['A', 'B'] + list(range(0, 10))

        flat_con = [random.choice(available_integers) if x == '#' else x for x in flat_con]

        temp = flat_con + [random.choice(available_integers) for i in range((board_size + - row*col - 4))]
        random.shuffle(temp)
        temp = [0] + temp[0:col] + [0] + temp[col:-col] + [0] + temp[-col:] + [0]       # adding corner invisible 0 
        return [temp[i:i+col+2] for i in range(0, board_size, col+2)] 


    # see explainer/level_generation.txt for more details
    def generate_wincon(core, n):                                               # n = pattern
        row, col = core[0], core[1]
        size = row*col                                                          # CORE size
        if n > size - 1:                                                        # prevent pattern overflowing
            n = size - 1

        if rand_int:
            temp = [random.randint(0, 9) for i in range(n)] + ['#']*(size - n)
        else:
            temp = [random.randint(0, 9)]*n + ['#']*(size - n)                  

        random.shuffle(temp)
        return [temp[i:i+col] for i in range(0, size, col)]                     # turn into matrix (nested list)


    win_con = generate_wincon(core, pattern)

    # record positions of '#'
    num_sign_pos = [(i1, i2) for i1, v1 in enumerate(win_con) for i2, v2 in enumerate(v1) if v2 == '#']    

    if info["matrix"] == []:                                                    # use saved matrix if previous save is found
        matrix = generate_matrix(win_con)
    else:
        matrix = info["matrix"]

    def check(matrix):
        temp = get_core(matrix, core, h_margin, v_margin)
        for p1, p2 in num_sign_pos:
            temp[p1][p2] = '#'
        return temp == win_con
            

    return matrix, core, h_margin, v_margin, generate_description(win_con, 'Where # is anything'), check, level, place, name



if __name__ == '__main__':
    curses.wrapper(lock, *generate_level((3, 4), 8, True, True, 'CPD. LG-01', 'Dirk'))
