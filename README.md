# task_scheduler

Concurrent thread management prototype.

## Installing

Go to project directory and type the commands below respectively.

```
$ sqlite3 task_scheduler.db
```

Load `seed.sql` by typing `.read seed.sql`
```
SQLite version 3.19.3 2017-06-27 16:48:08
Enter ".help" for usage hints.
$ sqlite> .read seed.sql
$ Ctrl-D
```

Install `virtualenv` into the project and activate it.
```
$ virtualenv .
$ source bin/activate
```

Install requirements.
```
$ pip install -r requirements.txt
```

## Running

To run scheduler, type:
```
$ python src/scheduler.py
```

## Environment Variables

`SCHEDULER_MAX_CONNECTIONS`

Maximum concurrent threads to be run.

> Default: 3

`SCHEDULER_MAX_THREADS`

Maximum threads to be open.

> Default: 10

`SCHEDULER_RESTART_DELAY`

Restart wait time in seconds.

> Default: 30

`SCHEDULER_THUMB_S_W`

Small thumbnail width size.

> Default: 200

`SCHEDULER_THUMB_S_H`

Small thumbnail height size.

> Default: 200

`SCHEDULER_THUMB_M_W`

Medium thumbnail width size.

> Default: 600

`SCHEDULER_THUMB_M_H`

Medium thumbnail height size.

> Default: 600

`SCHEDULER_THUMB_L_W`

Large thumbnail width size.

> Default: 2000

`SCHEDULER_THUMB_L_H`

Large thumbnail height size.

> Default: 2000


Cheers! :beers: