const express = require('express');
const path = require('path');
const app = express();

const start = (new Date()).getTime();

app.get('/', (req, res) => {
  const diff = (new Date()).getTime() - start;

  const number = (1.8 * Math.abs(Math.sin(diff / 5000))) + 0.2;
  res.status(200).send(`${number}`);
  console.log(`Returning value ${number}`);
});

app.get('/graph', function(req, res) {
  res.sendFile(path.join(__dirname, '/index.html'));
});

app.listen(4000);

console.log('Running data server at http://localhost:4000/');
