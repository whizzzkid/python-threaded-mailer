'''Will help populate test database with sample data.
The data should be in form of
<id> + <test_name> + <test_email> + <default_status=0>
'''

__author__ = "Nishant Arora (me@nishantarora.in)"

# imports
import MySQLdb

# DB Constants
DB_HOST = ''
DB_USER = ''
DB_PASS = ''
DB_DABA = ''
DB_TABL = ''

# Samples Count
REQ_NUM_SAMPLES = 10000

# Server Connection to MySQL
DB_SERVER = MySQLdb.connect(host=DB_HOST,
           user=DB_USER,
           passwd=DB_PASS,
           db=DB_DABA)
DB_CONN = DB_SERVER.cursor()

# Building Query.
SQL_QUERY = 'INSERT INTO ' + DB_TABL + \
' (`name`, `mail`, `status`) VALUES '

# For entire data set
for i in xrange(REQ_NUM_SAMPLES):
    SQL_QUERY += "('name" + str(i) + "', 'mail" + str(i) + \
    "@test.com', '0' )"
    if i != REQ_NUM_SAMPLES - 1:
        SQL_QUERY += ', '

#print command
try:
    DB_CONN.execute(SQL_QUERY)
    DB_SERVER.commit()
except Exception, error:
    print error
    DB_SERVER.rollback()

DB_SERVER.close()
