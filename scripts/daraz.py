from multiprocessing import Queue
from utils import sys_msg
from kernel import Semaphore
from time import sleep

def run(semaphore: Semaphore, results_queue: Queue, delay=5):
    sleep(delay)
    semaphore.lock()
    results_queue.put('NIGGA')
    semaphore.unlock()