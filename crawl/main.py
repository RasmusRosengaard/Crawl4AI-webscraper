import asyncio
from pathlib import Path
import hashlib
import tldextract
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config.config import Config  

QUEUE_FILE = Path("config/queue.queue")
LOG_FILE = Path("config/visited.log")


async def main():
    config = Config()

    if config.mode != "Crawl":
        print(f"Mode is '{config.mode}', exiting.")
        return

    queue = load_queue(config.url)
    visited = load_visited()


    ext = tldextract.extract(config.url)
    start_domain = f"{ext.domain}.{ext.suffix}"

    browser_conf = BrowserConfig(headless=True)
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        while queue:
            url = queue.pop(0)
            if url in visited:
                continue

            result = await crawler.arun(url, run_config=run_conf)
            visited.add(url)
            save_visited(url)

            folder = Path(f"html/{start_domain}")
            folder.mkdir(parents=True, exist_ok=True)
            file_path = folder / f"{hash_url(result.url)}.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result.cleaned_html)

            soup = BeautifulSoup(result.cleaned_html, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http') and href not in visited and href not in queue:
                    ext = tldextract.extract(href)
                    domain = f"{ext.domain}.{ext.suffix}"
                    if domain == start_domain:
                        queue.append(href)

            save_queue(queue)


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def load_queue(start_url: list[str]) -> list[str]:
    if QUEUE_FILE.exists():
        print("Loading queue from file.")
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    return [start_url]

def save_queue(queue: list[str]):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        for url in queue:
            f.write(url + "\n")

def load_visited() -> set[str]:
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_visited(url: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

if __name__ == "__main__":
    asyncio.run(main())
