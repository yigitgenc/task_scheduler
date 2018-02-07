import time
import logging
import threading

from db import connect
from settings import MAX_CONNECTIONS, RESTART_DELAY
from tasks import task_a, task_b

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-10s) %(message)s'
)


def service_a(event, lock, active_threads):
    """
    Checks the pending photos with status=0 statement periodically.

    :param event: instance of threading.Event
    :param lock: instance of threading.Lock
    :param active_threads: list
    :return:
    """

    semaphore = threading.BoundedSemaphore(MAX_CONNECTIONS)

    # Keep the service alive until the event is set.
    while not event.is_set():
        with lock:
            # Skip it if there are any active threads.
            if active_threads:
                continue

            conn, cursor = connect()
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
            logging.info('No pending photos found with status=0 statement. '
                         'Restarting service_a in {} seconds.'.format(RESTART_DELAY))

            time.sleep(int(RESTART_DELAY))

        time.sleep(0.5)

    return


def service_b(event, lock, active_threads):
    """
    Checks the pending photos with status=0 statement periodically
    and the active threads of task_a.

    :param event: instance of threading.Event
    :param lock: instance of threading.Lock
    :param active_threads: list
    :return:
    """

    # Keep the service alive until the event is set.
    while not event.is_set():
        with lock:
            # Skip it if there are more than two active threads.
            if len(active_threads) > 2:
                continue

            conn, cursor = connect()
            row = cursor.execute(
                'SELECT id, filename FROM pending_photos WHERE status=1 ORDER BY id ASC LIMIT 1;'
            ).fetchone()
            conn.close()

        if row:
            logging.info("Active threads are lower than 2. Service is ready to run task_b.")

            task = threading.Thread(target=task_b, name='task_b-{}'.format(row['id']), args=(lock, row))
            task.start()
            task.join()
        else:
            logging.info('No pending photos found with status=1 statement. '
                         'Restarting service_b in {} seconds.'.format(RESTART_DELAY))

            time.sleep(int(RESTART_DELAY))

        time.sleep(0.5)

    return
