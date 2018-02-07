import logging
import threading

from services import service_a, service_b

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-10s) %(message)s'
)


def main():
    """
    Concurrent thread management prototype.

    :return:
    """

    event = threading.Event()
    lock = threading.Lock()
    active_threads = list()

    service1 = threading.Thread(target=service_a, name='service_a', args=(event, lock, active_threads))
    service1.start()

    service2 = threading.Thread(target=service_b, name='service_b', args=(event, lock, active_threads))
    service2.start()

    return


if __name__ == '__main__':
    main()
