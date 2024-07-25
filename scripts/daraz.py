from multiprocessing import Queue
from utils import sys_msg
from kernel import Semaphore
from time import sleep

MKT_NAME = 'daraz'

def run(semaphore: Semaphore, results_queue: Queue, completion_queue: Queue, delay=20):
    sleep(delay)
    semaphore.lock()
    results_queue.put('NIGGA')
    completion_queue.put(MKT_NAME)
    semaphore.unlock()