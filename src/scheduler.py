import logging
import threading

from db import connect
from tasks import task_a, listener

MAX_CONNECTION = 3

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-10s) %(message)s'
)


def scheduler():
    """
    Concurrent thread management prototype.

    :return:
    """
    
    semaphore = threading.BoundedSemaphore(MAX_CONNECTION)
    lock = threading.Lock()
    conn, cursor = connect()
    active_threads = list()

    pending_photos = cursor.execute(
        'SELECT id, filename FROM pending_photos WHERE status=0 ORDER BY id ASC;'
    ).fetchall()

    conn.close()

    if pending_photos:
        for row in pending_photos:
            threading.Thread(target=task_a, name='task_a-{}'.format(row['id']), args=(
                semaphore, lock, active_threads, row
            )).start()
    else:
        logging.info('No pending photos with status=0 statement.')

    threading.Thread(target=listener, name='listener', args=(lock, active_threads)).start()

    return


if __name__ == '__main__':
    scheduler()
