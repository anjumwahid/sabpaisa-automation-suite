import os, allure
from datetime import datetime
from playwright.sync_api import Page

_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


def capture(page: Page, name: str = "screenshot"):
    os.makedirs(_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(_DIR, f"{name}_{ts}.png")
    page.screenshot(path=path, full_page=True)
    allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
    print(f"    [Screenshot] {path}")
    return path
