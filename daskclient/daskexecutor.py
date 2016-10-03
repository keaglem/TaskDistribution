from distributed import Executor, Scheduler, Nanny, Worker
from tornado.ioloop import IOLoop
from threading import Thread
import taskclient
import time

SCHEDULER_PORT = 5678
SCHEDULER_IP = '127.0.0.1'

HOME_PAGE = 'http://localhost:5050'

def test(one, two) :
    return 4

print('Hello')
loop_worker = IOLoop.current()
t2 = Thread(target=loop_worker.start)
t2.start()

nanny_process = Worker(scheduler_ip=SCHEDULER_IP,
                      scheduler_port=SCHEDULER_PORT,
                      loop=loop_worker )
#loop_worker.start()
nanny_process.start()
print('Im here')

executor = Executor('{}:{}'.format(SCHEDULER_IP, SCHEDULER_PORT))
#
result = executor.submit(taskclient.worker, HOME_PAGE, 0)
print(executor.gather(result))
