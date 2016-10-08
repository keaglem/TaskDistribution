from distributed import  Scheduler
from distributed.http import HTTPScheduler
from tornado.ioloop import IOLoop
from threading import Thread
import taskclient
import time

SCHEDULER_PORT = 5678
SCHEDULER_HTTP_PORT = 9786
SCHEDULER_BOKEH_PORT = 12345
SCHEDULER_IP = '127.0.0.1'

HOME_PAGE = 'http://localhost:5050'

# Initialize the IOLoop for the scheduler
loop = IOLoop.current()
t2 = Thread(target=loop.start, daemon=True)
# Initialize the Scheduler
http_port = SCHEDULER_HTTP_PORT
the_scheduler = Scheduler(ip=SCHEDULER_IP,
                          loop=loop,
                          services={('http', http_port): HTTPScheduler})


the_scheduler.start(port=SCHEDULER_PORT)
t2.start()
t2.join()

print('Started the scheduler')



