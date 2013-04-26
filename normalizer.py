#coding:utf8
import re


realm_Tistory = "Tistory"
realm_Daum = "Daum"
realm_Naver = "Naver"
realm_Egloos = "Egloos"



normal_mobile_form = {realm_Tistory: "http://%(id)s.tistory.com/m/%(post_no)s",
                      realm_Daum: "http://m.blog.daum.net/%(id)s/%(post_no)s",
                      realm_Naver: "http://m.blog.naver.com/%(id)s/%(post_no)s",
                      realm_Egloos: "http://%(id)s.egloos.com/m/%(post_no)s"}


normal_form = {realm_Tistory: "http://%(id)s.tistory.com/%(post_no)s",
               realm_Daum: "http://blog.daum.net/%(id)s/%(post_no)s",
               realm_Naver: "http://blog.naver.com/%(id)s/%(post_no)s",
               realm_Egloos: "http://%(id)s.egloos.com/%(post_no)s"}

normal_base_form = {realm_Tistory: "%(id)s.tistory.com",
                    realm_Daum: "blog.daum.net/%(id)s",
                    realm_Naver: "blog.naver.com/%(id)s",
                    realm_Egloos: "%(id)s.egloos.com"}


class URL(object):
    data = dict()

    def __init__(self, url):
        self.normalize(url)

    def normalize(self, url):
        author_id = None
        post_no = None
        realm = None


        if "tistory.com" in url:
            realm = realm_Tistory
            author_id = re.match(".*?([a-zA-Z0-9_-]+).tistory.com", url).group(1)
            post_no = re.match(".*?.tistory.com/([a-zA-Z0-9_-]+)", url).group(1)

        elif "blog.daum.net" in url:
            realm = realm_Daum
            author_id = re.match(".*?blog.daum.net/([a-zA-Z0-9_-]*)/", url).group(1)
            post_no = re.match(".*?blog.daum.net/[.a-zA-Z0-9_-]+/([a-zA-Z0-9_-]+)", url).group(1)

        elif "naver.com" in url:
            realm = realm_Naver
            author_id = re.match(".*?blog.naver.com/([.a-zA-Z0-9_-]+)/", url).group(1)
            post_no = re.match(".*?blog.naver.com/[a-zA-Z0-9_-]+/([a-zA-Z0-9_-]+)", url).group(1)

        elif "egloos.com" in url:
            realm = realm_Egloos
            author_id = re.match(".*?([a-zA-Z0-9_-]+).egloos.com/", url).group(1)
            post_no = re.match(".*?.egloos.com/([a-zA-Z0-9_-]+)", url).group(1)

        self.data["id"] = author_id
        self.data["post_no"] = post_no
        self.data["realm"] = realm

    def get_normal_form(self):
        return normal_form[self.data["realm"]] % self.data

    def get_normal_url(self):
        return normal_base_form[self.data["realm"]] % self.data

    def get_normal_mobile_form(self):
        return normal_mobile_form[self.data["realm"]] % self.data


