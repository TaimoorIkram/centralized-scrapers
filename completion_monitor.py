from datetime import datetime, timedelta
from multiprocessing import Queue
from sqlite3 import Connection
from utils import sys_msg

def monitor_completion(completion_queue: Queue, db_conn: Connection):
    """
    A kernel initiated daemon process that monitors a separate queue 
    where completion signals are sent. The signals contain the name 
    of the scraper that terminated, deadlines are updated appropriately.
    """

    while True:
        while not completion_queue.empty():
            scraper_name = completion_queue.get()
            sys_msg("completion_daemon", "The '%s' scraper completed. Deadline updated." % scraper_name)

            # updation of scraper deadline
            db_conn.execute("UPDATE TABLE scraper_deadlines SET deadline = ? WHERE scraper_name = ?", (datetime.now() + timedelta(days=5), scraper_name))
            db_conn.commit()
            sys_msg("kernel", "Updated deadlines for the completed scraper threads.")
