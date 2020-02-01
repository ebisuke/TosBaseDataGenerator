import requests
import json
class WikiPoster:
    api="https://treeofsavior.fandom.com/ja/api.php"
    session=requests.Session()
    def __init(self,uri="https://treeofsavior.fandom.com/ja/api.php"):
        self.api=uri
    def login(self,username,password):
        ret=self.__postrequest(
        {
            "action":"query",
            "prop":"info",
            "titles":"Sandbox",
            "intoken":"edit",

        })
        data=ret.json()
        logintoken= data['query']['pages'][next(iter(data['query']['pages']))]['edittoken']

        ret = self.__postrequest(
        {
            "action": "login",
            "lgname": username,
            "lgpassword": password,
            "lgtoken": "",

        })

        ret = self.__postrequest(
        {
            "action": "edit",
            "title": "Sandbox",
            "text":"testtest",
            "token":""
        })
        data = ret.json()
        print(str(ret))

    def __getrequest(self,arg):
        arg["format"]="json"
        resp=self.session.get(self.api,params=arg)
        resp.raise_for_status()
        return resp

    def __postrequest(self,arg):
        arg["format"]="json"
        resp=self.session.post(self.api,params=arg)
        resp.raise_for_status()
        return resp