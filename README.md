# Python Threaded Mailer #

This is a simple implementation for thread based mailing using SMTP and MySQL

### Setting Up ###

* $ git clone https://whizzzkid@bitbucket.org/whizzzkid/python-threaded-mailer.git
* $ cd python-threaded-mailer
* $ mysql -u <username> -p < table.sql
* Configure mailer.py and populate_table.py
* $ python populate_table.py
* $ python mailer.py
* Dependencies: MySQL, MySQLdb, smtplib

### Author ###
Nishant Arora (me@nishantarora.in)