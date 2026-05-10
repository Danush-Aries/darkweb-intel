import scrapy
from ..services.threat_scorer import calculate_threat_score

class DarkWebSpider(scrapy.Spider):
    name = "darkweb_spider"

    def __init__(self, keywords=None, *args, **kwargs):
        super(DarkWebSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords or []
        # Real DarkWeb Search Aggregators
        self.search_engines = {
            "ahmia": "http://ahmia.fi/search/?q={}",
            "torch": "http://torchde.onion/search?q={}", # Note: Torch is .onion, needs Tor
        }

    def start_requests(self):
        for keyword in self.keywords:
            for name, url_template in self.search_engines.items():
                target_url = url_template.format(keyword)
                yield scrapy.Request(
                    url=target_url,
                    meta={
                        "playwright": True,
                        "keyword": keyword,
                        "engine": name
                    },
                    callback=self.parse_search_results
                )

    async def parse_search_results(self, response):
        # Extract .onion links from search results
        # This is a simplified extractor; in production, this would be a more robust CSS/XPath selector
        links = response.css('a::attr(href)').getall()
        onion_links = [link for link in links if ".onion" in link]

        for link in onion_links:
            yield scrapy.Request(
                url=link,
                meta={
                    "playwright": True,
                    "keyword": response.meta.get("keyword"),
                    "from_engine": response.meta.get("engine")
                },
                callback=self.parse_content
            )

    async def parse_content(self, response):
        content = response.text
        keyword = response.meta.get("keyword")
        score = calculate_threat_score(content)

        yield {
            "keyword": keyword,
            "url": response.url,
            "content": content,
            "threat_score": score,
            "engine": response.meta.get("from_engine")
        }
