import os

# Maximum concurrent threads to be run.
MAX_CONNECTIONS = os.environ.get('SCHEDULER_MAX_CONNECTIONS', 3)

# Maximum threads to be open.
MAX_THREADS = os.environ.get('SCHEDULER_MAX_THREADS', 10)


# Thumbnail sizes.
THUMBNAIL_SIZES = [
    # Small
    {'folder_name': 'tns', 'size': (
        os.environ.get('SCHEDULER_THUMB_S_W', 200),  # Width
        os.environ.get('SCHEDULER_THUMB_S_H', 200),  # Height
    )},
    # Medium
    {'folder_name': 'tnm', 'size': (
        os.environ.get('SCHEDULER_THUMB_M_W', 600),  # Width
        os.environ.get('SCHEDULER_THUMB_M_H', 600),  # Height
    )},
    # Large
    {'folder_name': 'tnl', 'size': (
        os.environ.get('SCHEDULER_THUMB_L_W', 2000),  # Width
        os.environ.get('SCHEDULER_THUMB_L_H', 2000),  # Height
    )},
]
