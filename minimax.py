PLAYER = 'X'              # 'X', 'O'
DIFFICULTY = 'HARD'       # 'EASY', 'MEDIUM', 'HARD'
MISERE_MODE = False


def game_loop():
  global COMPUTER
  COMPUTER = 'O' if PLAYER == 'X' else 'X'

  board = create_new_board()
  current_player = PLAYER
  turn = 1

  print('\nBoard')
  print_board(board)

  while True:
    row, col = None, None

    if current_player == PLAYER:
      try:
        row = int(input('\nEnter the row number (1-3): ')) - 1
        col = int(input('Enter the column number (1-3): ')) - 1
      except:
        print('Invalid input.')
        continue
    else:
      row, col = minimax(board, current_player)[0]

    try:
      board = get_action_result(board, row, col, current_player)
    except ValueError as error:
      print(error)
      continue

    print(f'\nTurn {turn} ({"player" if current_player == PLAYER else "computer"})')
    print_board(board)

    turn += 1

    if not check_if_is_final_board(board):
      current_player = PLAYER if current_player == COMPUTER else COMPUTER
      continue

    print_result(board)
    break


def print_result(board):
    winner = verify_winner(board, False)
    result = '\n************\n'
    if winner == PLAYER:
      result += 'YOU WIN!'
    elif winner == COMPUTER:
      result += 'You lose...'
    else:
      result += 'TIE!'
    result += '\n************\n'
    print(result)


def create_new_board():
  return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

def clone_board(board):
  return [row[:] for row in board]

def print_board(board):
  print('-------------')
  for i in range(3):
    print('|', end='')
    for j in range(3):
      print(' ' + board[i][j] + ' |', end='')
    print('\n-------------')

def check_if_is_empty_cell(board, row, col):
  return board[row][col].strip() == ''


def get_possible_actions(board):
  actions = []
  for i in range(3):
    for j in range(3):
      if check_if_is_empty_cell(board, i, j):
        actions.append([i, j])
  return actions

def get_action_result(board, row, col, current_player):
  if row > 2 or row < 0 or col > 2 or col < 0:
    raise ValueError('Invalid cell. Try again.')
  if not check_if_is_empty_cell(board, row, col):
    raise ValueError('The cell is already filled. Try again.')
  board = clone_board(board)
  board[row][col] = current_player
  return board


def verify_winner(board, ignore_misere = True):
  winner = None

  # Check horizontally and vertically:
  for i in range(3):
    if board[i][0] == board[i][1] == board[i][2] and not check_if_is_empty_cell(board, i, 0):
      winner = board[i][0]
    elif board[0][i] == board[1][i] == board[2][i] and not check_if_is_empty_cell(board, 0, i):
      winner = board[0][i]

  # Check diagonally:
  if winner == None:
    if board[0][0] == board[1][1] == board[2][2] and not check_if_is_empty_cell(board, 0, 0):
      winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and not check_if_is_empty_cell(board, 0, 2):
      winner = board[0][2]

  if MISERE_MODE and winner != None and not ignore_misere:
    winner = PLAYER if winner == COMPUTER else COMPUTER

  return winner


def check_if_is_final_board(board):
  if verify_winner(board) != None:
    return True
  for i in range(3):
    for j in range(3):
      if check_if_is_empty_cell(board, i, j):
        return False
  return True


def calc_cost(board):
  winner = verify_winner(board)
  if winner == None:
    return 0
  result = 1 if winner == PLAYER else -1
  return result if not MISERE_MODE else result * (-1)


def minimax(board, current_player, current_level = 1):
  actions_and_costs = []
  possible_actions = get_possible_actions(board)

  for action in possible_actions:
    resulting_board = get_action_result(board, action[0], action[1], current_player)
    cost = None

    has_reached_max_level = \
      (DIFFICULTY == 'EASY' and current_level >= 3) \
      or (DIFFICULTY == 'MEDIUM' and current_level >= 6)

    if has_reached_max_level or check_if_is_final_board(resulting_board):
      cost = calc_cost(resulting_board)
    else:
      new_player = PLAYER if current_player == COMPUTER else COMPUTER
      new_level = current_level + 1
      cost = minimax(resulting_board, new_player, new_level)[1]

    actions_and_costs.append([action, cost])

  if current_player == PLAYER:
    return get_max_value(actions_and_costs)
  return get_min_value(actions_and_costs)


def get_max_value(actions_and_costs):
  result_action_and_cost = actions_and_costs[0]
  for i in range(1, len(actions_and_costs)):
    if actions_and_costs[i][1] > result_action_and_cost[1]:
      result_action_and_cost = actions_and_costs[i]
  return result_action_and_cost

def get_min_value(actions_and_costs):
  result_action_and_cost = actions_and_costs[0]
  for i in range(1, len(actions_and_costs)):
    if actions_and_costs[i][1] < result_action_and_cost[1]:
      result_action_and_cost = actions_and_costs[i]
  return result_action_and_cost


def main():
  game_loop()

if __name__ == '__main__':
  main()
