from distributed import Executor, Scheduler, Nanny, Worker
import distributed
from tornado.ioloop import IOLoop
from threading import Thread
import taskclient
import time
import itertools


SCHEDULER_PORT = 5678
SCHEDULER_HTTP_PORT = 9786
SCHEDULER_BOKEH_PORT = 12345
SCHEDULER_IP = '127.0.0.1'

HOME_PAGE = 'http://localhost:5050'

def test(one, two) :
    return 4

executor = Executor('{}:{}'.format(SCHEDULER_IP, SCHEDULER_PORT))

taskclient.add_user(HOME_PAGE)
for _ in range(5):
    taskclient.add_job(HOME_PAGE)

result_list = []
num_iters = 50
    #result = executor.map(taskclient.worker, [HOME_PAGE, HOME_PAGE], [0, 1])
result = executor.map(taskclient.worker,
                      itertools.repeat(HOME_PAGE,num_iters),
                      range(num_iters))
result_list = result

distributed.diagnostics.progress(result_list)
print()
print(executor.who_has(result_list))
sim_results = executor.gather(result_list)
print('---------')


