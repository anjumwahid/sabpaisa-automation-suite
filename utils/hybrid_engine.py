"""
Hybrid Locator Engine
Tries 3 strategies in order: XPath -> CSS -> Text
Two-pass: visible first, then attached + scroll into view.
"""

from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeout
from config.settings_manager import DEFAULT_TIMEOUT


class HybridEngine:

    def __init__(self, page: Page):
        self.page = page

    def find(self, locator_dict: dict, timeout=DEFAULT_TIMEOUT) -> Locator:
        strategies = self._build(locator_dict)

        for name, loc in strategies:
            try:
                loc.first.wait_for(state="visible", timeout=timeout)
                return loc.first
            except PlaywrightTimeout:
                print(f"    [!] [{name}] visible timed out, trying next...")

        for name, loc in strategies:
            try:
                loc.first.wait_for(state="attached", timeout=5000)
                print(f"    [*] [{name}] attached - scrolling into view...")
                loc.first.scroll_into_view_if_needed()
                return loc.first
            except PlaywrightTimeout:
                continue

        raise Exception(f"Element not found: {locator_dict}")

    def click(self, locator_dict: dict, timeout=DEFAULT_TIMEOUT):
        el = self.find(locator_dict, timeout)
        try:
            el.click(timeout=5000)
        except PlaywrightTimeout:
            print("    [!] Normal click failed, force clicking...")
            el.click(force=True)

    def fill(self, locator_dict: dict, value: str, timeout=DEFAULT_TIMEOUT):
        el = self.find(locator_dict, timeout)
        el.clear()
        el.fill(value)

    def get_text(self, locator_dict: dict, timeout=DEFAULT_TIMEOUT) -> str:
        return self.find(locator_dict, timeout).inner_text()

    def is_visible(self, locator_dict: dict, timeout=3000) -> bool:
        try:
            self.find(locator_dict, timeout)
            return True
        except Exception:
            return False

    def scroll_down(self, px=400):
        self.page.evaluate(f"window.scrollBy(0, {px})")

    def scroll_up(self, px=300):
        self.page.evaluate(f"window.scrollBy(0, -{px})")

    def wait(self, ms=1000):
        self.page.wait_for_timeout(ms)

    def _build(self, d: dict) -> list:
        s = []
        if "xpath" in d:
            s.append(("xpath", self.page.locator(f"xpath={d['xpath']}")))
        if "css" in d:
            s.append(("css", self.page.locator(d["css"])))
        if "text" in d:
            s.append(("text", self.page.get_by_text(d["text"])))
        return s
