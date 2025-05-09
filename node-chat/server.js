const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('chat message', (msg) => {
        io.emit('chat message', msg); //Broadcast to everyone)
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

const PORT = 3001;
server.listen(PORT, () => {
    console.log(`Chat server running at http://localhost:${PORT}`);
});