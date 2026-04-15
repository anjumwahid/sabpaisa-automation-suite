"""Conftest — Fixtures + Allure screenshot on failure."""

import pytest, allure
from config.settings_manager import HEADLESS, SLOW_MO, VIEWPORT
from utils.screenshot_util import capture


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": HEADLESS, "slow_mo": SLOW_MO}


@pytest.fixture
def browser_context_args():
    return {"viewport": VIEWPORT}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            page = item.funcargs.get("page")
            if page and not page.is_closed():
                capture(page, f"FAIL_{item.name.replace('[', '_').replace(']', '')}")
        except Exception:
            pass
