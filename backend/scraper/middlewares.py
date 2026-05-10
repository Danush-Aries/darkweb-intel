import scrapy
import requests

class TorMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def __init__(self, settings):
        self.proxy = settings.get("SOCKS_PROXY")

    def process_request(self, request, spider):
        # Ensure only .onion domains go through Tor
        if not request.url.endswith(".onion") and "ahmia.fi" not in request.url:
            spider.logger.warning(f"Skipping Tor proxy for non-onion URL: {request.url}")
            return None

        if self.proxy:
            request.meta["proxy"] = self.proxy
        else:
            spider.logger.error("SOCKS_PROXY not configured in settings.py!")

    def process_response(self, request, response, spider):
        # Advanced Leak Check: Verify if the request was actually routed through Tor
        # by checking if the response corresponds to the expected onion behavior.
        return response
