let socket;

function setup() {
    createCanvas(600,400);
    background(51);
    socket = io.connect('http://localhost:3000');
}

function mouseDragged () {
    let position = {
        x: mouseX,
        y: mouseY
    }
    noStroke();
    fill(255);
    ellipse(position.x, position.y, 10, 10);
    socket.emit('position', position)
}

function draw() {
}