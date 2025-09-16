import asyncio
import tldextract
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config.config import Config
from pathlib import Path

async def main():
    config = Config()
    
    if config.mode == "Crawl":
        browser_conf = BrowserConfig(headless=True)  # or False to see the browser
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS
        )


        async with AsyncWebCrawler(config=browser_conf) as crawler:
            for url in config.urls:
                print(f"Crawling URL: {url}")
                result = await crawler.arun(url, run_config=run_conf)

                ext = tldextract.extract(result.url)
                domain = f"{ext.domain}.{ext.suffix}"
  
                folder = Path(f"html/{domain}")
                folder.mkdir(parents=True, exist_ok=True)

                with open(f"html/{domain}/{hash_url(result.url)}.html", "w", encoding="utf-8") as f:
                    f.write(result.cleaned_html)
                

def hash_url(url: str) -> str:
    import hashlib
    return hashlib.md5(url.encode()).hexdigest()

if __name__ == "__main__":
    asyncio.run(main())
    
