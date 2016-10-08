from distributed import Executor, Scheduler, Nanny, Worker
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



print('Hello')
loop_worker = IOLoop.current()
t = Thread(target=loop_worker.start)
t.start()
loop_worker2 = IOLoop.current()
t2 = Thread(target=loop_worker2.start)
t2.start()
nanny_process = Worker(center_ip=SCHEDULER_IP,
                       center_port=SCHEDULER_PORT,
                       loop=loop_worker,
                       ncores=1)
nanny_process.start()

nanny_process2 = Worker(center_ip=SCHEDULER_IP,
                       center_port=SCHEDULER_PORT,
                       loop=loop_worker2,
                       ncores=1)
nanny_process2.start()
print('Im here')


executor = Executor('{}:{}'.format(SCHEDULER_IP, SCHEDULER_PORT))
#

taskclient.add_user(HOME_PAGE)
for _ in range(10):
    taskclient.add_job(HOME_PAGE)

for _ in range(5):
    result = executor.map(taskclient.worker, [HOME_PAGE, HOME_PAGE], [0, 1])
    sim_results = executor.gather(result)
    print([x['node_id'] for x in sim_results])
    time.sleep(2)

nanny_process.stop()
nanny_process2.stop()
loop_worker.stop()
loop_worker2.stop()
t.join()
t2.join()
