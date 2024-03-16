from typing import Optional, Callable, Dict

import requests

from backbone.configs import config
from backbone.crawler.helper.constant import DEFAULT_HEADERS


def request(url: str, callback: Callable, headers: Optional[Dict[str, str]] = None,
            meta: Optional[Dict[str, str]] = None):
    """
    :param url:
    :param callback:
    :param headers:
    :param meta:
    :return: scrapy.Request
    """

    headers = headers or DEFAULT_HEADERS

    try:
        req = Request(url=url, callback=callback, headers=headers, meta=meta)
        return req.request()
    except Exception as e:
        error = e

        try:
            req = Request(url="http:" + url, callback=callback, headers=headers, meta=meta)
            return req.request()
        except:
            raise error


class Request:
    def __init__(self, url, callback, headers=None, meta=None):
        self._meta = meta
        self._headers = headers or {}
        self._callback = callback
        self._url = url

    def get_url(self):
        return self._url

    def request(self):
        response = requests.get(self._url, headers=self._headers, timeout=10)
        return response


class RequestArgs:
    def __init__(self, callback: Callable, headers: Optional[Dict[str, str]] = None, url: str = None,
                 meta: dict = None):
        self._request_args: dict = {"headers": headers} if headers else {"headers": DEFAULT_HEADERS}
        self._request_args["url"] = url if url else ""
        self._request_args["meta"] = meta if meta else {}
        self.callback: Callable = callback

    def add_proxy(self, proxy: str) -> None:
        self._request_args["meta"]["proxy"] = proxy

    def add_meta(self, key, value):
        self._request_args["meta"][key] = value

    def add_header(self, headers: str) -> None:
        self._request_args["headers"] = {"headers": headers}

    def add_url(self, url: str) -> dict:
        self._request_args["url"] = url

    def get_arg(self) -> dict:
        return self._request_args

    def get_meta(self):
        return self._request_args["meta"]

    def get(self):
        args: dict = self._request_args
        return request(**args, callback=self.callback)
