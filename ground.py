
import requests

DAUM_VIEW = 1
NAVER_BLOG = 2

Name = {DAUM_VIEW : "Daum", NAVER_BLOG : "Naver"}


class Ground(object):
    ground_type = 0
    base_url = None

    def __init__(self):
        pass

    def fetch_url(self, seq_no):
        ground_url = self.make_ground_url(seq_no)
        blog_url = self.extract_from_ground(ground_url)
        return blog_url


    def make_ground_url(self, seq_no):
        raise "Not implmented"

    def extract_from_ground(self, ground_url):
        raise "Not implmented"




class DaumView(Ground):

    def __init__(self):
        Ground.__init__(self)
        self.ground_type = DAUM_VIEW
        self.base_url = "http://v.daum.net"

    def make_ground_url(self, seq_no):
        return self.base_url + "/link/%d" % seq_no

    def extract_from_ground(self, ground_url):
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
        structure = requests.get(ground_url, headers={"User-Agent": agent}, timeout=5.0)
        try:
            url = structure.history[0].headers["location"]
        except:
            raise Exception("extract url failed")
        return url




class NaverBlog(Ground):

    def __init__(self):
        Ground.__init__(self)
        self.ground_type = DAUM_VIEW
        self.base_url = "http://v.daum.net"

    def make_ground_url(self, seq_no):
        pass

    def extract_from_ground(self, ground_url):
        pass



def get_ground(type):
    ground = None
    type = int(type)
    if type == DAUM_VIEW:
        ground = DaumView()
    elif type == NAVER_BLOG:
        ground = NaverBlog()

    return ground
