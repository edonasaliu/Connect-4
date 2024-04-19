def create_board():
    """Create a 6x7 board for Connect 4."""
    return [[' ' for _ in range(7)] for _ in range(6)]

def show_board(board):
    """Display the board to the console."""
    print('  '.join(map(str, range(1, 8))))  # Column numbers
    for row in board:
        print('|' + '|'.join(row) + '|')

def make_move(board, col, token):
    """Place a token in the chosen column."""
    for row in reversed(range(6)):
        if board[row][col] == ' ':
            board[row][col] = token
            return board
    return board  # If column is full, return the board unchanged

def possible_moves(board):
    """Return a list of columns that are not full."""
    return [col for col in range(7) if board[0][col] == ' ']

def is_terminal(board):
    """Check if the game is over (win or full board)."""
    return check_win(board)[0] or all(board[0][col] != ' ' for col in range(7))

def utility(board, player):
    """Evaluate the board state."""
    winner = check_win(board)
    if winner[0]:
        if winner[1] == player:
            return 1000  # Favorable outcome
        else:
            return -1000  # Unfavorable outcome
        
    o_3_in_a_row = count_consecutive(board, 3, 'O')
    o_2_in_a_row = count_consecutive(board, 2, 'O') - o_3_in_a_row
    x_3_in_a_row = count_consecutive(board, 3, 'X')
    x_2_in_a_row = count_consecutive(board, 2, 'X') - x_3_in_a_row

    diff = abs((3 * o_2_in_a_row + 9 * o_3_in_a_row) - (3 * x_2_in_a_row + 9 * x_3_in_a_row))
    if player == "X":
        diff = -diff
    return diff

def count_consecutive(board, length, symbol):
    count = 0
    rows = len(board)
    cols = len(board[0])

    # Check horizontally
    for row in board:
        count += count_in_line(row, length, symbol)

    # Check vertically
    for col in range(cols):
        column = [board[row][col] for row in range(rows)]
        count += count_in_line(column, length, symbol)

    # Check diagonals from top-left to bottom-right
    for start in range(rows + cols - 1):
        diagonal = []
        for row in range(rows):
            col = start - row
            if 0 <= col < cols:
                diagonal.append(board[row][col])
        count += count_in_line(diagonal, length, symbol)

    # Check diagonals from top-right to bottom-left
    for start in range(-rows + 1, cols):
        diagonal = []
        for row in range(rows):
            col = start + row
            if 0 <= col < cols:
                diagonal.append(board[row][col])
        count += count_in_line(diagonal, length, symbol)

    return count

def count_in_line(line, length, symbol):
    """
    Counts the number of consecutive occurrences of a given symbol in a line.

    Args:
        line (list): The line to search for consecutive occurrences.
        length (int): The desired length of consecutive occurrences.
        symbol: The symbol to count.

    Returns:
        int: The number of times the symbol appears consecutively in the line.
    """
    count = 0
    consecutive = 0
    for value in line:
        if value == symbol:
            consecutive += 1
            if consecutive == length:
                count += 1
        else:
            consecutive = 0
    return count

def check_win(board):
    """Check for a win in all directions."""
    # Horizontal, vertical, and diagonal checks
    sequences = ['XXXX', 'OOOO']

    # Horizontal
    for row in board:
        for col in range(4):
            if ''.join(row[col:col+4]) in sequences:
                return True, row[col]

    # Vertical
    for col in range(7):
        for row in range(3):
            if ''.join([board[r][col] for r in range(row, row+4)]) in sequences:
                return True, board[row][col]

    # Positive diagonals
    for col in range(4):
        for row in range(3):
            if ''.join([board[row+i][col+i] for i in range(4)]) in sequences:
                return True, board[row][col]

    # Negative diagonals
    for col in range(4):
        for row in range(3, 6):
            if ''.join([board[row-i][col+i] for i in range(4)]) in sequences:
                return True, board[row][col]

    return False, None
