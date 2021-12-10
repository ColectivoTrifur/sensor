const express = require('express');
const socket = require('socket.io');
const midi = require('midi');
// Set up a new output.
const output = new midi.Output();

let app = express();
let server = app.listen(3000);
let io = socket(server);

app.use(express.static('public'));
console.log('Socket server is running');

io.sockets.on('connection', newConnection);

function newConnection(socket) {
    console.log("New connection: " + socket.id);
    output.openVirtualPort('p5-test');
    socket.on('position', positionMsg);
}

function positionMsg(data) {
    console.log(data);
    output.sendMessage([144,69,127]);
}