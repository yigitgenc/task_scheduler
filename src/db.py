import os
import sqlite3


def connect():
    """
    Connects to SQLite, creates table(s) if not exists.
    Returns connection and cursor as a tuple.

    :return: tuple
    """

    conn = sqlite3.connect(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'task_scheduler.db'
    ))
    conn.row_factory = sqlite3.Row

    return conn, conn.cursor()
