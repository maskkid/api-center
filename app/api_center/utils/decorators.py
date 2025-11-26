import time
import functools
import random

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    return wrapper

def require_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 在这里实现认证逻辑
        # 可以检查请求头中的token等
        return func(*args, **kwargs)
    return wrapper 


class DecoratedRequests:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebkit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    ]

    accept_language_list = [
        'en-US,en;q=0.9',
        'fr-FR,fr;q=0.9',
        'de-DE,de;q=0.9',
        'zh-CN,zh;q=0.9',
        'es-ES,es;q=0.9',
        'it-IT,it;q=0.9',
        'ja-JP,jp;q=0.9',
        'ko-KR,ko;q=0.9',
        'pt-BR,pt;q=0.9',
        'ru-RU,ru;q=0.9'
    ]

    def __init__(self, requests):
        self._requests = requests
        # 复制 requests 模块的所有公共属性
        for attr_name in dir(requests):
            if not attr_name.startswith('_'):
                setattr(self, attr_name, getattr(requests, attr_name))
        # 重写 get 和 post 方法
        self.get = self._get
        self.post = self._post

    def _get_headers(self, user_headers):
        random_user_agent = random.choice(self.user_agent_list)
        random_accept_language = random.choice(self.accept_language_list)
        my_headers = {
            'User-Agent': random_user_agent,
            'Accept': 'text/html,application/json,*/*',
            'Accept-Language': random_accept_language,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        if user_headers:
            final_headers = {**my_headers, **user_headers}
        else:
            final_headers = my_headers
        return final_headers

    def _get(self, *args, **kwargs):
        headers = self._get_headers(kwargs.get('headers'))
        kwargs['headers'] = headers
        return self._requests.get(*args, **kwargs)

    def _post(self, *args, **kwargs):
        headers = self._get_headers(kwargs.get('headers'))
        kwargs['headers'] = headers
        return self._requests.post(*args, **kwargs)

def decorate_requests(requests):
    return DecoratedRequests(requests)
