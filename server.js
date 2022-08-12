import Express from 'express';
import { Chess } from 'chess.js'
const app = Express();
import http from 'http'
const server = http.createServer(app);
import { Server } from 'socket.io';
const io = new Server(server)
const port = 8080;
let game = new Chess()

app.use(Express.json())
app.use(Express.static('./static'));

function updateStatus() {
    io.emit('status', {
        turn: game.turn(),
        status: game.in_checkmate() ? 'Checkmate' : game.in_draw() ? 'Draw' : '',
    })
}

app.post("/move", (req, res) => {
    let { colour, move } = req.body;
    let promotion = "q"
    if (move.length < 3 || move.length > 7 ) {
        return res.status(405).end()
    }
    if ("bnqr".includes(move.charAt(move.length-1))) {
        promotion = move.charAt(move.length-1)
        console.log(promotion)
    }
    if (!move.includes("-")) {
        move = move.substring(0, 2) + "-" + move.substring(2, 4)
    }
    if (game.turn() != colour) {
        return res.status(403).end()
    }
    const [ from, to ] = move.split("-")
    const gameMove = game.move({
        from,
        to,
        promotion
    })
    if (gameMove === null) return res.status(403).json({ error: 1 }).end()
    res.status(200).end()
    io.emit("move", { colour, move: game.fen()})
    updateStatus()
    if (game.game_over()) {
        return res.json({ error: 2 })
    }
})

app.post("/new", (req, res) => {
    io.emit("new")
    game = new Chess()
    res.status(200).end()
})

app.post("/teams", (req, res) => {
    let { team1, team2, round } = req.body
    io.emit("teams", { team1, team2, round })
    res.status(200).end()
})

io.on('connection', socket => {
    console.log("connected")
    io.emit("move", { colour: "connect", move: game.fen()})
    updateStatus()
    socket.on('disconnect', function () {
        console.log('disconnected');
    });
})

server.listen(port, () => {
    console.log(`Listening on *:${port}`);
})