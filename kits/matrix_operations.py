def transpose(matrix) -> list: 
    return [list(t) for t in zip(*matrix)]


def get_core(matrix, core, h_margin, v_margin) -> list:
    return [row[h_margin: h_margin + core[1]] for row in matrix[v_margin: v_margin + core[0]]]

# deprecated
def check_multiple(multiple, matrix, core, h_margin, v_margin) -> tuple:
    # multiple = the desired multiple to check

    row_indices, column_indices = [], []    # (row indices in core grids, column indices in core grids)
    
    for i, row in enumerate(get_core(matrix, core, h_margin, v_margin)):
        if not [0 for item in row if item % multiple != 0]:
            row_indices += [i]

    for i, row in enumerate(get_core(transpose(matrix), core, h_margin, v_margin)):
        if not [0 for item in row if item % multiple != 0]:
            column_indices += [i]

    return row_indices, column_indices


def generate_description(win_con, add_str=''):
    if add_str:
        temp = [' '.join(map(str, x)) for x in win_con] + [add_str]
    else:
        temp = [' '.join(map(str, x)) for x in win_con]
    return list(map(lambda x: f'{x:^10}', temp))




if __name__ == '__main__':
    
    matrix = [                          
        [0, 0, 0, 0, 0, 0, 0], 
        [0, 3, 6, 3, 6, 3, 0],              
        [0, 3, 2, 9, 2, 7, 0], 
        [0, 3, 2, 9, 2, 7, 0],
        [0, 6, 6, 6, 6, 6, 0],
        [0, 3, 2, 3, 2, 7, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    core = (5, 5)                       # (num of row, num of column)
    h_margin = 1
    v_margin = 1

    row_indices, column_indices = check_multiple(2, matrix, core, h_margin, v_margin)
    print(f'\nWhole line with multiple of 2:')
    print(f'Row:    {row_indices}')
    print(f'Column: {column_indices}\n')

    row_indices, column_indices = check_multiple(3, matrix, core, h_margin, v_margin)
    print(f'\nWhole line with multiple of 3:')
    print(f'Row:    {row_indices}')
    print(f'Column: {column_indices}\n')


    #print(*transpose(transpose(matrix)), sep='\n')
