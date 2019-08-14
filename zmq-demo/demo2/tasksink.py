import sys
import time
import zmq

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.bind('tcp://*:5558')

tstart = time.time()

for task_nbr in range(100):
    s = receiver.recv()
    if task_nbr % 10 == 0:
        sys.stdout.write(':')
    else:
        sys.stdout.write('.')
    sys.stdout.flush()

tend = time.time()
print('Total elapsed time: %d msec' % ((tend - tstart) * 1000))
