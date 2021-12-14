const express = require('express');
let app = express();
let server = app.listen(3000);
const socket = require('socket.io')
var cors = require('cors')

//osc config
const Client = require('node-osc').Client;
const Bundle = require('node-osc').Bundle;

let address='/objects/texturedMesh.001/modifiers/Wireframe/thickness'
function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}
const client = new Client('127.0.0.1', 9003);
//end of osc config


let io = socket(server);
app.use(express.static('public'));
app.use(cors())
console.log('Socket server is running');

io.sockets.on('connection', newConnection);

function newConnection(socket) {
    console.log("New connection: " + socket.id);
    socket.on('position', play);
}

function play(data) {
    const bundle = new Bundle([address, data]);
    client.send(bundle);
    console.log("sent info", bundle)
}
