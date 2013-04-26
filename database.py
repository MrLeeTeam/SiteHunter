import sys
import psycopg2

con = None
db_info = None


def init(database_info):
    global db_info
    db_info = database_info
    connect_i()

def connect_i():
    global con
    global db_info
    con = psycopg2.connect(host=db_info["host"], database=db_info["database"], user=db_info["id"], password=db_info["pw"])


def get_next_seq(ground_index):
    global con

    seq_no = 0
    try:
        cursor = con.cursor()
        cursor.execute("SELECT seq_no from blog_ground where type = %s", ground_index)
        record = cursor.fetchone()

        if record:
            seq_no = record[0]

        cursor.execute("UPDATE blog_ground set seq_no = seq_no + 1 where type = %s", ground_index)
        con.commit()
    except Exception, e:
        print "[ERROR] get_next_seq - ", e.message

    return seq_no


def register_new_site(url, realm):
    global con
    try:
        cursor = con.cursor()
        cursor.execute("SELECT b_id FROM blog_meta where url = '%s'" % url)

        if cursor.fetchone() is None:
            cursor.execute("INSERT into blog_meta(url, realm) values (%s, %s)", (url, realm))
            con.commit()

    except Exception, e:
        print "[ERROR] register_new_site - ", e.message


