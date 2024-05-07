const redis = require('redis');
import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
  client.subscribe('holberton school channel', (err) => {
    if (err) {
      console.error('Error subscribing to channel', err);
    }
  });
});
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.on('message', (_channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    client.unsubscribe('holberton school channel');
    client.quit();
    console.log('Server killed');
  }
});
