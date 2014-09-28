'''Bulk mailing script, with multi threading.'''

__author__ = "Nishant Arora (me@nishantarora.in)"

# imports
import MySQLdb
import smtplib
import threading

# DB Constants, check db_config.py
import db_config

# Threading Config
WORKER_THREAD_COUNT = 20

# SMTP Constants
SMTP_SERVER = 'some.mail.server.com'    # e.g: smtp.gmail.com
SMTP_PORT = 587                         # Common SMTP port
SMTP_USER = ''                          # SMTP User Credentials
SMTP_PASS = ''                          # SMTP Pass Credentials

# MAIL Constants
MAIL_SENDER = 'some_sender@domain.com'  # Sender's email
MAIL_SUBJECT = 'Some Subject Line'      # Subject Line, can be dynamic
MAIL_BODY = 'Some Body.'                # Mail body, can be dynamic

# Threading Class.
class ThreadFunction(threading.Thread):
    '''This class would help generate multiple threads.'''
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):

        # Server Connection to MySQL for Thread.
        db_server = MySQLdb.connect(host=DB_HOST,
                                    user=DB_USER,
                                    passwd=DB_PASS,
                                    db=DB_DABA)
        db_conn = db_server.cursor()

        # SMTP Mail server connection for thread.
        smtp_session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_session.ehlo()
        smtp_session.starttls()
        smtp_session.login(SMTP_USER, SMTP_PASS)

        # Looping till we have rows available.
        while True:

            # Fetching One row for processing and locking row with
            # MySQL InnoDB FOR UPDATE clause.
            db_conn.execute("""SELECT * FROM """ + \
            DB_TABL + """ WHERE status=0 LIMIT 1 FOR UPDATE""")
            row = db_conn.fetchone()

            # If we have a row, else break.
            if row:

                # Constructing Mail Headers.
                mail_recipient = row[2]
                mail_headers = ["From: " + MAIL_SENDER,
                "Subject: " + MAIL_SUBJECT,
                "To: " + mail_recipient,
                "MIME-Version: 1.0",
                "Content-Type: text/html"]

                # Easier to concat.
                mail_headers = "\r\n".join(mail_headers)

                # Sending mail through already existing server connection.
                smtp_session.sendmail(MAIL_SENDER, mail_recipient, \
                mail_headers + "\r\n\r\n" + MAIL_BODY)

                # Updating Table, and releasing row lock.
                db_conn.execute("""UPDATE """ + DB_TABL + \
                """ SET status=1, sent_time=NOW(),""" + \
                """ thread=CONCAT(thread, %s) WHERE id=%s""", \
                (self.name, int(row[0])))

                # Commiting change to MySQL server
                db_server.commit()
            else:
                break
        # Closing connections once the thread is done.
        db_server.close()
        smtp_session.quit()

# Python list to maintain all thread instances
ALL_THREADS = []

# Starting all the threads
for i in xrange(WORKER_THREAD_COUNT):
    thread = ThreadFunction('thread' + str(i))
    thread.start()
    ALL_THREADS.append(thread)

# Waiting for all threas to finish
for thread in ALL_THREADS:
    thread.join()

# Blurting out statistics.
def get_output_from_db(query):
    '''Returns output from database as list'''
    db_server = MySQLdb.connect(host=DB_HOST,
                                user=DB_USER,
                                passwd=DB_PASS,
                                db=DB_DABA)
    db_conn = db_server.cursor()
    db_conn.execute(query)
    result = db_conn.fetchall()
    db_conn.close()
    return result

def print_results(result):
    '''Prints results to console'''
    for row in result:
        print row[0], ' : ', row[1], 'Records Processed'

print '===== Time Performance ====='
print_results(get_output_from_db("SELECT sent_time, COUNT( * ) " \
"FROM  `mailing_list` GROUP BY sent_time"))
print '===== Thread Performance ====='
print_results(get_output_from_db("SELECT thread, COUNT( * ) "\
"FROM  `mailing_list` GROUP BY thread"))
