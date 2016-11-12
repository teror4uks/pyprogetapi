import urllib3
import codecs
import json
import journal

class Walker:
    def __init__(self, url, feed, api_key, DEBUG=0):
        self.url = url
        self.feed = feed
        self.api_key = api_key
        Walker.DEBUG = DEBUG

    def getlistpackages(self):
        pass

    def getfeedid(self):
        reader = codecs.getreader('utf-8')
        parametrs = {"API_Key": self.api_key, "Feed_Name": self.feed}
        http = urllib3.PoolManager()
        response = http.request(method='GET', url=self.url \
                                    + '/api/json/Feeds_GetFeed?' \
                                    + "API_Key=" \
                                    + parametrs["API_Key"] \
                                    + '&' + 'Feed_Name=' \
                                    + parametrs["Feed_Name"], preload_content=False)
        result = json.load(reader(response))

        if Walker.DEBUG == 1:
            print('Feed_Id: ',result['Feed_Id'])
        return result['Feed_Id']

    def get_nuget_packages_list(self):
        reader = codecs.getreader('utf-8')
        _feed_id = self.getfeedid()
        parametrs = {"API_Key": self.api_key, "Feed_Id": _feed_id}
        http = urllib3.PoolManager()
        response = http.request(method='GET', url=self.url \
                                                  + '/api/json/NuGetPackages_GetPackages?' \
                                                  + "API_Key=" \
                                                  + parametrs["API_Key"] \
                                                  + '&' + 'Feed_Id=' \
                                                  + str(parametrs["Feed_Id"]), preload_content=False)
        result = json.load(reader(response))

        if Walker.DEBUG == 1:
            #print(result[1]['Package_Id']) ['Version_Text']['Published_Date']
            #print(result[0])
            res = self._get_format_nuget_pack_list(result)
            print(res)
        result = self._get_format_nuget_pack_list(result)
        return result

    def _get_format_nuget_pack_list(self, json_list):
        ar = []
        for res in json_list:
            temp = {}
            for pack_id in res.keys():
                if pack_id == 'Package_Id':
                    temp[pack_id] = res[pack_id]
                    ar.append(temp)
                if pack_id == 'Version_Text':
                    temp[pack_id] = res[pack_id]
        return ar

    def __str__(self):
        return "API = {0}, FEED = {1}, URL = {2}".format(self.api_key, self.feed, self.url)

if __name__ == '__main__':
    main = Walker(url='http://172.30.114.63:81', feed='Default', api_key='WRsdqWhltrOLePrsgWxcvZasTGpfgG', DEBUG=0)
    mirror = Walker(url='http://172.30.96.16:81', feed='Mirror1', api_key='JsrWEks923s2gQ2K93GKSm45s5a3Ff2', DEBUG=0)
    m1 = mirror.get_nuget_packages_list()
    m = main.get_nuget_packages_list()
    j_main = journal.Journal()
    j_m1 = journal.Journal()
    j_main.insert_packs(m)
    j_m1.insert_packs(m1)
    print(j_main.get_table())
    print(j_m1.get_table())
    print('--------------------')
    print(j_main.diff_table(j_m1))
