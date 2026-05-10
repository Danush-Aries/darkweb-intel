[global]
spider_modules = ["app.spiders"]
scrapy_playwright_enabled = True

# Playwright settings
PLAYWRIGHT_DEFAULT_TIMEOUT = 30000
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

# Tor Proxy Settings (assuming tor-proxy container is on port 9050)
SOCKS_PROXY = "socks5://tor-proxy:9050"

DOWNLOADER_MIDDLEWARES = {
    "backend.scraper.middlewares.TorMiddleware": 100,
}

# Scrapy Playwright
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "scrapy_playwright.reactor.AsynchronousSelectorReactor"
