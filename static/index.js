const board = Chessboard('board', "start")
const socket = io()

socket.on("move", ({ colour, move }) => {
    board.move(move)
})