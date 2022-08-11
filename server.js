const Express = require('express');
const { stringify } = require('querystring');
const app = Express();
const server = require('http').createServer(app);
const { Server } = require('socket.io')
const io = new Server(server)
const port = 8080;

app.use(Express.json())
app.use(Express.static(__dirname + '/static'));

app.post("/move", (req, res) => {
    let { colour, move } = req.body;
    if (move.length != 4) {
        return res.status(402).end()
    }
    res.status(200).end()
    if (!move.includes("-")) {
        move = move.substring(0, 2) + "-" + move.substring(2, 4)
    }
    io.emit("move", { colour, move })
})

io.on('connection', socket => {
    console.log("connected")
    socket.on('disconnect', function () {
        console.log('disconnected');
    });
})

server.listen(port, () => {
    console.log(`Listening on *:${port}`);
})