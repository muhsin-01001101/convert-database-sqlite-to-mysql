Requirements
------------
NOTE: In this Example is used Ubuntu Terminal

* PHP 7.3 or higher;
* PDO-SQLite PHP extension enabled;
* Mysql;
* Python 3;

Installation
------------
Migrate SQLite database to MySQL database:

```bash
# Open the Database Directory
$ cd data/
# Here is used the sqlite .dump command, 
# in this case would be created a dump of the database.sqlite database.
$ sqlite3 database.sqlite .dump > dump.sql

$ cat dump.sql | python sqlite-to-mysql.py > dump-mysql.sql
```