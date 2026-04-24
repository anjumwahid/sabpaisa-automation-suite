# SabPaisa Payment Gateway — Automation Test Suite

## About
Automated regression test suite for the **SabPaisa Payment Gateway** checkout flow.
Built with **Playwright + Python**, Hybrid Page Object Model, Allure reports, and a
parallel multi-client batch runner with Excel + Allure HTML output.

- **Default Environment:** Staging (change via `config/settings.json` or `ENV=Production`)
- **Primary clients:** CHIN36 (Fee Forward YES), SUBI79 (Fee Forward NO)
- **Payment modes covered:** UPI, Cards, Netbanking, Wallets, Offline (Cash / RTGS / IMPS)

---

## Folder Structure

```
playwright_checkout_project/
|
|-- config/                             <-- SETTINGS
|   |-- settings.json                   <-- env, headless, slow-mo, viewport (edit this)
|   |-- settings_manager.py             <-- loader (no edit)
|
|-- data/                               <-- TEST DATA
|   |-- checkout_data.json              <-- merchant, customer, amount, card, UPI (edit this)
|   |-- clients.json                    <-- list of merchants for batch runs (edit this)
|   |-- data_provider.py                <-- loader (no edit)
|
|-- pages/                              <-- PAGE OBJECTS (locators + actions)
|   |-- base_page.py
|   |-- configure_page.py               <-- merchant fetch, env select, continue
|   |-- customer_page.py                <-- customer form
|   |-- checkout_page.py                <-- UPI / Cards / Netbanking / Wallets / Offline
|
|-- tests/
|   |-- test_regression_suite.py        <-- ALL regression tests (R1–R12)
|
|-- utils/
|   |-- hybrid_engine.py                <-- XPath → CSS → Text fallback locator engine
|   |-- screenshot_util.py              <-- auto-screenshot on failure, Allure attach
|
|-- reports/                            <-- Allure results & HTML (auto-generated)
|-- screenshots/                        <-- per-test screenshots (auto-generated)
|
|-- run_parallel_clients.py             <-- BATCH RUNNER — multi-client + Excel + Allure HTML
|-- conftest.py                         <-- browser fixtures + failure hook
|-- pytest.ini
|-- requirements.txt
|-- Dockerfile, docker-compose.yml      <-- containerized runs
|-- .github/workflows/                  <-- GitHub Actions CI
|-- bitbucket-pipelines.yml             <-- Bitbucket CI
|-- Jenkinsfile                         <-- Jenkins pipeline
```

---

## Setup (First Time Only)

```bash
# 1. Install Python packages
pip install -r requirements.txt

# 2. Install the browser
playwright install chromium

# 3. Install Allure CLI (for HTML reports)
#    scoop (Windows, recommended): scoop install allure
#    npm:                          npm install -g allure-commandline
```

---

## Where to Change Things in PyCharm

| What to change | File | Key field |
|---|---|---|
| Order amount for tests | `data/checkout_data.json` | `customer.amount` |
| Customer name / email / phone | `data/checkout_data.json` | `customer.*` |
| Card number / expiry / CVV | `data/checkout_data.json` | `card.*` |
| UPI ID | `data/checkout_data.json` | `upi.upi_id` |
| Default merchant (non-batch tests) | `data/checkout_data.json` | `merchant_id` |
| Batch run client list | `data/clients.json` | array |
| Staging / Production toggle | `config/settings.json` | `environment` |
| Headless on/off | `config/settings.json` | `headless` |
| Test speed (slow-mo) | `config/settings.json` | `slow_mo` |
| Viewport / timeouts | `config/settings.json` | `viewport`, `default_timeout` |

All other flow is code — page objects in `pages/`, tests in `tests/test_regression_suite.py`.

---

## How to Run — Complete Command Reference

Pick your goal below. All commands run from `playwright_checkout_project/`.

### 🎯 Quick decision guide

