# SabPaisa Payment Gateway - Automation Test Suite

## About
Automated regression test suite for **SabPaisa Payment Gateway** checkout flow using **Playwright + Python** with **Hybrid POM** architecture and **Allure Reports**.

**Environment:** Staging
**Client Code:** UTTA99
**Payment Modes:** UPI, Cards, Netbanking, Wallets, Offline Payment

---

## Folder Structure

```
playwright_checkout_project/
|
|-- config/                          <-- SETTINGS
|   |-- settings.json                <-- URL, browser, timeout (edit this)
|   |-- settings_manager.py          <-- Reads settings (DO NOT EDIT)
|
|-- data/                            <-- TEST DATA
|   |-- checkout_data.json           <-- Merchant ID, customer, card, bank
|   |-- negative_data.json           <-- Invalid/boundary test data
|   |-- data_provider.py             <-- Reads data files (DO NOT EDIT)
|
|-- pages/                           <-- PAGE OBJECTS (locators + actions)
|   |-- base_page.py                 <-- Common: click, fill, scroll, screenshot
|   |-- configure_page.py            <-- Merchant config (Staging/Production)
|   |-- customer_page.py             <-- Customer details form
|   |-- checkout_page.py             <-- All payment modes (UPI/Cards/Net/Wallet/Offline)
|
|-- tests/                           <-- TEST CASES
|   |-- test_checkout_flow.py        <-- Positive tests (26 cases)
|   |-- test_negative_checkout.py    <-- Negative tests (22 cases)
|   |-- test_sequential_all_modes.py <-- Sequential: all modes + all banks (6 cases)
|   |-- test_regression_suite.py     <-- Full regression suite (50 cases)
|   |-- test_all_banks_then_modes.py <-- All netbanks one by one then other modes (2 cases)
|
|-- utils/                           <-- HELPERS
|   |-- hybrid_engine.py             <-- Finds elements: XPath -> CSS -> Text fallback
|   |-- screenshot_util.py           <-- Auto screenshot on failure + Allure attach
|
|-- reports/                         <-- Allure report output (auto-generated)
|-- screenshots/                     <-- Failure screenshots (auto-saved)
|
|-- conftest.py                      <-- Browser fixtures + screenshot hook
|-- pytest.ini                       <-- Pytest config
|-- requirements.txt                 <-- Python packages
|-- .gitignore                       <-- Keeps repo clean
```

---

## Setup (First Time Only)

```bash
# 1. Install Python packages
pip install -r requirements.txt

# 2. Install browser
playwright install chromium

# 3. Install Allure CLI (for reports)
#    Option A: npm
npm install -g allure-commandline
#    Option B: pip
pip install allure-commandline
#    Option C: scoop (Windows)
scoop install allure
```

---

## How to Run Tests

### Run ALL tests (full regression)
```bash
pytest tests/ --alluredir=allure-results --headed --slowmo 500 -v -s
```

### Run specific section (example: only R5 Netbanking)
```bash
pytest tests/test_regression_suite.py -k "R5" --alluredir=allure-results --headed --slowmo 500 -v -s
```

### Run only E2E smoke tests
```bash
pytest tests/test_regression_suite.py -k "R9" --alluredir=allure-results --headed --slowmo 500 -v -s
```

### Run headless (no browser window - CI/CD)
```bash
pytest tests/ --alluredir=allure-results -v
```

---

## How to See Allure Report

### Option 1: Auto-open in browser
```bash
allure serve allure-results
```

### Option 2: Generate static HTML (share with client)
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

## Test Suite Summary

| Section | Cases | What It Covers |
|---------|-------|----------------|
| R1 - Merchant Config | 6 | Open, fetch, continue, invalid/special/no-fetch |
| R2 - Customer Form | 5 | Fill fields, empty, invalid email, zero/negative amount |
| R3 - UPI | 2 | Select UPI, Generate QR |
| R4 - Cards | 5 | Form, fill card, invalid/empty/expired card |
| R5 - Netbanking | 5 | Search Equitas, show all, click ALL banks, popular banks, non-existent |
| R6 - Wallets | 2 | Grid visible, click ALL wallets (PhonePe, Amazon, MobiKwik, Airtel, FreeCharge, Jio, OLA) |
| R7 - Offline | 3 | Options visible, Cash, Bank Of India |
| R8 - Switching | 4 | Switch all, rapid switch, card persistence, reload |
| R9 - E2E Smoke | 5 | Netbanking E2E, Cards E2E, UPI E2E, Wallet E2E, Offline E2E |
| R10 - Full Sequential | 1 | ALL banks one by one → Cards → UPI → ALL wallets → Offline |

**Total: 38 test cases (zero duplicates)**
**Single file: `tests/test_regression_suite.py`**

---

## Payment Modes Covered

| Mode | What Is Tested |
|------|---------------|
| **UPI** | Select UPI, Scan QR tab, Generate QR code |
| **Cards** | Card number, holder name, expiry, CVV, Pay button |
| **Netbanking** | Search bank, show all banks, click each bank individually |
| **Wallets** | PhonePe, AmazonPay, MobiKwik, Airtel Money, FreeCharge, Jio, OLA Money |
| **Offline** | Cash, Bank Of India (NEFT/RTGS/IMPS) |

