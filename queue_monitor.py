from multiprocessing import Queue
from utils import sys_msg


def monitor_queue(queue: Queue):
    """
    A function that runs in a separate thread to look
    for changes in the queue. This runs in parallel with
    the kernel to monitor the changes in the system data
    queue.

    When the queue is changed, it is the task of this
    function which runs as a daemon thread to upload the
    results back to the server.
    """


    while True:
        while not queue.empty():
            sys_msg("queue_monitor", "Received data \"%s\" in queue." % queue.get())