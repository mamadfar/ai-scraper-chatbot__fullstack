
from loguru import logger
from playwright import (
    Browser
)

class ScraperService:
    """ 
    Handles all web scraping logic

    Design decision: ScraperService manages its own Browser lifecycle.
    The browser is created on first use and reused across all scrape calls.
    This is the same battern as a DB connection pool

    In TS we'd do the same with a class that holds a shared Playwright Browser instance
    """

    def __init__(self):
        #? _browser is None until first use - lazy initialization
        # The underscore prefix means "private" (Python convention, not enforced)
        # Same as private browser: Browser | null = null in TS
        self._browser: Browser | None = None
        self._visited_urls: set[str] = set() # track visited URLs to avoid loops and duplicates

    async def _get_browser(self) -> Browser:
        """
        Returns the shared browser instance, creating it if needed
        This is the lazy singleton pattern for expensive resources
        """
        if self._browser is None or not self._browser.is_connected():
            logger.info("Launching Playwright browser...")