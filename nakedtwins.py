
'''---------------------------------------------------utils.py------------------------------------------------'''
from collections import defaultdict
import copy
from copy import deepcopy


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]
history = {}  # history must be declared here so that it exists in the assign_values scope


def extract_units(unitlist, boxes):
    """Initialize a mapping from box names to the units that the boxes belong to

    Parameters
    ----------
    unitlist(list)
        a list containing "units" (rows, columns, diagonals, etc.) of boxes

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    units = defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                # defaultdict avoids this raising a KeyError when new keys are added
                units[current_box].append(unit)
    return units


def extract_peers(units, boxes):
    """Initialize a mapping from box names to a list of peer boxes (i.e., a flat list
    of boxes that are in a unit together with the key box)

    Parameters
    ----------
    units(dict)
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a set
        containing all boxes that are peers of the key box (boxes that are in a unit
        together with the key box)
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    peers = defaultdict(set)  # set avoids duplicates
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    # defaultdict avoids this raising a KeyError when new keys are added
                    peers[key_box].add(peer_box)                
    return peers


def assign_value(values, box, value):
    """You must use this function to update your values dictionary if you want to
    try using the provided visualization tool. This function records each assignment
    (in order) for later reconstruction.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    prev = values2grid(values)
    values[box] = value
    if len(value) == 1:
        history[values2grid(values)] = (prev, (box, value))
    return values

def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]


def values2grid(values):
    """Convert the dictionary board representation to as string

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    """
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid):
    """Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def display(values):
    """Display the values as a 2-D grid.

    Parameters
    ----------
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()


def reconstruct(values, history):
    """Returns the solution as a sequence of value assignments 

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    history(dict)
        a dictionary of the form {key: (key, (box, value))} encoding a linked
        list where each element points to the parent and identifies the value
        assignment that connects from the parent to the current state

    Returns
    -------
    list
        a list of (box, value) assignments that can be applied in order to the
        starting Sudoku puzzle to reach the solution
    """
    path = []
    prev = values2grid(values)
    while prev in history:
        prev, step = history[prev]
        path.append(step)
    return path[::-1]


import copy
from copy import deepcopy

'''--------------------------------------------------Solution.py------------------------------------------------'''
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

diagonal_units = [[rows[i]+cols[i] for i in range(0,9)]]
i = 8
diagonals=[]
for r in rows:
    diagonals.append(r+cols[i])
    i=i-1
diagonal_units.append(diagonals)
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def naked_twins(values):
   
    if(values is None):
        return False
    values_out = deepcopy(values)
    
    for key1 in values:
        if(len(values[key1])==2):
            for key2 in units[key1]:
                for key_box in key2:
                    if((values[key1] == values[key_box]) and (key1!=key_box)):
                        for peer_key in key2:
                            if(peer_key!=key_box and peer_key!=key1):
                                values_out[peer_key] = values_out[peer_key].replace(''+(values[key1])[0],'')
                                values_out[peer_key] = values_out[peer_key].replace(''+(values[key1])[1],'')
   return values_out

def eliminate(values):    
    for x in values: 
        if(len(values[x])==1):
            for peer in peers[x]:
                values[peer] = values[peer].replace(''+values[x],'')            
    return values

def only_choice(values):
    s = "123456789"
    for unit in unitlist:
        for x in range(0,9):
            count = 0
            for unitbox in unit:
                if(s[x] in values[unitbox]):
                    count = count+1
                    temp = unitbox
            if(count == 1):
                values[temp] = s[x]                
    return values



def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
                


def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:        
        return False ## Failed earlier
    
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    minlen,minbox = min((len(values[b]),b) for b in boxes if len(values[b])>1)   
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[minbox]:
        new_sudoku = deepcopy(values)
        new_sudoku[minbox] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