| Goal | Go to section |
|---|---|
| Run one particular mode (UPI / Cards / Wallets / …) | **§ 1** |
| Run all modes for one client (CHIN36 or SUBI79) | **§ 2** |
| Dynamic per-bank / per-wallet flow (full E2E per item) | **§ 3** |
| Run the entire regression (all 68 tests) | **§ 4** |
| Generate client-ready Excel + Allure HTML | **§ 5** |
| Just see the Allure report after any run | **§ 6** |
| Run in Docker | **§ 7** |
| Run via Jenkins / GitHub Actions / Bitbucket | **§ 8** |
| Override settings on the CLI (env / headless / …) | **§ 9** |

---

### § 1 — Particular Mode (one mode only)

```bash
# UPI
pytest tests/test_regression_suite.py::TestR3UPI --headed --slowmo 500

# Cards (Debit + Credit + negative cases)
pytest tests/test_regression_suite.py::TestR4Cards --headed --slowmo 500

# Netbanking (all 10 tests)
pytest tests/test_regression_suite.py::TestR5Netbanking --headed --slowmo 500

# Wallets
pytest tests/test_regression_suite.py::TestR6Wallets --headed --slowmo 500

# Offline (Cash / RTGS / IMPS)
pytest tests/test_regression_suite.py::TestR7Offline --headed --slowmo 500

# Fee Forward (CHIN36 YES / SUBI79 NO)
pytest tests/test_regression_suite.py::TestR11FeeForward --headed --slowmo 500

# Fetch validation
pytest tests/test_regression_suite.py::TestR12FetchValidation --headed --slowmo 500

# Language dropdown (EN / Hindi)
pytest tests/test_regression_suite.py::TestR13Language --headed --slowmo 500
```

---

### § 2 — All Modes for One Client

```bash
# CHIN36 — all 8 E2E tests one-by-one (UPI, Cards×2, Netbanking×2, Wallet, Offline×3)
pytest tests/test_regression_suite.py -k "chin36" --headed --slowmo 500

# SUBI79 — all 8 E2E tests
pytest tests/test_regression_suite.py -k "subi79" --headed --slowmo 500
```

---

### § 3 — Dynamic Per-Bank / Per-Wallet Flow

These discover what the client offers at runtime and run a fresh E2E session for each item:

```bash
# Wallets — every wallet CHIN36 offers (4 for CHIN36, 7 for others)
pytest tests/test_regression_suite.py::TestR6Wallets::test_all_wallets_per_flow --headed --slowmo 500

# Netbanking — every popular bank on checkout
pytest tests/test_regression_suite.py::TestR5Netbanking::test_netbanking_per_bank_flow --headed --slowmo 500

# Offline — every Cash/RTGS/IMPS bank
pytest tests/test_regression_suite.py::TestR7Offline::test_offline_per_bank_flow_dynamic --headed --slowmo 500

# All three together
pytest tests/test_regression_suite.py -k "per_bank_flow or per_flow" --headed --slowmo 500
```

---

### § 4 — Full Regression (all 68 tests)

```bash
# Headed with visible browser + Allure (best for manual review, ~30 min)
pytest tests/test_regression_suite.py --headed --slowmo 500 --alluredir=reports/allure-results

# Headless (fastest, ~15 min — use for CI)
pytest tests/test_regression_suite.py --alluredir=reports/allure-results -v

# Stop at first failure (debugging)
pytest tests/test_regression_suite.py --headed --slowmo 500 -x
```

---

### § 5 — Client-Ready Excel + Allure HTML (best for sharing results)

Use the batch runner `run_parallel_clients.py`:

```bash
# ⭐ One client only (CHIN36 end-to-end)
python run_parallel_clients.py --clients CHIN36 --workers 1

# ⭐ Two clients in parallel (CHIN36 + SUBI79)
python run_parallel_clients.py --clients CHIN36,SUBI79 --workers 2

# Faster — smoke only (E2E tests only, ~5 min)
python run_parallel_clients.py --clients CHIN36,SUBI79 --workers 2 --smoke

# Three clients in parallel
python run_parallel_clients.py --clients CHIN36,SUBI79,AJME --workers 3

# Every client in data/clients.json
python run_parallel_clients.py

# 10 parallel workers
python run_parallel_clients.py --workers 10
```

