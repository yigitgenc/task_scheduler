# task_scheduler

Concurrent thread management prototype.

## Installation

Go to project directory and type the commands below respectively.

```
$ sqlite3 task_scheduler.db
```

Load `seed.sql` by typing `.read seed.sql`
```
SQLite version 3.19.3 2017-06-27 16:48:08
Enter ".help" for usage hints.
$ sqlite> .read seed.sql
```

Install `virtualenv` into the project and activate it.
```
$ virtualenv .
$ source bin/activate
```

To run scheduler, type:
```
$ python src/sheduler.py
```

Cheers! :beers: