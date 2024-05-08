import kue from 'kue';
import createPushNotificationsJobs from './8-job';
import { expect } from 'chai';
import sinon from 'sinon';

describe('createPushNotificationsJobs', () => {
  let queue;
  let consoleSpy;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
    consoleSpy = sinon.spy(console, 'log');
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
    consoleSpy.restore();
  });

  it('should throw error if jobs is not an array', () => {
    expect(() => {
      createPushNotificationsJobs('invalid', queue);
    }).throw('Jobs is not an array');
  });

  it('should create jobs in the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'Message 1' },
      { phoneNumber: '4153518781', message: 'Message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).equal(2);
  });

  it('should log job creation', () => {
    const jobs = [
      { phoneNumber: '4153518789', message: 'Message 1' },
      { phoneNumber: '4153518781', message: 'Message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(consoleSpy.callCount).equal(2);
    expect(consoleSpy.calledWithMatch(/Notification job created:/)).equal(true);
  });
});
