"""BasePage — Parent of all page objects."""

from playwright.sync_api import Page
from utils.hybrid_engine import HybridEngine
from utils.screenshot_util import capture


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.engine = HybridEngine(page)

    def navigate(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def reload(self):
        self.page.reload(wait_until="networkidle")

    def scroll_down(self, px=400):
        self.engine.scroll_down(px)

    def scroll_up(self, px=300):
        self.engine.scroll_up(px)

    def wait(self, ms=1000):
        self.engine.wait(ms)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def screenshot(self, name="screenshot"):
        return capture(self.page, name)