**Output**
- `reports/Client_Regression_Report_<timestamp>.xlsx` — 5 sheets: Summary + Cards + Netbanking + Wallets + Offline
- `reports/allure-report-<MERCHANT_ID>/` — static Allure HTML per client
- `screenshots/` — per-test PNGs

---

### § 6 — View Allure Report

```bash
# Live interactive server (recommended — opens in browser automatically)
allure serve reports/allure-results

# Per-client static HTML (after batch run)
allure open reports/allure-report-CHIN36
allure open reports/allure-report-SUBI79

# Generate static HTML from raw results (shareable folder)
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

**Open Excel (Windows)**:
```bash
start reports/Client_Regression_Report_*.xlsx
```

---

### § 7 — Docker

```bash
# Build the image
docker build -t sabpaisa-tests .

# Run the full regression inside the container, mount reports back to host
docker run --rm -v $(pwd)/reports:/app/reports sabpaisa-tests

# Run a specific section in Docker
docker run --rm -v $(pwd)/reports:/app/reports sabpaisa-tests \
  pytest tests/test_regression_suite.py -k "R11" --alluredir=reports/allure-results

# Override env vars at runtime
docker run --rm -e ENV=Production -e HEADLESS=true \
  -v $(pwd)/reports:/app/reports sabpaisa-tests

# Using docker-compose (simpler)
docker-compose up --build

# Stop and cleanup
docker-compose down
```

**View reports** after the container exits:
```bash
allure serve reports/allure-results
```

---

### § 8 — CI/CD (Jenkins / GitHub Actions / Bitbucket)

#### Jenkins — `Jenkinsfile`

The included `Jenkinsfile` is a declarative pipeline that works on Windows or Linux Jenkins agents:

```groovy
pipeline {
    agent any
    environment {
        HEADLESS = 'true'
        SLOW_MO  = '0'
        ENV      = 'staging'
    }
    stages {
        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'playwright install chromium'
            }
        }
        stage('Run Regression Tests') {
            steps {
                bat 'pytest tests/test_regression_suite.py --alluredir=allure-results -v'
            }
        }
    }
    post {
        always {
            allure results: [[path: 'allure-results']]
        }
    }
}
```

**Jenkins setup**
1. Install plugins: **Allure Jenkins Plugin**, **Pipeline**
2. Create a new **Pipeline** job → point to this repo → set Jenkinsfile path to `Jenkinsfile`
3. Trigger manually or configure SCM polling / webhooks
4. After run, click **Allure Report** link on the build page to view

**To customize the Jenkins run**, edit `Jenkinsfile`:
```groovy
// Only run smoke
bat 'pytest tests/test_regression_suite.py -k "R9 or R10" --alluredir=allure-results'

// Only CHIN36
bat 'pytest tests/test_regression_suite.py -k "chin36" --alluredir=allure-results'

// Use the parallel runner (Excel + Allure per client)
bat 'python run_parallel_clients.py --workers 5'
```

#### GitHub Actions — `.github/workflows/regression.yml`

**Triggers**: push to main/develop, PRs, scheduled (Mon-Fri 6 AM UTC), manual `workflow_dispatch`

```bash
# Trigger manually from GitHub UI → Actions tab → "Regression Suite" → Run workflow
# Or via gh CLI:
gh workflow run regression.yml
```

After run: **Actions tab → click run → download `allure-results` artifact → `allure serve` locally**

#### Bitbucket Pipelines — `bitbucket-pipelines.yml`

**Auto-triggers** on every push + two custom pipelines:
- `smoke-test` — only R9 + R10 E2E tests (fastest, ~5 min)
- `full-regression` — all 68 tests

**Run manually** from Bitbucket UI → Pipelines → Run pipeline → select `smoke-test` or `full-regression`

After run: **Pipelines → click run → Artifacts → download allure-results**

---

### § 9 — CLI Overrides (no file edits)

Any setting in `config/settings.json` can be overridden with environment variables:

| Variable | Default | Example |
|---|---|---|
| `ENV` | Staging | `ENV=Production` |
| `HEADLESS` | false | `HEADLESS=true` |
| `SLOW_MO` | 500 | `SLOW_MO=0` |
| `BASE_URL` | (from settings.json) | `BASE_URL=https://...` |
| `TIMEOUT` | 15000 | `TIMEOUT=30000` |
| `MERCHANT_ID_OVERRIDE` | (none) | `MERCHANT_ID_OVERRIDE=CHIN36` |

