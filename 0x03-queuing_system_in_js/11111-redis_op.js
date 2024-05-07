import { redisClientFactory } from 'kue';
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

function setNewSchool(SchoolName, value) {
  if (typeof value === 'object') {
    value = JSON.stringify(value);
  }
  client.set(SchoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  val = client.get(schoolName);
  console.log(value);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
