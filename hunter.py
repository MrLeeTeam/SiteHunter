#coding:utf8


from datetime import datetime

import config
import ground
import database
from normalizer import URL


def init():
    config.init()
    database.init(config.get_database_info())


def main():
    ground_type = config.get_ground_type()
    ground_hunter = ground.get_ground(ground_type)

    while 1:
        try:
            seq_no = database.get_next_seq(config.get_ground_index())
            print "[", datetime.now(), "]", "#%d" % seq_no, " - ",
            site_url = ground_hunter.fetch_url(seq_no)
            print site_url,
            url_object = URL(site_url)

            if url_object.data["realm"] is None:
                print "(Unacceptable URL)"
                continue

            print "(", url_object.get_normal_url(), ")"
            database.register_new_site(url_object.get_normal_url(), url_object.data["realm"])

        except Exception, e:
            print e.message


if __name__ == "__main__":
    init()
    main()
