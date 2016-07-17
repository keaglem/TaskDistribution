from multiprocessing import Process, Pool, cpu_count
import click
import requests
import json
import subprocess
import datetime
import time


@click.command()
@click.option('--num_nodes', default=1, help='Number of processing nodes to work on')
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
        processes.append(Process(target=worker, args=(home_page, node_num)))
        processes[node_num].daemon = True
        processes[node_num].start()
    for node_num in range(num_nodes):
        processes[node_num].join()


def worker(home_page, node_num):
    """
    Worker job for retrieving tasks from the web-server (runs forever)
    :param home_page: website base location
    :param node_num: node number for print purposes
    :return:
    """
    while True:
        try:
            url_get = home_page + '/api/get_job'
            resp = requests.get(url_get)
            data = json.loads(resp.text)

            if not data['job']:
                print('No jobs to perform ... Sleeping on node: {}'.format(node_num))
                time.sleep(2)
                continue

            url_put = home_page + '/api/finish_job'
            sim = data['job']
            print('Running job {}'.format(sim['simulation_id']))
            sim['start_time'] = datetime.datetime.now().timetuple()
            output=subprocess.check_output([sim['submission']['high_level_script_name'],
                             sim['submission']['simulation_name'],
                             str(sim['random_seeding']),
                             ' > ' + sim['output_filename']], shell=False)
            sim['end_time'] = datetime.datetime.now().timetuple()
            sim['is_complete'] = True
            sim['has_error'] = False
            requests.put(url_put, json={'result': sim})

            time.sleep(2)
        except (ConnectionError, ConnectionRefusedError):
            print('Failed to connect to {} on node_num {}'.format(url_get, node_num))
            time.sleep(500)
        except Exception as the_exception:
            print('Failed to connect to {} on node_num {}'.format(url_get, node_num))
            print(the_exception)
            time.sleep(1000)


def add_job(home_page):
    url_get = home_page + '/api/add_job'
    resp = requests.get(url_get)


def add_user(home_page):
    url_get = home_page + '/api/add_user'
    resp = requests.get(url_get)

if __name__ == '__main__':

    main_loop()




