from distributed import  Scheduler
from tornado.ioloop import IOLoop
from threading import Thread
import taskclient
import time

SCHEDULER_PORT = 5678
SCHEDULER_IP = '127.0.0.1'

HOME_PAGE = 'http://localhost:5050'

# Initialize the IOLoop for the scheduler
loop = IOLoop.current()
t2 = Thread(target=loop.start, daemon=True)
t2.start()
# Initialize the Scheduler
the_scheduler = Scheduler(ip=SCHEDULER_IP,
                          loop=loop)
the_scheduler.start(port=SCHEDULER_PORT)

t2.join()

print ('Started the scheduler')




