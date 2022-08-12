import re, time
from itertools import count
from collections import namedtuple as nmd
import chess
import random
pval = { 'P': 10*10, 'N': 28*10, 'B': 32*10, 'R': 48*10, 'Q': 93*10, 'K': 6000*10 }

# mapping values

pst={'P':[0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0],'N':[-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69],'B':[-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10],'R':[35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32],'Q':[6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42],'K':[4,54,47,-99,-99,60,83,-62,-32,10,55,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-55,-43,-52,-28,-51,-47,-8,-50,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,17,30,-3,-14,6,-1,40,18]}


for k, t in pst.items():
    pd = lambda row: (0,) + tuple(x+pval[k] for x in row) + (0,)
    pst[k] = sum((pd(t[i*8:i*8+8]) for i in range(8)), ())
    pst[k] = (0,)*20 + pst[k] + (0,)*20

treeparam1, treeparam2, treeparam3, treeparam4 = 91, 98, 21, 28

N, E, S, W = -10, 1, 10, -1

directions = {
    'P': (N, N+N, N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}

lowerbound = pval['K'] - 10*pval['Q']
upperbound = pval['K'] + 10*pval['Q']

maxttsize = 1e7

class Board(nmd('Board', 'bd score castlingrights bc ep kp')):

    def generator(self):
        for i, p in enumerate(self.bd):
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.bd[j]
                    if q.isspace() or q.isupper(): break
                    if p == 'P' and d in (N, N+N) and q != '.': break
                    if p == 'P' and d == N+N and (i < treeparam1+N or self.bd[i+N] != '.'): break
                    if p == 'P' and d in (N+W, N+E) and q == '.' \
                            and j not in (self.ep, self.kp, self.kp-1, self.kp+1): break
                    yield (i, j)
                    if p in 'PNK' or q.islower(): break
                    if i == treeparam1 and self.bd[j+E] == 'K' and self.castlingrights[0]: yield (j+E, j+W)
                    if i == treeparam2 and self.bd[j+W] == 'K' and self.castlingrights[1]: yield (j+W, j+E)
    def move(self, move):
        i, j = move
        p, q = self.bd[i], self.bd[j]
        put = lambda bd, i, p: bd[:i] + p + bd[i+1:]
        bd = self.bd
        (castlingrights,    bc,    ep,    kp)       = self.castlingrights  , self.bc,    0,     0
        score = self.score + self.value(move)
        bd = put(bd, j, bd[i])
        bd = put(bd, i, '.')
        if i == treeparam1: castlingrights = (False, castlingrights[1])
        if i == treeparam2: castlingrights = (castlingrights[0], False)
        if j == treeparam3: bc = (bc[0], False)
        if j == treeparam4: bc = (False, bc[1])
        if p == 'K':
            castlingrights = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                bd = put(bd, treeparam1 if j < i else treeparam2, '.')
                bd = put(bd, kp, 'R')
        if p == 'P':
            if treeparam3 <= j <= treeparam4:
                bd = put(bd, j, 'Q')
            if j - i == 2*N:
                ep = i + N
            if j == self.ep:
                bd = put(bd, j+S, '.')
        return Board(
            Board(bd, score, castlingrights, bc, ep, kp).bd[::-1].swapcase(), -Board(bd, score, castlingrights, bc, ep, kp).score, Board(bd, score, castlingrights, bc, ep, kp).bc, Board(bd, score, castlingrights, bc, ep, kp).castlingrights,
            119-Board(bd, score, castlingrights, bc, ep, kp).ep if Board(bd, score, castlingrights, bc, ep, kp).ep else 0,
            119-Board(bd, score, castlingrights, bc, ep, kp).kp if Board(bd, score, castlingrights, bc, ep, kp).kp else 0)

    def value(self, move):
        i, j = move
        p, q = self.bd[i], self.bd[j]
        score = pst[p][j] - pst[p][i]
        if q.islower():
            score += pst[q.upper()][119-j]
        if abs(j-self.kp) < 2:
            score += pst['K'][119-j]
        if p == 'K' and abs(i-j) == 2:
            score += pst['R'][(i+j)//2]
            score -= pst['R'][treeparam1 if j < i else treeparam2]
        if p == 'P':
            if treeparam3 <= j <= treeparam4:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][119-(j+S)]
        return score


Entry = nmd('Entry', 'lower upper')
class ChessAI:
    def __init__(self, color: str):
        self.color = color # either "w" or "b"
        
        self.hist = [Board((
        '         \n'
        '         \n'
        ' rnbqkbnr\n' 
        ' pppppppp\n' 
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' ........\n'
        ' PPPPPPPP\n'
        ' RNBQKBNR\n' 
        '         \n' 
        '         \n' 
    ), 0, (True,True), (True,True), 0, 0)]
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0
    def make_move(self) -> str:
        a = 'abcdefgh'
        mymove = self.playnext(self.hist)
        if self.color == 'w':
            mymove = [a[7-a.index(mymove[0][0])] + str(abs(9-int(mymove[0][1]))) + a[7-a.index(mymove[0][2])] + str(abs(9-int(mymove[0][3]))),mymove[1],mymove[2]]

        self.hist.append(self.hist[-1].move(mymove[2]))

        return mymove[0]
    def add_move(self, move: str) -> None:
        a = 'abcdefgh'
        if self.color == 'w':
            move = a[7-a.index(move[0])] + str(abs(9-int(move[1]))) + a[7-a.index(move[2])] + str(abs(9-int(move[3])))
        match = re.match('([a-h][1-8])'*2, move)
        fil, rank = ord(match.group(1)[0]) - ord('a'), int(match.group(1)[1]) - 1
        m1 = treeparam1 + fil - 10*rank
        fil, rank = ord(match.group(2)[0]) - ord('a'), int(match.group(2)[1]) - 1
        m2 = treeparam1 + fil - 10*rank
        m = m1,m2
        
        self.hist.append(self.hist[-1].move(m))

    def playnext(self, bd):
        
        start = time.time()
        for _depth, move, score in self.search(bd[-1], bd):
            if time.time() - start > 1:
                break
        
        rank, fil = divmod((119-move[0]) - treeparam1, 10)
        rank2, fil2 = divmod((119-move[1]) - treeparam1, 10)
        m1 = chr(fil + ord('a')) + str(-rank + 1)
        m2 = chr(fil2 + ord('a')) + str(-rank2 + 1)
        
        return m1+m2,score,move
    def search(self, position, history=()):
        self.nodes = 0
        if True:
            self.history = set(history)
            
            self.tp_score.clear()

        for depth in range(7, 1000):
            lower, upper = -upperbound, upperbound
            while lower < upper - 13:
                gamma = (lower+upper+1)//2
                score = self.bound(position, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            self.bound(position, lower, depth)
            
            yield depth, self.tp_move.get(position), self.tp_score.get((position, depth, True)).lower
            
    def bound(self, position, gamma, depth, root=True):
        self.nodes += 1

        depth = max(depth, 0)

        if position.score <= -lowerbound:
            return -upperbound

        if True:
            if not root and position in self.history:
                return 0

        entry = self.tp_score.get((position, depth, root), Entry(-upperbound, upperbound))
        if entry.lower >= gamma and (not root or self.tp_move.get(position) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper

        def moves():
            if depth > 0 and not root and any(c in position.bd for c in 'RBNQ'):
                yield None, -self.bound(Board(
            position.bd[::-1].swapcase(), -position.score,
            position.bc, position.castlingrights, 0, 0), 1-gamma, depth-3, root=False)
            if depth == 0:
                yield None, position.score
            killer = self.tp_move.get(position)
            if killer and (depth > 0 or position.value(killer) >= 219):
                yield killer, -self.bound(position.move(killer), 1-gamma, depth-1, root=False)
            for move in sorted(position.generator(), key=position.value, reverse=True):
                if depth > 0 or position.value(move) >= 219:
                    yield move, -self.bound(position.move(move), 1-gamma, depth-1, root=False)

        best = -upperbound
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                if len(self.tp_move) > maxttsize: self.tp_move.clear()
                self.tp_move[position] = move
                break
        if best < gamma and best < 0 and depth > 0:
            is_dead = lambda position: any(position.value(m) >= lowerbound for m in position.generator())
            if all(is_dead(position.move(m)) for m in position.generator()):
                in_check = is_dead(Board(
            position.bd[::-1].swapcase(), -position.score,
            position.bc, position.castlingrights, 0, 0))
                best = -upperbound if in_check else 0

        if len(self.tp_score) > maxttsize: self.tp_score.clear()
        if best >= gamma:
            self.tp_score[position, depth, root] = Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[position, depth, root] = Entry(entry.lower, best)

        return best
    

    


    
 