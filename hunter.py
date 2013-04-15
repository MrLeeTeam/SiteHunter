#coding:utf8
import requests
import psycopg2
import normalizer
from lxml import html





def init_check():
    pass

def main():
    while True:
        url = get_url() ## get url from db
        if url == None:
            continue
        url_info = normalizer.normalize(url)
        saveNewSite(url_info)
        #print url
        #if isRegistered(url) == False:
        #    saveNewSite(url, realm)
        #break;


def get_url():
    # Get url from database
    link = get_new_link()
    url = extract_link(link)
    return url


def saveNewSite(data):
    # Save data to DB
    url = data["base"]
    realm = data["realm"]

    print url, realm
    try:
        con = psycopg2.connect(host="mrleesvr", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = con.cursor()

        cursor.execute("INSERT into blog_meta(url, realm) values ( %s, %s)", (url, realm))
        con.commit()
        con.close()
    except:
        print "ERROR net link"



def isRegistered(url):
    pass


def get_new_link():
    seq_no = 0
    try:
        con = psycopg2.connect(host="mrleesvr", database="mrlee", user="mrlee", password="altmxjfl")
        cursor = con.cursor()

        cursor.execute("SELECT seq_no from blog_ground where type = 1")

        record = cursor.fetchone()

        if record:
            seq_no = record[0]
        print "Get SEQ #%d" % seq_no
        cursor.execute("UPDATE blog_ground set seq_no = seq_no + 1")
        con.commit()
        con.close()
    except:
        print "ERROR net link"


    if seq_no != 0:
        return "http://v.daum.net/link/%s" % seq_no
    return None

def extract_link(url):
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"

    structure = requests.get(url, headers={"User-Agent": agent})
    try:
        url = structure.history[0].headers["location"]
    except:
        return None
    return url


if __name__ == "__main__":
    main()
