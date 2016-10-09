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

def test(one, two) :
    return 4

executor = Executor('{}:{}'.format(SCHEDULER_IP, SCHEDULER_PORT))

taskclient.add_user(HOME_PAGE)
for _ in range(1):
    taskclient.add_job(HOME_PAGE)

result_list = []
for test in range(5):
    #result = executor.map(taskclient.worker, [HOME_PAGE, HOME_PAGE], [0, 1])
    result = executor.submit(taskclient.worker, HOME_PAGE, test)
    #executor.submit(result)
    result_list.append(result)

distributed.diagnostics.progress(result_list)
sim_results = executor.gather(result_list)
print('---------')
print(sim_results[0] is sim_results[1])
print('---------')
print([x['node_id'] for x in sim_results])

