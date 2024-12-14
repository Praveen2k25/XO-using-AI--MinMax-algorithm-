from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)


board = [[" ", " ", " "] for _ in range(3)]
current_player = "X" 
game_over = False
winner = None

def check_winner(player):

    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def is_board_full():

    return all(all(cell != " " for cell in row) for row in board)

def minimax(depth, is_maximizing):

    if check_winner("O"):
        return 1  
    if check_winner("X"):
        return -1  
    if is_board_full():
        return 0  

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"  
                    score = minimax(depth + 1, False)
                    board[i][j] = " "  
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(depth + 1, True)
                    board[i][j] = " "  
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = float('-inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"  
                score = minimax(0, False)
                board[i][j] = " " 
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move != (-1, -1):
        board[best_move[0]][best_move[1]] = "O" 
        return best_move
    return None, None  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_player_move():
    global current_player, game_over, winner

    if game_over:
        return jsonify({'status': 'Game Over', 'winner': winner})

    data = request.get_json()
    row = data['row']
    col = data['col']

    if board[row][col] == " ":
        board[row][col] = current_player
        if check_winner(current_player):
            winner = current_player
            game_over = True
            return jsonify({'status': 'Winner', 'winner': winner})

        elif is_board_full():
            game_over = True
            return jsonify({'status': 'Draw'})

        else:
            current_player = "O"  
            ai_row, ai_col = ai_move()  
            if check_winner("O"):
                winner = "O"
                game_over = True
                return jsonify({'status': 'Winner', 'winner': winner})
            elif is_board_full():
                game_over = True
                return jsonify({'status': 'Draw'})
            else:
                current_player = "X"  
                return jsonify({'status': 'Next Move', 'player': current_player, 'ai_row': ai_row, 'ai_col': ai_col})

    return jsonify({'status': 'Invalid Move'})

@app.route('/reset', methods=['POST'])
def reset_game():
    global board, current_player, game_over, winner
    board = [[" ", " ", " "] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None
    return jsonify({'status': 'Reset'})

if __name__ == '__main__':
    app.run(debug=True)
