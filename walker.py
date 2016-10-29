from urllib3.request import RequestMethods

class Walker:
    def __init__(self, url, feed, api_key):
        self.url = url
        self.feed = feed
        self.api_key = api_key

    def getListPackages(self):
        pass

    def getFeedID(self):
        self.parametrs = {"API_Key": self.api_key, "Feed_Name": self.feed}
        self.response = RequestMethods.request(url=self.url+'/api/json/NuGetPackages_GetPackages?' + "API_Key=" + self.parametrs["API_Key"]  + '&' + 'Feed_Name=' )
        return self.response

if __name__ == '__main__':
    walker = Walker(url='http://172.30.114.63:81', feed='Default', api_key='WRsdqWhltrOLePrsgWxcvZasTGpfgG')
    walker.getFeedID()
