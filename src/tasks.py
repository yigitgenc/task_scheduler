import os
import time
import random
import logging
import threading

from PIL import Image

from db import connect

THUMBNAIL_SIZES = [
    dict(folder_name='tns', size=(200, 200)),
    dict(folder_name='tnm', size=(600, 600)),
    dict(folder_name='tnl', size=(2000, 2000))
]

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-10s) %(message)s'
)


def task_a(semaphore, lock, active_threads, row):
    """
    Opens queued image, create thumbnails and
    save in a folder with the format {photo.id}.jpg

    :param semaphore: instance of threading.BoundedSemaphore
    :param lock: instance of threading.Lock
    :param active_threads: list
    :param row: row object of the SQL query result

    :return:
    """

    logging.debug('Waiting to join the pool.')

    with semaphore:
        logging.debug('Joined the pool. Starting...')

        thread_name = threading.current_thread().getName()

        with lock:
            active_threads.append(thread_name)

        data_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
        )

        file_path = os.path.join(data_directory, 'original', row['filename'])
        file_name, ext = os.path.splitext(os.path.basename(str(file_path)))
        thumbnail_name = '{}.{}.jpg'.format(file_name, row['id'])

        logging.debug('Creating thumbnails for {}'.format(file_path))

        for thumbnail in THUMBNAIL_SIZES:
            thumbnail_path = os.path.join(data_directory, thumbnail['folder_name'], thumbnail_name)

            image = Image.open(file_path)
            image.thumbnail(thumbnail['size'], Image.ANTIALIAS)
            image.save(thumbnail_path, 'JPEG')

            logging.debug('Thumbnail created: {} {}'.format(thumbnail_path, thumbnail['size']))

        # Mimics something that takes time.
        time.sleep(random.randint(3, 10))

        with lock:
            conn, cursor = connect()
            cursor.execute('UPDATE pending_photos SET status=1 WHERE id={}'.format(row['id']))
            conn.commit()
            conn.close()

            active_threads.remove(thread_name)

        logging.debug('Exiting.')

    return


def task_b(lock):
    """
    Executes external binary.

    :param lock: instance of threading.Lock
    :return:
    """

    logging.debug('Starting...')

    with lock:
        conn, cursor = connect()

        pending_photos = cursor.execute(
            'SELECT id, filename FROM pending_photos WHERE status=1 ORDER BY id ASC;'
        ).fetchall()

        if pending_photos:
            for row in pending_photos:
                logging.debug('Processing {}'.format(row['filename']))

                # Mimics something that takes time.
                time.sleep(random.randint(3, 10))

                cursor.execute('UPDATE pending_photos SET status=2 WHERE id={}'.format(row['id']))
                conn.commit()
        else:
            logging.info('No pending photos with status=1 statement.')

        conn.close()

    logging.debug('Exiting.')

    return


def listener(lock, active_threads):
    """
    Checks the active threads of task_a and
    runs task_b if it's lower than 2.

    :param lock: instance of threading.Lock
    :param active_threads: list
    :return:
    """

    logging.debug('Listening active threads...')

    while True:
        with lock:
            if len(active_threads) < 2:
                threading.Thread(target=task_b, name='task_b', args=(lock, )).start()

        if len(active_threads) == 0:
            break

        time.sleep(0.5)

    logging.debug('Exiting.')