---

## How to Change Test Data

### Change client code or customer details
Edit `data/checkout_data.json`:
```json
{
    "merchant_id": "UTTA99",
    "customer": {
        "customer_id": "Test",
        "name": "test",
        "email": "test@gmail.com",
        "phone": "6477834567",
        "amount": "1",
        "description": "Test Product"
    },
    "payment": { "bank_search": "eq", "bank_name": "Equitas Bank" },
    "card": { "card_number": "4111111111111111", "holder": "Test User", "expiry": "12/28", "cvv": "123" },
    "upi": { "upi_id": "test@ybl" }
}
```

### Change environment (Staging/Production)
Edit `config/settings.json`:
```json
{
    "base_url": "https://dgrdfsk1dqpwl.cloudfront.net/client-test/configure.html",
    "environment": "Staging",
    "browser": "chromium",
    "headless": false,
    "slow_mo": 500,
    "default_timeout": 15000
}
```

---

## Architecture (How It Works)

```
settings.json -----> WHERE to test (URL, environment, browser)
checkout_data.json -> WHAT data to use (merchant, customer, card, bank)
pages/ ------------> HOW to interact (locators + actions per page)
tests/ ------------> WHAT to test (positive, negative, regression)
hybrid_engine.py --> FINDS elements (XPath -> CSS -> Text fallback)
conftest.py -------> SETS UP browser (headed/headless, viewport)
Allure ------------> GENERATES report (steps, screenshots, pass/fail)
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Language |
| Playwright | Browser automation |
| Pytest | Test framework |
| Allure | Test reporting |
| Docker | Containerized test execution |
| Bitbucket Pipelines | CI/CD (Bitbucket) |
| GitHub Actions | CI/CD (GitHub) |
| Hybrid POM | Architecture (Page Objects + data-driven) |

---

## Docker

### Build and run tests in Docker
```bash
docker build -t sabpaisa-tests .
docker run --rm -v $(pwd)/allure-results:/app/allure-results sabpaisa-tests
```

### Using docker-compose
```bash
docker-compose up --build
```

### View report after Docker run
```bash
allure serve allure-results
```

---

## CI/CD — Bitbucket Pipelines

File: `bitbucket-pipelines.yml` (already included)

### Auto runs on every push to any branch

### Manual triggers:
- **Smoke Test** (E2E only): Run custom pipeline `smoke-test`
- **Full Regression**: Run custom pipeline `full-regression`

### View results:
- Allure results are saved as **pipeline artifacts**
- Download `allure-results` artifact → run `allure serve allure-results`

---

## CI/CD — GitHub Actions

File: `.github/workflows/regression.yml` (already included)

### Auto triggers:
- Push to `main` or `develop`
- Pull request to `main`
- Scheduled: Mon-Fri 6 AM UTC
- Manual: workflow_dispatch

### View results:
- Go to **Actions** tab → click run → download `allure-results` artifact
- Run `allure serve allure-results` locally

---

## Environment Variable Overrides (Docker / CI)

Override settings.json via ENV vars:

| Variable | Default | Example |
|----------|---------|---------|
| `ENV` | Staging | `ENV=Production` |
| `HEADLESS` | false | `HEADLESS=true` |
| `SLOW_MO` | 500 | `SLOW_MO=0` |
| `BASE_URL` | (from settings.json) | `BASE_URL=https://...` |
| `BROWSER` | chromium | `BROWSER=firefox` |
| `TIMEOUT` | 15000 | `TIMEOUT=30000` |

Example:
```bash
# Run headless in CI
HEADLESS=true SLOW_MO=0 pytest tests/ --alluredir=allure-results -v

# Run against Production
ENV=Production pytest tests/ --alluredir=allure-results -v
```

---

## Folder Structure (Final)

```
playwright_checkout_project/
|
|-- config/                          <-- Settings
|   |-- settings.json
|   |-- settings_manager.py          <-- Supports ENV overrides
|
|-- data/                            <-- Test data
|   |-- checkout_data.json
|   |-- negative_data.json
|   |-- data_provider.py
|
|-- pages/                           <-- Page Objects (Hybrid POM)
|   |-- base_page.py
|   |-- configure_page.py
|   |-- customer_page.py
|   |-- checkout_page.py
|
|-- tests/                           <-- Single regression file
|   |-- test_regression_suite.py     <-- 38 test cases (R1-R10)
|
|-- utils/                           <-- Helpers
|   |-- hybrid_engine.py
|   |-- screenshot_util.py
|
|-- reports/                         <-- Allure output
|-- screenshots/                     <-- Failure screenshots
|
|-- .github/workflows/regression.yml <-- GitHub Actions CI/CD
|-- bitbucket-pipelines.yml          <-- Bitbucket CI/CD
|-- Dockerfile                       <-- Docker image
|-- docker-compose.yml               <-- Docker compose
|-- .dockerignore
|-- .gitignore
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
|-- README.md
```
