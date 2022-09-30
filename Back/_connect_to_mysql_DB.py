import MySQLdb
import os
from dotenv import load_dotenv
# import pandas as pd
import attendence as at

load_dotenv()

db = MySQLdb.connect(host=os.getenv('HOST'),
                     port=int(os.getenv('PORT')), # your host, usually localhost
                     user=os.getenv('USER'),         # your username
                     passwd=os.getenv('PASSWD'),  # your password
                     db=os.getenv('DB'))        # name of the data base

db.autocommit(True)

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

#cur = db.cursor()
# cur.execute(
#     "DROP TABLE attendance_total ")
#

def fill_the_table():
    if not checkTableExists(db, "attendance_total"):
        cur = db.cursor() 
	cur.execute("CREATE TABLE attendance_total (student_name varchar(128),attTime double(10,2), lec_time double(10,2),att_percent_time double(4,2),more_then_70_perc varchar(15))")
        result = at.read_from_csv()
        for index, row in result.iterrows():
            print(row["Name"], row["Total atendance time (min)"], row["Total lecture time (min)"], row["% Attendance time"],row["More then 70% Attendence"])
            cur.execute(
                "INSERT INTO attendance_total (student_name ,attTime , lec_time ,att_percent_time ,more_then_70_perc ) VALUES (%s,%s,%s,%s,%s)",(row["Name"], row["Total atendance time (min)"], row["Total lecture time (min)"], row["% Attendance time"],row["More then 70% Attendence"]))
	cur.close()

fill_the_table()
# studentName:  attTime: lecTime:  attPercentTime: moreThen70perc:

# you must create a Cursor object. It will let
#  you execute all the queries you need
# cur = db.cursor()
#
# # Use all the SQL you like
# cur.execute("SELECT * FROM user")
#
# # print all the first cell of all the rows
# for row in cur.fetchall():
#     print(row)

# db.close()
