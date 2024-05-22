import time
from dataclasses import dataclass, field
from typing import Optional, Any

from bs4 import BeautifulSoup

from backbone.container.container import Provider, Container
from backbone.crawler.helper.helpers.requests import RequestArgs
from backbone.infrastructure.log.logger import Logger


@dataclass
class Response:
    url: Optional[str] = field(default=None)
    header: Optional[dict] = field(default=None)
    meta: Optional[Any] = field(default=None)
    content: Optional[Any] = field(default=None)
    body: Optional[Any] = field(default=None)
    request: RequestArgs = field(default=None)

    def __post_init__(self):
        self._css_selector = False
        self._find_selector = False

        response, request = self._get_request()
        if request is not None:
            if self.url is None:
                self.url = response.url
            if self.header is None:
                self.header = response.headers
            if self.content is None:
                self.content = response.content
            if self.meta is None:
                self.meta = request.get_meta()
            if self.body is None:
                self.body = response.text

    def _get_request(self):
        request = self.request
        self._count_fail_request = 0
        time_asked_again = 0
        for _ in range(3):
            time.sleep(time_asked_again)
            try:
                self._response_get = request.get()
                self._print_successfully()

                return self._response_get, request
            except Exception as e:
                if self._count_fail_request == 3:
                    raise ValueError(
                        f"fail count: {self._count_fail_request}  reference: {e.args}"
                    ) from e
                self._count_fail_request += 1
                time_asked_again += 3
                self._print_warning(e)

        raise ValueError("fail requested")

    def _print_successfully(self,logger: Logger = Provider[Container.logger]):
        logger.info(f"request successfully url: {self._response_get.url} | status: {self._response_get.status_code}")

    def _print_warning(self, e,logger: Logger = Provider[Container.logger]):
        logger.warning(f"fail count: {self._count_fail_request}  reference: {e.args if hasattr(e, 'args') else e}")

    def css(self, css_selector: str):
        self._css_selector = True
        self._selector = css_selector
        return self

    def find(self, tag, selector: dict):
        self._find_selector = True
        self._tag = tag
        self._selector = selector
        return self

    def get(self, attribute=None):
        if self._css_selector:
            return self._execute_css_selector()
        elif self._find_selector:
            if element := self._execute_object_selector():
                return element.get(attribute)
            else:
                return element

    def find_all(self, tag, class_=None) -> BeautifulSoup.find_all:
        soup_obj = BeautifulSoup(self.content, 'html.parser')
        return soup_obj.find_all(tag, class_=class_)

    def _execute_css_selector(self):
        soup_obj = BeautifulSoup(self.content, 'html.parser')
        if "::text" not in self._selector:
            return str(soup_obj.select(self._selector)[0])
        selector = self._selector.replace("::text", "")
        return soup_obj.select(selector)[0].get_text(strip=True)


    def _execute_object_selector(self):
        soup_obj = BeautifulSoup(self.content, 'html.parser')
        return soup_obj.find(self._tag, self._selector)
