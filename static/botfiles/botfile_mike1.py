import random 

board = [
    [-1, -1, -1, -1, -1],
    [-1,  0,  0,  0, -1],
    [ 1,  0,  0,  0, -1],
    [ 1,  0,  0,  0,  1],
    [ 1,  1,  1,  1,  1]
]


movement_counter = 0
diag_pos = [(1,1), (1, 3), (3,1), (3,3)]

first_bot = random.choice([1, -1])
second_bot = -first_bot

def display():
    for row in board:
        for cell in row:
            if cell == -1:
                print("R", end=" ")  #red piece
            elif cell == 0:
                print(".", end=" ")
            elif cell == 1:
                print("B", end=" ")  #blue piece
        print()

    
def get_position(color): #parameter color: "-1" as red and "1" as blue
    positions = []
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == color:
                positions.append((row, column))
    return positions


def is_valid_move(piece_position):
    row, column = piece_position
    valid_moves = []
    movement = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    movement2 = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
    if (row, column) in diag_pos:
        for prob_row, prob_column in movement2:
            new_row = row + prob_row
            new_column = column + prob_column
            if 0 <= new_row < len(board) and 0 <= new_column < len(board[0]) and board[new_row][new_column] == 0:
                valid_moves.append((new_row, new_column))
    else:
        for prob_row, prob_column in movement:
            new_row = row + prob_row
            new_column = column + prob_column
            if 0 <= new_row < len(board) and 0 <= new_column < len(board[0]) and board[new_row][new_column] == 0:
                valid_moves.append((new_row, new_column))
    return valid_moves

def ganh(color, position):
    print('ganh activated')
    row, column = position
    valid_remove = []
    opp_remove = []
    chet_pair = [[(1,0), (-1, 0)], [(0,1), (0, -1)]]
    chet_pair2 = [[(1,0), (-1, 0)], [(0,1), (0, -1)], [(1,1), (-1,-1)], [(-1,1), (1,-1)]]


    if (row, column) in diag_pos:
        print('ganh diag condition met')

        for pairs in chet_pair2:
            for check_row, check_column in pairs:
                opp_row = row + check_row
                opp_column = column + check_column

                if 0 <= opp_row < len(board) and 0 <= opp_column < len(board[0]):
                    if board[opp_row][opp_column] == -color:
                        opp_remove.append((opp_row, opp_column))

            if len(opp_remove) < 2:
                opp_remove = []
            else:
                for removal in opp_remove:
                    valid_remove.append(removal)
                opp_remove = []
    else:
        for pairs in chet_pair:
            for check_row, check_column in pairs:
                opp_row = row + check_row
                opp_column = column + check_column
                if 0 <= opp_row < len(board) and 0 <= opp_column < len(board[0]):
                    if board[opp_row][opp_column] == -color: #index out of range error
                        opp_remove.append((opp_row, opp_column))

            if len(opp_remove) < 2:
                opp_remove = []
            else:
                for removal in opp_remove:
                    valid_remove.append(removal)
                    print('chet passed!')
                opp_remove = []

    return valid_remove

def chet(color, position):
    print('chet activated')

    row, column = position
    valid_remove = []
    opp_verified = []
    diagnal = [(-1, 1), (1, -1), (1, 1), (-1, -1)]
    non_diagnal = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    
    for psbl_row , psbl_column in diagnal:
        opp_row = row + psbl_row
        opp_column = column + psbl_row
        if 1 <= opp_row < len(board) -1 and 1 <= opp_column < len(board[0]) - 1:
            if board[opp_row][opp_column] == -color:
                if (opp_row, opp_column) in diag_pos:
                    opp_verified.append((opp_row, opp_column))
                else:
                    pass
        if opp_verified:
            ally_row = opp_row + psbl_row
            ally_column = opp_column + psbl_column
            if board[ally_row][ally_column] == color:
                valid_remove.append((opp_row, opp_column))
                print('ganh passed!')
            opp_verified = []
        else:
            opp_verified = []
      
    for psbl_row , psbl_column in non_diagnal:
        opp_row = row + psbl_row
        opp_column = column + psbl_row
        if 1 <= opp_row < len(board) -1 and 1 <= opp_column < len(board[0]) - 1:
            if board[opp_row][opp_column] == -color:
                opp_verified.append((opp_row, opp_column))

        if opp_verified:
            ally_row = opp_row + psbl_row
            ally_column = opp_column + psbl_column
            if board[ally_row][ally_column] == color:
                valid_remove.append((opp_row, opp_column))
                print('ganh passed!')
            opp_verified = []
        else:
            opp_verified = []

    return valid_remove

def order_66(board, valid_chet=None, valid_ganh=None):
    execute = []
    print(valid_chet)
    print(valid_ganh)
    

    if valid_chet:
        execute.extend(valid_chet)
    
    if valid_ganh:
        execute.extend(valid_ganh)
    print(execute)

    for row, column in execute:
        board[row][column] = 0
    print(board)

    return board


while True:
    display()
    my_positions = get_position(1)
    opponent_positions = get_position(-1)

    if not my_positions:
        print('end game')
    if not opponent_positions:
        print('end game')

    if movement_counter%2 == 0:
        piece_positions = my_positions
        selected_color = 1
    else:
        selected_color = -1
        piece_positions = opponent_positions
    
    position_select = random.choice(piece_positions)
    valid_move = is_valid_move(position_select)

    input('enter to continue... ')

    if valid_move:
        new_position = random.choice(valid_move)
        board[position_select[0]][position_select[1]] = 0
        board[new_position[0]][new_position[1]] = selected_color
        valid_ganh_remove = ganh(selected_color, new_position)
        valid_chet_remove = chet(selected_color, new_position)
        board = order_66(board, valid_chet_remove, valid_ganh_remove)
        movement_counter += 1
        
    else:
        print('bot could not find a valid destination')


    