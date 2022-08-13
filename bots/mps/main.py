import chess
from engine import ChessAI

def user_move(color, board):                   #pushes move by user on the board 
    print(board)
    smove=input("Enter move:")
    move=ChessAI(color).add_move(board,smove)
    return move

def ai_move(color, board):                          #pushes the ai move on board
    print(board)
    move = chess.Move.from_uci(ChessAI(color).make_move(board))
    board.push(move)
    return str(move)

def main(color, board, fname):                      #main function
    while True:
        file = open(f"data/{fname}", "a")
        if color == "b":
            umove=user_move(color, board)
            file.write(umove+"\n")
            amove=ai_move(color, board)
            file.write(amove + "\n")
        elif color == "w":
            amove=ai_move(color, board)
            file.write(amove+"\n")
            umove=user_move(color, board)
            file.write(umove + "\n")

        if board.is_checkmate():
            print(board.outcome())
        elif board.is_stalemate() or board.is_insufficient_material():
            print("Match draw")
        file.close()

board = chess.Board()                                    #defines the board
user_color = input("Enter color(w or b):")
filename = input("Enter filename to save the game:")
while True:
    if user_color == "w":
        ai_color = "b"
        break
    elif user_color == "b":
        ai_color = "w"
        break
    else:
        print("Invalid Move")
main(ai_color, board, filename)
