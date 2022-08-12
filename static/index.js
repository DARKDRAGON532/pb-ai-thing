const board = Chessboard('board', "start")
const socket = io()

socket.on("move", ({ colour, move }) => {
    if (colour == "connect") {
        // do stuff
    }
    board.position(move)
})

socket.on("new", () => {
    board.start()
})

socket.on("status", ({ turn, status }) => {
    turn = turn == "w" ? "White" : "Black"
    document.getElementById("info").innerText = `${turn}'s turn\n${status}`
})

socket.on("teams", ({ team1, team2, round }) => {
    document.getElementById("team-info").innerText = `${team1} vs ${team2}\nRound ${round}`
})

socket.on("reload", () => {
    document.location.reload()
})