const kue = require('kue');

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '+1234567890',
  message: 'Hello, this is a notification message!',
};

const job = queue.create('push notification code', jobData);

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.log('Notification job failed');
});

job.save((err) => {
  if (!err) {
    console.log(`Notification job created: ${job.id}`);
  }
});

queue.on('error', (err) => {
  console.log('Kue error:', err);
});
