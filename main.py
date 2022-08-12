import sys
from importlib.machinery import SourceFileLoader
import requests

def send_move(move, colour):
    res = requests.post("http://localhost:8080/move", json={"move": move, "colour": colour})
    try:
        res = res.json()
    except:
        pass
    if type(res) != requests.Response:
        if res["error"]:
            if res["error"] == 1:
                print(f"Error: Invalid move by {colour}")
                sys.exit()
            elif res["error"] == 2:
                print("Game over")
                sys.exit()


bot1 = SourceFileLoader(sys.argv[1].split("/")[-1], sys.argv[1]).load_module()
bot2 = SourceFileLoader(sys.argv[2].split("/")[-1], sys.argv[2]).load_module()

white = bot1.ChessAI("w")
black = bot2.ChessAI("b")

requests.post("http://localhost:8080/new")
requests.post("http://localhost:8080/teams", json={"team1": sys.argv[1].split("/")[-1].removesuffix(".py"), "team2": sys.argv[2].split("/")[-1].removesuffix(".py"), "round": input("enter round: ")})

while True:
    white_move = white.make_move()
    send_move(white_move, "w")
    black.add_move(white_move)
    # input("Press Enter to continue...")
    black_move = black.make_move()
    send_move(black_move, "b")
    white.add_move(black_move)
    # input("Press Enter to continue...")