from time import sleep
import requests
import chess
import random
from time import sleep  
board = chess.Board()
while board.is_game_over() == False:
    move=str(random.choice([move for move in board.legal_moves]))
    print(move)
    requests.post("http://localhost:8080/move", json={"move": move, "colour":"w"})
    board.push_uci(move)
if input("new? : ") == "y":requests.post("http://localhost:8080/new")