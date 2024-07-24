from datetime import datetime
from multiprocessing import Process, Pipe, Queue
import random
from threading import Event, Thread
import time

from boot import start_kernel
from utils import sys_msg
from scripts import daraz
from queue_monitor import monitor_queue

class ScraperThread():
    def __init__(self, thread_name, thread_process) -> None:
        self.thread_name = thread_name
        self.is_joined = False
        self.thread_process = thread_process

    def join(self):
        self.thread_process.join()
        self.is_joined = True

class Semaphore():
    def __init__(self) -> None:
        self.isLocked = False
    
    def lock(self):
        while (self.isLocked): continue

        self.isLocked = True
        print('semaphore: acquired by %s' % __name__)
        return False

    def unlock(self):
        if self.isLocked: 
            self.isLocked = False
            return True
        else: return False

def worker(conn):
    event.wait(0.25)
    semaphore.lock()
    print('[%s] This is the first thread sending data to the other guy.' % __name__)
    conn.send([42, None, string])
    conn.close()
    semaphore.unlock()

try:
    t_start = time.time()
    if __name__ == '__main__':
        # globals
        event = Event()
        semaphore = Semaphore()
        string = 'lol'

        # boot the kernel
        db_conn = start_kernel()

        # load scraper deadlines
        deadlines = db_conn.execute("SELECT * FROM scraper_deadlines").fetchall()
        scraper_deadlines = {}
        processes = {}

        for deadline in deadlines:
            scraper_deadlines[deadline[0]] = datetime.fromisoformat(deadline[1])

            # scraper thread pool to be joined
            processes[deadline[0]] = None

        while True:
            # refresh current day. could be optimized i think.
            today = datetime.now()
            

            # compare to find the faulty day.
            for key in scraper_deadlines.keys():
                # data items from each scraper to be pushed to the API
                data_queue = Queue(maxsize=4)


                # start the queue monitor thread
                data_queue_monitor = Thread(target=monitor_queue, args=(data_queue, ), daemon=True)
                data_queue_monitor.start()

                if today > scraper_deadlines[key]: 
                    sys_msg("kernel", "System detected '%s' scraper to have reached its deadline." % key)

                    # scraper thread that runs if the previous one has terminated or is not running.
                    if processes[key] and processes[key].thread_process.is_alive():
                        sys_msg("kernel", "The process '%s' scraper is still running." % key)
                    else:
                        parent_conn, child_conn = Pipe()
                        p = Process(target=daraz.run, args=(semaphore, data_queue, random.randint(1, 5)))
                        p.start()

                        thread_process = ScraperThread(key, p)
                        processes[key] = thread_process

                else:
                    print('GOOD TO GO')
                    pass

                # optional wait of one day to check expiration again?
                
            for process in processes.keys():
                if processes[process] and processes[process].is_joined == False:
                    processes[process].join()

except KeyboardInterrupt as kInt:
    print('\r[%s] Closing the kernel...' % __name__)
finally:
    print('[%s] The kernel exited successfully with a total runtime of %.2f seconds.' % (__name__, time.time() - t_start))