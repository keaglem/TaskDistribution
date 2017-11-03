from distributed import Executor, Scheduler, Nanny, Worker
import distributed
from tornado.ioloop import IOLoop
from threading import Thread
import taskclient
import time

SCHEDULER_PORT = 5678
SCHEDULER_HTTP_PORT = 9786
SCHEDULER_BOKEH_PORT = 12345
SCHEDULER_IP = '127.0.0.1'

HOME_PAGE = 'http://localhost:5050'

print('Hello')
loop_worker = IOLoop()
t = Thread(target=loop_worker.start)
t.start()

NUM_WORKERS = 2

nanny_process = [Worker(center_ip=SCHEDULER_IP,
                        center_port=SCHEDULER_PORT,
                        loop=loop_worker,
                        ncores=2) for _ in range(NUM_WORKERS)]

for nanny in nanny_process:
    nanny.start()

t.join()

for nanny in nanny_process:
    nanny.start()

loop_worker.stop()
