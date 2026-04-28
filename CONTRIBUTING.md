# Contributing Guide

Thanks for working on the SabPaisa Automation Test Suite. This guide gets you from zero to a merged PR in 15 minutes.

## Quick Start

```bash
git clone https://github.com/anjumwahid/sabpaisa-automation-suite.git
cd sabpaisa-automation-suite
pip install -r requirements.txt
playwright install chromium

# Verify setup
pytest tests/test_regression_suite.py -k "R1.1" --headed --slowmo 500
```

## Project Structure

```
config/        Settings (env, headless, slow-mo)
data/          Test data (merchant, customer, card, clients list)
pages/         Page Object Model (locators + actions per page)
tests/         All test cases (single file: test_regression_suite.py)
utils/         Hybrid Engine + screenshot util
reports/       Auto-generated (Excel + Allure)
```

## Adding a New Test

### 1. Choose the right section

| Section | Use for |
|---|---|
| R1 | Merchant configuration / Fetch flows |
| R2 | Customer form validation |
| R3 | UPI |
| R4 | Cards |
| R5 | Netbanking |
| R6 | Wallets |
| R7 | Offline (Cash/RTGS/IMPS) |
| R8 | Mode switching / stability |
| R10 | Per-client E2E (CHIN36, SUBI79) |
| R11 | Fee Forward |
| R12 | Fetch validation |
| R13 | Language |

### 2. Write the test

In `tests/test_regression_suite.py`:

```python
@allure.title("R5.12: My new test description")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.netbanking          # mode marker
@pytest.mark.smoke                # tier marker
def test_my_new_test(self, page):
    co = goto_checkout_for_client(page, "CHIN36")
    co.select_netbanking()
    # ... test logic ...
    assert co.is_pay_visible(), "Pay button should appear"
```

### 3. Add page object methods (if needed)

In `pages/checkout_page.py`:

```python
# Locator
NEW_BUTTON = {
    "xpath": "//button[normalize-space()='New Action']",
    "css": "button.new-action",
    "text": "New Action",
}

# Action
@allure.step("Click new action")
def click_new_action(self):
    self.engine.click(self.NEW_BUTTON, timeout=10000)
    self.wait(1000)
```

### 4. Verify

```bash
# Syntax check
python -c "import ast; ast.parse(open('tests/test_regression_suite.py').read())"

# Collect (don't run)
pytest tests/test_regression_suite.py --collect-only -q | grep my_new_test

# Run only your test
pytest tests/test_regression_suite.py::TestR5Netbanking::test_my_new_test --headed --slowmo 500
```

### 5. Commit

```bash
git add .
git commit -m "Add R5.12: my new test description"
git push
```

## Test Markers — Use Them

Always add appropriate markers so tests can be filtered:

```python
@pytest.mark.smoke         # Add if test runs in <30s and is critical
@pytest.mark.critical      # Add if release-blocking
@pytest.mark.regression    # Default — full suite
@pytest.mark.slow          # Add if test takes >2 min
@pytest.mark.netbanking    # Mode marker
@pytest.mark.chin36        # Client-specific
@pytest.mark.dynamic       # Dynamic per-item discovery tests
```

Run filtered:
```bash
pytest -m smoke                          # Just smoke
pytest -m "critical and not slow"        # Critical but quick
pytest -m "netbanking or wallets"        # Two modes
pytest -m "chin36 and regression"        # Per-client regression
```

## Coding Standards

### Page Object Model

- **One class per page** in `pages/`
- Locators as `dict` with `xpath`, `css`, `text` keys (HybridEngine tries each)
- Actions decorated with `@allure.step("Description")`
- Wait after actions: `self.wait(1000)`

### Test Naming

- `test_<positive_action>` for happy path
- `test_neg_<scenario>` for negative tests
- `test_<client>_<scenario>` for client-specific (e.g., `test_chin36_charges_visible`)

### Assertions

```python
# Bad — vague
assert co.is_pay_visible()

# Good — descriptive failure message
assert co.is_pay_visible(), f"Pay button should be visible after selecting bank, URL={page.url}"
```

### Don't

- ❌ Hardcode merchant IDs in tests (use `_dynamic_client()` for dynamic tests)
- ❌ Use `time.sleep()` (use `co.wait(ms)` or Playwright auto-waits)
- ❌ Skip Allure decorators (`@allure.title`, `@allure.severity`)
- ❌ Catch broad exceptions silently — log them

## Pull Request Checklist

- [ ] Test passes locally (`pytest -k <my_test> --headed --slowmo 500`)
- [ ] Allure report shows test with screenshots
- [ ] Pytest markers added (`@pytest.mark.smoke` etc.)
- [ ] CHANGELOG.md updated under `[Unreleased]` section
- [ ] No hardcoded credentials or URLs in test code (use `data/` or env vars)
- [ ] No new files in `screenshots/` or `reports/` (auto-generated, gitignored)
- [ ] README updated if new commands or env vars added

## Reporting Issues

Open a GitHub issue with:

1. **Test name** that fails
2. **Expected** behavior
3. **Actual** behavior
4. **Allure attachment** screenshot
5. **Browser console log** (if relevant)

## Architecture Decisions

- **Why single test file?** — Easier to onboard new testers; a big suite stays scannable
- **Why dict locators (`xpath`/`css`/`text`)?** — Resilient to UI changes; falls through 3 strategies
- **Why fresh-session per bank in dynamic tests?** — Mirrors real user behavior; isolates failures
- **Why pytest-playwright over raw Playwright?** — Better fixtures, parallelism, Allure integration

## Need Help?

- Ask in `#qa-automation` Slack channel
- Tag `@anjumwahid` in PR comments
- Check the `HANDOVER_GUIDE.pdf` first — covers most beginner questions
