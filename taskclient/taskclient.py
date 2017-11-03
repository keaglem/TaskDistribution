from multiprocessing import Process, Pool, cpu_count
import click
import requests
import json
import subprocess
import datetime
import time
import platform
import os

EXECUTABLE_NAME = 'echo'

@click.command()
@click.option('--num_nodes', default=2, help='Number of processing nodes to work on')
@click.option('--home_page', default='http://localhost:5000', help='Web-site for retrieving tasks')
def main_loop(num_nodes, home_page):
    """
    Keep num_nodes busy with work from the server
    :param num_nodes: Number of processors to run on
    :param home_page: Home-page to contact for work
    :return: n/a
    """
    add_user(home_page)
    for _ in range(10):
        add_job(home_page)

    if num_nodes > cpu_count():
        print('Asked for too many nodes: Requested {} nodes and had {}.'.format(num_nodes, cpu_count()))
        return
    processes = []
    for node_num in range(num_nodes):
        processes.append(Process(target=worker_main, args=(home_page, node_num)))
        processes[node_num].daemon = True
        processes[node_num].start()
    for node_num in range(num_nodes):
        processes[node_num].join()


def worker_main(home_page, node_num):
    """
    Main loop to run forever for a worker
    :param home_page: website to contact for jobs
    :param node_num: node number assigned to the process
    :return: nothing
    """
    while True:
        worker(home_page=home_page, node_num=node_num)
        time.sleep(3)

def worker(home_page, node_num):
    """
    Worker job for retrieving tasks from the web-server (runs forever)
    :param home_page: website base location
    :param node_num: node number for print purposes
    :return: sim dictionary
    """

    print('Home page: {}, node_num: {}'.format(home_page, node_num))

    sim = dict([])

    try:
        url_get = home_page + '/api/get_job'
        print('URL to get: {}'.format(url_get))
        node_string = '{}_{}'.format(platform.node(), node_num)
        resp = requests.get(url_get, params={'id': node_string})

        if resp.status_code is not 200:
            print('Invalid request, code: {}, reason: {}'.format(resp.status_code, resp.reason))

        data = json.loads(resp.text)
        if not data['job']:
            print('No jobs to perform ... Sleeping on node: {}'.format(node_num))
            return []

        # Setup output parameters
        url_put = home_page + '/api/finish_job'
        sim = data['job']

        print('Running job {}'.format(sim['simulation_id']))
        sim['start_time'] = datetime.datetime.now().timetuple()

        # Setup environment for the processes to run
        env = {}
        env.update(os.environ)

        # Call the desired process
        command_line = ' '.join([EXECUTABLE_NAME,
                        sim['input_settings_filename'],
                        sim['output_directory'],
                        str(sim['random_seeding']),
                        sim['submission']['simulation_name']])
        print(command_line)
        #subprocess.call(command_line,
        #                shell=True,
        #                env=env)

        # Setup output parameters
        sim['end_time'] = datetime.datetime.now().timetuple()
        sim['is_complete'] = True
        sim['has_error'] = False
        # Put output status
        requests.put(url_put, json={'result': sim})
    except (ConnectionError, ConnectionRefusedError):
        print('Failed to connect to {} on node_num {}, sleeping.'.format(url_get, node_num))
    except Exception as the_exception:
        print('Failed to connect to {} on node_num {}, reporting error {}'.format(url_get, node_num, the_exception))

        # Setup failure parameters
        sim['end_time'] = datetime.datetime.now().timetuple()
        sim['is_complete'] = False
        sim['has_error'] = True

        # Put failure information to the server
        requests.put(url_put, json={'result': sim})

    return sim

def add_job(home_page):
    url_get = home_page + '/api/add_job'
    resp = requests.get(url_get)


def add_user(home_page):
    url_get = home_page + '/api/add_user'
    resp = requests.get(url_get)

if __name__ == '__main__':

    main_loop()




