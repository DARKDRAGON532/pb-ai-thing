# import required module
import chess
import random

# create board object
board=chess.Board()


def staticAnalysis(board, move,color):
    score = 0           
        ## Check some things about this move:
        # score += 10 if board.is_capture(move) else 0
        # To actually make the move:
    board.push(move)
        # Now check some other things:
    for (piece, value) in [(chess.PAWN, 1),
                            (chess.BISHOP, 4),
                            (chess.KING, 0),
                            (chess.QUEEN, 10),
                            (chess.KNIGHT, 5),
                        (chess.ROOK, 5)]:
        score += len(board.pieces(piece, color)) * value
        score -= len(board.pieces(piece, not color)) * value
            # can also check things about the pieces position here
    return score

class ChessAI:
    board=chess.Board()
    
    def __init__(self, color):
            self.color = color
        
            self.color= 0 if color.lower() == "b" else 1
    

    def add_move(self,move:str):
            board.push(chess.Move.from_uci(move))
            print(board)
  
            pass        

    def make_move(self):
        # while board.is_game_over:

            if int(self.color) == 0:

                board.turn = False
            else:
                board.turn = True

            movelist = list(board.legal_moves)
            max = 0
            l = []


            for a in movelist:
                newboard_1 = board.copy()
                newboard_1.push(a)
                legal_moves_after_1st_move = list(newboard_1.legal_moves)
                l1 = []

                if newboard_1.is_stalemate():
                    l.append([[0]])
                    continue
                if newboard_1.is_checkmate():
                    l.append([[10**10]])
                    continue
                for b in legal_moves_after_1st_move:
                    # New board 2 is board with 1 piece changed
                    newboard_2= newboard_1.copy()
                    newboard_2.push(b)

                    legal_moves_after_2nd_move = list(newboard_2.legal_moves)
                    l2 = []
                    if newboard_2.is_checkmate():
                        l1.append([-10**10])

                    for c in legal_moves_after_2nd_move:
                        newboard_3 = newboard_2.copy()
                        # New board 3 is board with 2 pieces changed
                        if int(self.color) == 1:
                            temp_score = staticAnalysis(newboard_3,c,chess.WHITE)
                        elif int(self.color) == 0:
                            temp_score = staticAnalysis(newboard_3,c,chess.BLACK)
                        l2.append(temp_score)

                        # Finding the max score
                        if temp_score>=max:
                            move1,move2,move3 = a,b,c
                            max = temp_score

                        # l2 contains all scores for third move
                        # l2 means depth is 2

                    l1.append(l2)

                    # l1 contains nested list of all possible scores after second move
                    # l1 means depth is 1

                l.append(l1)
                # l contains nested nested list of all possible scores after 1st move
                # l means depth is 0

            # Mini Max Begins
            # Step 1 : Finding maximimum score from l2
            newl = []
            for l1 in l:
                max_values_from_all_l2 = []

                for l2 in l1:
                    max = -10**10
                    for i in l2:
                        if i >= max:
                            max = i

                    max_values_from_all_l2.append(max)

                newl.append(max_values_from_all_l2)
            #print('\n\n')
                # newl is nested list of all l1 with max_values of all l2
                # basically newl is the new l.

            # Step 2 : Finding the miniumn score from all l1
            final= []
            for l1 in newl:
                min = 10**10
                for i in l1:
                    if i <= min:
                        min = i
                final.append(min)
            # final is basically new l .

            # Step 3 : Finding the maximum score from final
            dict1 = {}
            for i,j in zip(movelist,final):
                dict1[str(i)] = j


            #If all most optimal elements are same then take random move

            max =-1000000
            
            for i in dict1.items():
                if i[1]>max:
                    max = i[1]
                    

            temp_list = []
            for i in dict1.items():
                if i[1]==max:
                    temp_list.append(i[0])

            move = random.choice(temp_list)

            # move is the optimal move to be made

            # print("AI Moved the piece from", move[:2], 'to', move[2:] , '\n\n\n')

            board.push(chess.Move.from_uci(move))
            print(board)


            return move
