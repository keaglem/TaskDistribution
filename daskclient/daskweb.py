import multiprocessing
import subprocess
import socket
import os
import sys
import json
import logging

SCHEDULER_PORT = 5678
SCHEDULER_HTTP_PORT = 9786
SCHEDULER_BOKEH_PORT = 12345
SCHEDULER_IP = '127.0.0.1'

logger = logging.getLogger('distributed.scheduler')

if __name__ == '__main__':


    import bokeh
    import distributed.bokeh
    bokeh_port = SCHEDULER_BOKEH_PORT
    show = True
    ip = SCHEDULER_IP
    host = SCHEDULER_IP
    given_host = host
    http_port = SCHEDULER_HTTP_PORT
    port = SCHEDULER_PORT
    bokeh_whitelist = []

    hosts = ['%s:%d' % (h, bokeh_port) for h in
             ['localhost', '127.0.0.1', ip, socket.gethostname(),
              host] + list(bokeh_whitelist)]
    dirname = os.path.dirname(distributed.__file__)
    paths = [os.path.join(dirname, 'bokeh', name)
             for name in ['status', 'tasks']]
    binname = 'bokeh.bat' if 'win' in sys.platform else 'bokeh'
    binname = os.path.join(os.path.dirname(sys.argv[0]), binname)
    args = ([binname, 'serve'] + paths +
            ['--log-level', 'warning',
             '--check-unused-sessions=50',
             '--unused-session-lifetime=1',
             '--port', str(bokeh_port)] +
            sum([['--host', host] for host in hosts], []))
    if show:
        args.append('--show')

    bokeh_options = {'host': host if given_host else '127.0.0.1',
                     'http-port': http_port,
                     'tcp-port': port,
                     'bokeh-port': bokeh_port}
    with open('.dask-web-ui.json', 'w') as f:
        json.dump(bokeh_options, f, indent=2)

    if sys.version_info[0] >= 3:
        from bokeh.command.bootstrap import main

        ctx = multiprocessing.get_context('spawn')
        bokeh_proc = ctx.Process(target=main, args=(args,))
        bokeh_proc.daemon = True
        bokeh_proc.start()
    else:
        bokeh_proc = subprocess.Popen(args)

    logger.info(" Bokeh UI at:  http://%s:%d/status/"
                % (ip, bokeh_port))

    bokeh_proc.join()