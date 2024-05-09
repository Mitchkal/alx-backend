import redis from 'redis';
import kue from 'kue';
import express from 'express';

const port = 1245;

import { promisify } from 'util';

const client = redis.createClient();
const queue = kue.createQueue();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const reserveSeat = (number) => {
  client.set('available_seats', number, redis.print);
};

const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);
  return await getAsync('available_seats');
};

const initializeSeats = async () => {
  await reserveSeat(50);
};

let reservationEnabled = true;
initializeSeats();

const app = express();

app.get('/available_seats', async (_req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberofAvailableSeats: numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }
  //   const { reserve_seat } = req.params;

  const job = queue.create('reserve_seat', {}).save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(availableSeats - 1);
      if (availableSeats === 1) {
        reservationEnabled = false;
      }
      console.log(`Seat reservation job ${job.id} completed`);
      done();
    }
  });
});
app.listen(port, (err) => {
  if (!err) {
    console.log('app is running on localhost port 1245');
  } else {
    console.log(`App is not running due to error ${err}`);
  }
});