**Bash / Git Bash**:
```bash
ENV=Production pytest tests/test_regression_suite.py -k "R11"
HEADLESS=true SLOW_MO=0 pytest tests/test_regression_suite.py
MERCHANT_ID_OVERRIDE=CHIN36 pytest tests/test_regression_suite.py
```

**PowerShell**:
```powershell
$env:ENV="Production"; pytest tests/test_regression_suite.py -k "R11"
$env:HEADLESS="true"; $env:SLOW_MO="0"; pytest tests/test_regression_suite.py
```

**Docker**:
```bash
docker run --rm -e ENV=Production -e HEADLESS=true sabpaisa-tests
```

---

### 🏆 Most useful commands (star these)

```bash
# ⭐ Watch one mode in browser
pytest tests/test_regression_suite.py::TestR6Wallets::test_all_wallets_per_flow --headed --slowmo 500

# ⭐ All CHIN36 modes visible
pytest tests/test_regression_suite.py -k "chin36" --headed --slowmo 500

# ⭐ Client-ready Excel + Allure (CHIN36 + SUBI79 parallel)
python run_parallel_clients.py --clients CHIN36,SUBI79 --workers 2

# ⭐ Full regression headless for CI
pytest tests/test_regression_suite.py --alluredir=reports/allure-results

# ⭐ View last run's Allure
allure serve reports/allure-results
```

---

### 🔧 Troubleshooting

```bash
# Clean all caches + old reports before a fresh run
rm -rf __pycache__ */__pycache__ .pytest_cache
rm -rf reports/allure-results* reports/allure-report-*
rm -f screenshots/*.png reports/*.xlsx

# List all tests without running
pytest tests/test_regression_suite.py --collect-only -q

# Re-install Playwright browsers
playwright install chromium

# Check versions
pytest --version
allure --version
```

---

## Excel Report Layout (5 sheets)

The batch runner `run_parallel_clients.py` produces
`reports/Client_Regression_Report_<timestamp>.xlsx`:

| Sheet | Rows | Columns |
|---|---|---|
| **Summary** | 1 per client | Total / Passed / Failed / Config / UPI / Cards / Netbanking / Wallets / Offline / Overall Status |
| **Cards Detail** | 1 per client | Debit Card, Credit Card × PASS/FAIL/N/A |
| **Netbanking Detail** | 1 per client | 30 popular banks × PASS/FAIL/N/A |
| **Wallets Detail** | 1 per client | 7 wallets × PASS/FAIL/N/A |
| **Offline Detail** | 1 per client | Cash→ICICI, Cash→Airtel, Cash→FINO, Cash→BoI Retail, RTGS→IDFC, IMPS→SabPaisa |

Cells: 🟩 green = PASS · 🟥 red = FAIL · ⬜ grey = N/A

---

## Test Suite Summary

| Section | Class | Tests | What It Covers |
|---|---|---|---|
| **R1** | `TestR1MerchantConfig` | 6 | Open configure, fetch, invalid merchant, special chars, continue |
| **R2** | `TestR2CustomerForm` | 5 | Fill fields, empty, invalid email, zero/negative amount |
| **R3** | `TestR3UPI` | 2 | Select UPI, Generate QR |
| **R4** | `TestR4Cards` | 5 | Card form, fill, invalid/empty/expired card |
| **R5** | `TestR5Netbanking` | 10 | Equitas search, show/hide all banks, popular grid, full expanded list, IDFC → Pay → Cancel, **R5.10 recorded walkthrough** |
| **R6** | `TestR6Wallets` | 2 | Wallet grid, click all wallets (PhonePe / Amazon / MobiKwik / Airtel / FreeCharge / Jio / OLA) |
| **R7** | `TestR7Offline` | 5 | Cash, RTGS, IMPS; **R7.5 per-bank walkthrough with screenshots + challan verify** |
| **R8** | `TestR8Switching` | 4 | Switch all modes, rapid switch, card persistence, reload |
| **R9** | `TestR9E2ESmoke` | 5 | Netbanking / Cards / UPI / Wallet / Offline end-to-end smoke |
| **R10** | `TestR10_CHIN36`, `TestR10_SUBI79` | 16 | Mode-by-mode full E2E per client (CHIN36 = 8, SUBI79 = 8) |
| **R11** | `TestR11FeeForward` | 3 | **Fee Forward YES (CHIN36) / NO (SUBI79) — Convenience Charges visibility + math** |
| **R12** | `TestR12FetchValidation` | 3 | **Fetch click → green indicator / API URL populated; invalid merchant blocked; bypass-fetch detection** |
| **R13** | `TestR13Language` | 3 | **Checkout language dropdown — open, switch to Hindi, iterate all languages** |

