const Client = require('node-osc').Client;
const Bundle = require('node-osc').Bundle;

let address='/objects/texturedMesh.001/modifiers/Wireframe/thickness'
const bundle = new Bundle([address, .001], [address, .02], [address, .03]);
const client = new Client('127.0.0.1', 9003);
client.send(bundle);
console.log("again")
client.close();
