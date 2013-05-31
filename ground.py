
import requests
import json

DAUM_VIEW = 1
NAVER_SECTION = 2

Name = {DAUM_VIEW : "Daum", NAVER_SECTION : "Naver"}


class Ground(object):
    ground_type = 0
    base_url = None

    def __init__(self):
        pass

    def fetch_url(self, seq_no):
        request_info = self.make_request_info(seq_no)
        blog_url = self.extract_from_ground(request_info)
        return blog_url


    def make_request_info(self, seq_no):
        raise "Not implmented"

    def extract_from_ground(self, ground_url):
        raise "Not implmented"


class DaumView(Ground):

    def __init__(self):
        Ground.__init__(self)
        self.ground_type = DAUM_VIEW
        self.base_url = "http://v.daum.net"

    def make_request_info(self, seq_no):
        return {'url': self.base_url + "/link/%d" % seq_no}

    def extract_from_ground(self, ground_info):
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
        structure = requests.get(ground_info['url'], headers={"User-Agent": agent}, timeout=5.0)
        try:
            url = structure.history[0].headers["location"]
        except:
            raise Exception("extract url failed")
        return [url]




class NaverSection(Ground):

    def __init__(self):
        Ground.__init__(self)
        self.ground_type = NAVER_SECTION
        self.base_url = "http://m.blog.naver.com/DirectoryPostListAsync.nhn"

    def make_request_info(self, seq_no):
        header = {'Origin': 'http://m.blog.naver.com', 'Host': 'm.blog.naver.com', 'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'charset': 'utf-8', 'Referer': 'http://m.blog.naver.com/TopicList.nhn',
                'Connection': 'keep-alive', 'Accept-Charset': 'windows-949,utf-8;q=0.7,*;q=0.3'}
        data = {'seq': seq_no , 'page': seq_no, 'blogId': ''}
        return {'data': data, 'header': header, 'url' : self.base_url }
        pass

    def extract_from_ground(self, ground_info):
        dataset = ground_info['data']
        lists = set()

        for i in range(40):
            dataset['seq'] = i
            try:
                structure = requests.post(ground_info['url'], dataset, headers=ground_info['header'], timeout=5.0)
            except Exception, e:
                continue

            body = structure.text
            #print body
            body = body.encode(structure.encoding)

            lines = body.split("\n")


            for line in lines:
                if "blogId" in line:
                    id = line.replace("\"blogId\":\"", "").replace("\",","")
                    lists.add("blog.naver.com/%s/0" % id.strip())
                    #print line

        return lists



def get_ground(type):
    ground = None
    type = int(type)
    if type == DAUM_VIEW:
        ground = DaumView()
    elif type == NAVER_SECTION:
        ground = NaverSection()

    return ground


if __name__ == "__main__":
    naver = NaverSection()
    print naver.fetch_url(1)