**Total 68 tests, all in `tests/test_regression_suite.py`.**

### Dynamic per-bank/per-wallet flows (the R6.3 pattern)

Three tests follow the same **dynamic discovery + fresh session per item + verify real gateway** pattern:

| Test | What it does |
|---|---|
| **R5.11** `test_netbanking_per_bank_flow` | Discovers popular banks for the client → fresh session per bank → Pay → verify real gateway |
| **R6.3** `test_all_wallets_per_flow` | Discovers wallets enabled for the client (4 for CHIN36, N for another) → per-wallet E2E |
| **R7.6** `test_offline_per_bank_flow_dynamic` | Discovers Cash + RTGS + IMPS banks → fresh session per bank → Pay at bank → verify challan |

These scale with the client's actual offerings — no hardcoded bank/wallet lists.

### R2 amount/input edge cases (R2.5 — R2.8)

New customer-form stress tests:
- **R2.5** Negative amount (`-100`)
- **R2.6** Large amount (`23000`) — verifies reflection on checkout card
- **R2.7** Decimal amount (`99.99`)
- **R2.8** Hindi input — Devanagari name, customer ID, description (`राम कुमार`, `ग्राहक_१`, `परीक्षण उत्पाद`)

---

## New Feature Scenarios

### R7.5 — Offline walkthrough with per-bank screenshots

Each bank scenario gets a **fresh session** (configure → customer form → offline).
After selecting the bank and clicking **Pay at bank**, the test:

1. Screenshots the state **before** Pay (proves bank was selected)
2. Screenshots the state **after** Pay (challan / gateway / error dialog)
3. Verifies a challan / gateway page opened — PASS or FAIL

All screenshots land in `screenshots/` and attach to Allure for visual review.

### R11 — Fee Forward YES / NO

Validates the checkout summary card:
- **CHIN36 (Fee Forward = YES)** → `Convenience Charges` row MUST be visible
- **SUBI79 (Fee Forward = NO)** → `Convenience Charges` row MUST be hidden
- Math check: `Total Amount == Order Amount + Convenience Charges`

### R12 — Fetch validation

Catches the "user bypassed Fetch" bug where someone lands on the customer form
without a valid configured merchant:
- **R12.1** valid merchant → green indicator + API URL populated
- **R12.2** invalid merchant → no API URL populated, error shown
- **R12.3** skip Fetch → API URL empty (form submission should not reach valid checkout)

---

## How It Works (Architecture)

```
settings.json   -> WHERE to test (URL, env, headless, slow-mo)
checkout_data.json -> WHAT data (merchant, amount, customer, card)
clients.json    -> LIST of merchants for batch runs
pages/          -> HOW to interact (locators + actions per page)
tests/          -> WHAT to assert (R1–R12)
hybrid_engine   -> FINDS elements (XPath -> CSS -> Text, with scroll fallback)
screenshot_util -> AUTO captures on failure (+ Allure attach)
run_parallel_clients.py -> DRIVES multi-client batch + Excel + Allure HTML
Allure          -> REPORT (steps, screenshots, pass/fail)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Language |
| Playwright | Browser automation |
| Pytest | Test framework |
| Allure | Test reports |
| openpyxl | Multi-sheet Excel output |
| Hybrid POM | Architecture (locators + actions per page, data-driven) |
| Docker | Containerized execution |
| Jenkins / GitHub Actions / Bitbucket Pipelines | CI/CD |
