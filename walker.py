import urllib3
import codecs
import json
import journal
import os
import subprocess
import argparse

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

    def download_nuget(self, list_packges):
        d = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(d + '/NuGetCachePath'):
            subprocess.PIPE('nuget.exe locals all -clear')
        else:
            os.mkdir(d + '/NuGetCachePath')

        for p, v in list_packges:
            # subprocess.PIPE('nuget.exe install ' + p + 'Version' + v)
            print('Pack ', p)
            print('Ver ', v)
        return 0



    def __str__(self):
        return "API = {0}, FEED = {1}, URL = {2}".format(self.api_key, self.feed, self.url)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--master')
    parser.add_argument('-s', '--slave')
    parser.add_argument('-ma', '--api_key_master')
    parser.add_argument('-sa', '--api_key_slave')
    parser.add_argument('-mf', '--feed_master')
    parser.add_argument('-sf', '--feed_slave')

    args = parser.parse_args()
    print('url_m: {0}, url_s: {1}, api_m: {2}, api_s: {3}, feed_m: {4}, feed_s: {5}'.format(args.master,
                                                                                            args.slave,
                                                                                            args.api_key_master,
                                                                                            args.api_key_slave,
                                                                                            args.feed_master,
                                                                                            args.feed_slave),
          sep=',')
    config = {'master': 'value1', 'slave': 'value2',
              'api_key_master': 'value1', 'api_key_slave': 'value2',
              'feed_master': 'value1', 'feed_slave': 'value2'}

    if not os.path.exists(os.path.realpath + '/config.json'):
        with open('config.json', 'w') as f:
            json.dump(config, f)

if __name__ == '__main__':
    #exit(cli())
    d = os.path.dirname(os.path.realpath(__file__))

    if os.path.exists(d + '/config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
            main = Walker(url=config['master'], feed=config['feed_master'], api_key=config['api_key_master'], DEBUG=0)
            mirror = Walker(url=config['slave'], feed=config['feed_slave'], api_key=config['api_key_slave'], DEBUG=0)
            m1 = mirror.get_nuget_packages_list()
            m = main.get_nuget_packages_list()
            j_main = journal.Journal()
            j_m1 = journal.Journal()
            j_main.insert_packs(m)
            j_m1.insert_packs(m1)
            print(j_main.get_table())
            print(j_m1.get_table())
            print('--------------------')
            diff = j_main.diff_table(j_m1)
            mirror.download_nuget(diff)

