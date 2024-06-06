import requests


class Proxy():
    def __init__(self):
        res = requests.get(
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=json")
        self.dict = res.json()

    def get_random_proxy(self):
        return self.dict['proxies'][0]

    def get_proxies(self):
        return self.dict['proxies']

    def get_proxies_by_country(self, country):
        return [proxy for proxy in self.dict['proxies'] if proxy['ip_data']['country'].lower() == country.lower()]

    def get_proxies_by_protocol(self, protocol):
        return [proxy for proxy in self.dict['proxies'] if proxy['protocol'].lower() == protocol.lower()]

    def get_proxies_by_country_and_protocol(self, country, protocol):
        return [proxy for proxy in self.dict['proxies'] if
                proxy['ip_data']['country'].lower() == country.lower() and proxy[
                    'protocol'].lower() == protocol.lower()]

    def get_http_and_false_ssl(self):
        return [proxy for proxy in self.dict['proxies'] if
                proxy['protocol'].lower() == 'http' and proxy['ssl'] == False and proxy['anonymity'].lower() == 'elite']

    @staticmethod
    def is_proxy_working(proxy):
        proxy_link = 'http://{}'.format(proxy)
        try:
            response = requests.get('https://google.com', proxies={"http": proxy_link}, timeout=5)
            if response.status_code == 200:
                return True
        except:
            return False
        return False
