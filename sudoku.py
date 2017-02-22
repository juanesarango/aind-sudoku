rows = 'ABCDEFGHI'
cols = '123456789'

# Easy sudoku
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

# Random sudoku
grid = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'

# Hard sudoku
grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'


def cross(a, b):
    return [s + t for s in a for t in b]


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in chunks(rows, 3) for cs in chunks(cols, 3)]

unitlist = row_units + col_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def grid_values(sudoku_string, wild_card='.'):
    """
    Convert grid string into {<box>: <value>} dict with '123456789'
    value for empties.

    Args:
        sudoku_string: A string of 81 characters long with the
        starting numbers for all the boxes in a sudoku. Empty
        boxes can be representated as dots `.`.
        Example: `'...3.2.6.'...`

    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.


    Answer from aind:
        return dict(zip(boxes, sudoku_string))
    """

    assert len(sudoku_string) == 81, "The length of `grid` should be 81. A 9x9 sudoku."
    sudoku_dict = {}
    for index, letter in enumerate(sudoku_string):
        sudoku_dict[boxes[index]] = letter if letter != wild_card else '123456789'
    return sudoku_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print('\n')
    return


def eliminate(sudoku_dict):
    """
    Returns a sudoku dict after applying the eliminate technique.

    Args:
        sudoku_dict: A dict representing the sudoku. It'll contain
        in each box the value of it, or the possible values.

    Returns:
        A sudoku dict after applying the eliminate technique in all
        the boxes.
    """
    for box, value in sudoku_dict.items():
        if len(value) == 1:
            for peer in peers[box]:
                sudoku_dict[peer] = sudoku_dict[peer].replace(value, '')
    return sudoku_dict


def only_choice(sudoku_dict):
    """
    It runs through all the units of a sudoku
    and it applies the only choice technique.

    Args:
        sudoku_dict: A dict representing the sudoku.
    Returns:
        A sudoku dict after applying the only choice technique.
    """
    # for box, value in sudoku_dict.items():
    #     for unit in units[box]:
    #         for possible_value in '123456789':
    #             sudoku_dict[box] = possible_value if sum([1 if possible_value in sudoku_dict[item] else 0 for item in unit]) == 1 else value  # noqa
    # return sudoku_dict

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in sudoku_dict[box]]
            if len(dplaces) == 1:
                sudoku_dict[dplaces[0]] = digit
    return sudoku_dict


def reduce_puzzle(sudoku_dict):
    """
    Uses constrain propagation to reduce the search space
    Args:
        sudoku_dict: A dict representing the sudoku.
    Returns:
        A sudoku dict solved or partially solved
    """
    count = 0
    stalled = False
    while max(len(sudoku_dict[s]) for s in boxes) > 1 and not stalled:
        initial_state = sudoku_dict.copy()
        sudoku_dict = eliminate(sudoku_dict)
        sudoku_dict = only_choice(sudoku_dict)
        count += 1
        stalled = initial_state == sudoku_dict
        if min(len(sudoku_dict[s]) for s in boxes) == 0:
            return False
    return sudoku_dict


def search(sudoku_0):
    # Using depth-first search and propagation, create a search tree and solve the sudoku."

    # First, reduce the puzzle using the previous function
    sudoku_0 = reduce_puzzle(sudoku_0)
    if not sudoku_0:
        return False
    if sudoku_is_solved(sudoku_0):
        return sudoku_0

    # Choose one of the unfilled squares with the fewest possibilities
    chosen_box = find_better_box(sudoku_0)

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for value in sudoku_0[chosen_box]:
        sudoku_1 = sudoku_0.copy()
        sudoku_1[chosen_box] = value
        sudoku_2 = search(sudoku_1)
        if sudoku_2:
            return sudoku_2


def sudoku_is_solved(sudoku_dict):
    len_boxes = [len(sudoku_dict[s]) for s in boxes]
    return min(len_boxes) == 1 and max(len_boxes) == 1


def find_better_box(sudoku_dict):
    len_boxes = [s for s in boxes if len(sudoku_dict[s]) > 1]
    min_length = min(len(sudoku_dict[s]) for s in len_boxes)
    min_len_box = [s for s in len_boxes if len(sudoku_dict[s]) == min_length]
    return min_len_box[0]


def naked_twins(sudoku_dict):
    pass


# Metodo #1 eliminar hasta que solo quede cada box con 1 número
def method_1():
    display(grid_values(grid, ','))
    sudoku_dict = grid_values(grid)
    count = 0
    while max(len(sudoku_dict[s]) for s in boxes) > 1:
        sudoku_dict = eliminate(sudoku_dict)
        count += 1
    display(sudoku_dict)
    print('METODO 1: Fue resuelto en {} iteraciones'.format(count))


# Metodo #2 eliminar y utilizar única opción
def method_2():
    display(grid_values(grid, ','))
    sudoku_dict = grid_values(grid)
    count = 0
    while max(len(sudoku_dict[s]) for s in boxes) > 1:
        sudoku_dict = eliminate(sudoku_dict)
        sudoku_dict = only_choice(sudoku_dict)
        count += 1
    display(sudoku_dict)
    print('METODO 2: Fue resuelto en {} iteraciones'.format(count))


# Metodo #3 Aplicar constraints propagation de eliminar y utilizar única opción
def method_3():
    display(grid_values(grid, ','))
    sudoku_dict = grid_values(grid)
    sudoku_dict = reduce_puzzle(sudoku_dict)
    if sudoku_dict:
        display(sudoku_dict)
    else:
        print("METODO 3: No es posible resolver el sudoku por este metodo")


def method_4():
    display(grid_values(grid, ','))
    sudoku_dict = grid_values(grid)
    sudoku_dict = search(sudoku_dict)
    if sudoku_dict:
        display(sudoku_dict)
    else:
        print("METODO 4: No es posible resolver el sudoku por este metodo")


# method_1()
# method_2()
# method_3()
method_4()
