import { createClient } from 'redis';

async function connectToRedis() {
  return new Promise((resolve, reject) => {
    const client = createClient();

    client.on('error', (err) => {
      console.log(`Redis client not connected to the server: ${err}`);
      reject(err);
    });
    client.on('connect', () => {
      console.log('Redis client connected to the server');
      resolve(client);
    });
  });
}

connectToRedis();
