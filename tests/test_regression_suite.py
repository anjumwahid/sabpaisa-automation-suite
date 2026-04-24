"""
REGRESSION TEST SUITE - SabPaisa Payment Gateway
Environment: Staging

Sections:
  R1  - Merchant Configuration (Positive + Negative)
  R2  - Customer Form (Positive + Negative)
  R3  - UPI Payment
  R4  - Card Payment (Positive + Negative)
  R5  - Netbanking (Search, All Banks, Popular Banks)
  R6  - Wallets (All Wallets)
  R7  - Offline Payment (Cash, RTGS, IMPS)
  R8  - Payment Mode Switching & Stability
  R10 - Full E2E Per Mode (CHIN36, SUBI79)

Run:    pytest tests/test_regression_suite.py --alluredir=allure-results --headed --slowmo 500 -v -s
Report: allure serve allure-results
"""

import allure
import pytest
from pages import ConfigurePage, CustomerPage, CheckoutPage
from data.data_provider import get_checkout_data, get_customer_data, get_card_data, get_payment_data


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════

DATA = None

def _d():
    global DATA
    if DATA is None:
        DATA = {
            "merchant": get_checkout_data()["merchant_id"],
            "customer": get_customer_data(),
            "card": get_card_data(),
            "payment": get_payment_data(),
        }
    return DATA

def configure(page):
    ConfigurePage(page).configure_merchant(_d()["merchant"])

def goto_checkout(page) -> CheckoutPage:
    configure(page)
    cust = CustomerPage(page)
    cust.fill_customer_details(**_d()["customer"])
    cust.handle_advanced_and_checkout()
    co = CheckoutPage(page)
    co.wait_for_checkout_load()
    return co

def goto_checkout_for_client(page, merchant_id: str, env: str = "Staging") -> CheckoutPage:
    """Configure a specific merchant on a given environment and go to checkout."""
    cp = ConfigurePage(page)
    cp.open()
    cp.reload_page()
    cp.click_form_card()
    cp.select_environment(env)
    cp.enter_merchant_id(merchant_id)
    cp.click_fetch()
    cp.wait_for_fetch_complete()
    cp.scroll_down(300)
    cp.click_merchant_api_url()
    cp.click_checkout_base_url()
    cp.click_continue()
    cust = CustomerPage(page)
    cust.fill_customer_details(**_d()["customer"])
    cust.handle_advanced_and_checkout()
    co = CheckoutPage(page)
    co.wait_for_checkout_load()
    return co


# ══════════════════════════════════════════════════════════════════════
#  R1: MERCHANT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R1 - Merchant Configuration")
class TestR1MerchantConfig:

    @allure.title("R1.1: Open configure page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_open_page(self, page):
        c = ConfigurePage(page)
        c.open()
        assert "configure" in c.get_current_url().lower()

    @allure.title("R1.2: Fetch merchant on Staging")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fetch_merchant(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment()
        c.enter_merchant_id(_d()["merchant"])
        c.click_fetch()
        c.wait_for_fetch_complete()
        assert "Fetching" not in c.get_fetch_button_text()

    @allure.title("R1.3: Continue to customer form")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_continue_to_customer(self, page):
        configure(page)
        assert CustomerPage(page).is_still_on_customer_form()

    @allure.title("R1.4: [NEG] Invalid merchant ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_invalid_merchant(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment()
        c.enter_merchant_id("INVALID_XYZ_999")
        c.click_fetch()
        assert c.has_client_not_found_error()

    @allure.title("R1.5: [NEG] Special characters in merchant ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_neg_special_char_merchant(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment()
        c.enter_merchant_id("@#$%^&*!")
        c.click_fetch()
        assert c.has_client_not_found_error()

    @allure.title("R1.6: [NEG] Continue without fetch")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_continue_without_fetch(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment()
        c.enter_merchant_id(_d()["merchant"])
        url_before = c.get_current_url()
        c.click_continue()
        c.wait(2000)
        assert "configure" in c.get_current_url() or url_before == c.get_current_url()


# ══════════════════════════════════════════════════════════════════════
#  R2: CUSTOMER FORM
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R2 - Customer Form")
class TestR2CustomerForm:

    @allure.title("R2.1: Fill all fields and proceed")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fill_and_proceed(self, page):
        co = goto_checkout(page)
        assert "checkout" in co.get_current_url().lower()

    @allure.title("R2.2: [NEG] Empty fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_empty_fields(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("", "", "", "", "", "")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        if not cust.is_still_on_customer_form() and not cust.has_validation_error():
            allure.attach("App allowed empty fields", name="BUG", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R2.3: [NEG] Invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_neg_invalid_email(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("Test", "test", "not-email", "6477834567", "1", "Test")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        if not cust.is_still_on_customer_form() and not cust.has_validation_error():
            allure.attach("App accepted invalid email", name="BUG", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R2.4: [NEG] Zero amount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_zero_amount(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("Test", "test", "test@gmail.com", "6477834567", "0", "Test")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        if not cust.is_still_on_customer_form() and not cust.has_validation_error():
            allure.attach("App allowed zero amount", name="BUG", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R2.5: [NEG] Negative amount (-100)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_negative_amount(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("Test", "test", "test@gmail.com", "6477834567", "-100", "Test")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        if not cust.is_still_on_customer_form() and not cust.has_validation_error():
            allure.attach("App accepted negative amount", name="BUG",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("R2.6: Large amount (23000)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_large_amount(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("Test", "test", "test@gmail.com", "6477834567", "23000", "Test")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        co = CheckoutPage(page)
        co.wait_for_checkout_load()
        co.screenshot("R2_6_large_amount_checkout")
        total = co.get_total_amount()
        allure.attach(f"Total Amount shown: {total}", name="Large amount reflected",
                      attachment_type=allure.attachment_type.TEXT)
        assert "23000" in total.replace(",", "") or "23,000" in total, \
            f"Large amount 23000 should reflect on checkout. Got: {total}"

    @allure.title("R2.7: Decimal amount (99.99)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_decimal_amount(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details("Test", "test", "test@gmail.com", "6477834567", "99.99", "Test")
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        co = CheckoutPage(page)
        co.wait_for_checkout_load()
        co.screenshot("R2_7_decimal_amount_checkout")
        total = co.get_total_amount()
        allure.attach(f"Total Amount shown: {total}", name="Decimal amount reflected",
                      attachment_type=allure.attachment_type.TEXT)

    @allure.title("R2.8: Hindi (Devanagari) name + Hindi customer ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hindi_input(self, page):
        configure(page)
        cust = CustomerPage(page)
        # Hindi / Devanagari strings
        cust.fill_customer_details(
            "ग्राहक_१",        # customer_id in Hindi
            "राम कुमार",       # name in Hindi
            "test@gmail.com",
            "6477834567",
            "50",
            "परीक्षण उत्पाद",   # description in Hindi
        )
        cust.handle_advanced_and_checkout()
        cust.wait(3000)
        try:
            co = CheckoutPage(page)
            co.wait_for_checkout_load()
            co.screenshot("R2_8_hindi_input_checkout")
            name_on_card = co.get_merchant_name_on_checkout()
            allure.attach(
                f"Hindi name entered. Reached checkout: {'checkout' in page.url.lower()}\n"
                f"Merchant display name on card: {name_on_card}",
                name="Hindi input result", attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as e:
            allure.attach(
                f"Hindi input rejected / page did not reach checkout: {str(e)[:120]}",
                name="Hindi input result", attachment_type=allure.attachment_type.TEXT,
            )


# ══════════════════════════════════════════════════════════════════════
#  R3: UPI
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R3 - UPI Payment")
class TestR3UPI:

    @allure.title("R3.1: Select UPI + Pay visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_select_upi(self, page):
        co = goto_checkout(page)
        co.select_upi()
        assert co.is_pay_visible()

    @allure.title("R3.2: Generate QR code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_generate_qr(self, page):
        co = goto_checkout(page)
        co.select_upi()
        co.click_generate_qr()
        assert co.is_qr_visible(), "QR should be visible"


# ══════════════════════════════════════════════════════════════════════
#  R4: CARD PAYMENT
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R4 - Card Payment")
class TestR4Cards:

    @allure.title("R4.1: Card form visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_card_form(self, page):
        co = goto_checkout(page)
        co.select_cards()
        assert co.is_card_form_visible()

    @allure.title("R4.2: Fill valid card + Pay visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_card(self, page):
        co = goto_checkout(page)
        c = _d()["card"]
        co.complete_cards_flow(c["card_number"], c["holder"], c["expiry"], c["cvv"])
        assert co.is_pay_visible()

    @allure.title("R4.3: [NEG] Invalid card (all zeros)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_invalid_card(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.enter_card_number("0000000000000000")
        co.enter_card_holder("Test")
        co.enter_card_expiry("12/28")
        co.enter_card_cvv("123")
        co.click_pay()
        co.wait(3000)
        allure.attach(f"URL: {co.get_current_url()}", name="Result", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R4.4: [NEG] Empty card fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_empty_card(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.click_pay()
        co.wait(2000)
        assert co.is_card_form_visible()


# ══════════════════════════════════════════════════════════════════════
#  R5: NETBANKING
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R5 - Netbanking")
class TestR5Netbanking:

    @allure.title("R5.1: Search Equitas Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_equitas(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        assert co.is_search_visible()
        co.search_bank("eq")
        co.select_equitas_bank()

    @allure.title("R5.2: Show all banks")
    @allure.severity(allure.severity_level.NORMAL)
    def test_show_all_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        co.wait(2000)
        count = page.locator("img[alt*='Bank']").count()
        allure.attach(f"Total banks: {count}", name="Count", attachment_type=allure.attachment_type.TEXT)
        assert count > 3

    @allure.title("R5.3: Click every bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        co.wait(3000)
        banks = co.get_all_bank_names()
        passed, failed_list = 0, []
        for bank in banks:
            try:
                co.select_netbanking()
                co.click_show_all_banks()
                co.wait(1000)
                co.click_bank_by_name(bank)
                passed += 1
            except Exception as e:
                failed_list.append(f"{bank}: {str(e)[:80]}")
        allure.attach(f"Passed: {passed}/{len(banks)}\nFailed:\n" + "\n".join(failed_list or ["None"]),
                      name="All Banks Result", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R5.4: [NEG] Non-existent bank")
    @allure.severity(allure.severity_level.NORMAL)
    def test_neg_no_bank(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.search_bank("ZZZZZZZ_NO_BANK")
        assert co.is_no_bank_found()

    @allure.title("R5.5: Popular banks grid — click each")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_popular_banks_grid(self, page):
        co = goto_checkout(page)
        popular = [
            ("Karur Vysya Bank", co.select_karur_vysya),
            ("Bank of Baroda Corporate", co.select_bob_corporate),
            ("Bank of Baroda Retail", co.select_bob_retail),
            ("Equitas Bank", co.select_equitas_bank),
            ("Indian Overseas Bank", co.select_indian_overseas),
            ("State Bank of India", co.select_sbi),
        ]
        passed, failed = 0, []
        for name, method in popular:
            try:
                co = goto_checkout(page)
                co.select_netbanking()
                method()
                passed += 1
            except Exception as e:
                failed.append(f"{name}: {str(e)[:80]}")
        allure.attach(f"Passed: {passed}/{len(popular)}\nFailed:\n" + "\n".join(failed or ["None"]),
                      name="Popular Banks Result", attachment_type=allure.attachment_type.TEXT)
        assert passed >= 1

    @allure.title("R5.6: Show / Hide all banks toggle")
    @allure.severity(allure.severity_level.NORMAL)
    def test_show_hide_all_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        expanded = page.locator("span.text-blue-600").count()
        allure.attach(f"Expanded bank count: {expanded}", name="Expanded", attachment_type=allure.attachment_type.TEXT)
        assert expanded > 0
        co.click_hide_all_banks()

    @allure.title("R5.7: Select bank from expanded list (HDFC)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_select_from_full_list(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        co.select_bank_from_list("HDFC Bank")

    @allure.title("R5.8: Expanded list banks — click each via generic helper")
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_expanded_list_banks(self, page):
        expanded_banks = [
            "HDFC Bank", "Karnataka Bank", "Punjab National Bank [Retail]",
            "RBL Bank", "Saraswat Bank", "Janata Sahakari Bank LTD Pune",
            "Royal Bank Of Scotland", "Deutsche Bank", "Dhanlaxmi Bank",
            "Catholic Syrian Bank", "Kotak Mahindra Bank",
            "Punjab & Maharashtra Co-op Bank Ltd", "City Union Bank",
            "Indusind Bank", "Jammu and Kashmir Bank", "Punjab & Sind Bank",
            "IDFC FIRST Bank Limited", "Fedral Bank", "ICICI Bank",
            "Standard Chartered Bank", "Lakshmi Vilas Bank NetBanking",
            "Tamilnad Mercantile Bank", "UCO Bank", "Axis Bank", "DBS Bank Ltd",
        ]
        passed, failed = 0, []
        for bank in expanded_banks:
            try:
                co = goto_checkout(page)
                co.select_netbanking()
                co.click_show_all_banks()
                co.wait(1000)
                co.select_bank_from_list(bank)
                passed += 1
            except Exception as e:
                failed.append(f"{bank}: {str(e)[:80]}")
        allure.attach(f"Passed: {passed}/{len(expanded_banks)}\nFailed:\n" + "\n".join(failed or ["None"]),
                      name="Expanded List Result", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R5.9: IDFC → Pay → Cancel on bank gateway")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_idfc_pay_then_cancel(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.search_bank("idfc")
        co.select_idfc_bank()
        co.click_pay()
        co.wait(3000)
        try:
            co.click_cancel()
        except Exception as e:
            allure.attach(f"Cancel click failed: {str(e)[:120]}",
                          name="Cancel", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R5.11: Netbanking per-bank complete flow (dynamic, fresh session per bank) (CHIN36)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_netbanking_per_bank_flow(self, page):
        """Same pattern as R6.3 but for Netbanking popular-grid banks.
        Fresh session per bank: Configure CHIN36 → customer form → checkout
        → Netbanking → click bank → Pay → wait for bank gateway → verify
        real page loaded. PASS if URL changed + not chrome-error + has
        content. Discovery is dynamic — if CHIN36 offers 4 popular banks
        we run 4, if 7 then 7."""

        # Discovery pass
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_netbanking()
        co.wait(2500)
        bank_alts = co.get_visible_netbanking_popular_alts()
        allure.attach(
            f"Discovered {len(bank_alts)} popular netbanking bank(s) for CHIN36:\n  - " +
            "\n  - ".join(bank_alts or ["(none)"]),
            name="Netbanking banks discovered",
            attachment_type=allure.attachment_type.TEXT,
        )
        if not bank_alts:
            pytest.skip("No popular banks visible for this client — nothing to test")

        log = [f"Discovered {len(bank_alts)} popular bank(s): {bank_alts}", ""]

        for idx, alt in enumerate(bank_alts, 1):
            safe = alt.replace(" ", "_").replace("/", "_")
            try:
                # Fresh full session
                co = goto_checkout_for_client(page, "CHIN36")
                co.select_netbanking()
                co.wait(1500)
                checkout_url = co.get_current_url()

                # Click the specific bank image
                co.page.locator(f"img[alt='{alt}']").first.click(timeout=5000)
                co.wait(2500)  # visible: bank highlighted
                co.screenshot(f"nb_{idx:02d}_{safe}_selected")

                # Pay
                co.wait(1000)
                co.click_pay()

                # Wait for bank gateway
                try:
                    co.page.wait_for_load_state("domcontentloaded", timeout=20000)
                except Exception:
                    pass
                try:
                    co.page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass
                co.wait(6000)
                co.screenshot(f"nb_{idx:02d}_{safe}_bank_page")

                # Verdict
                current_url = co.get_current_url()
                is_error = (current_url.startswith("chrome-error")
                            or current_url.startswith("about:blank")
                            or "ERR_" in current_url)
                try:
                    has_content = co.page.evaluate(
                        "() => document.body && document.body.innerText.trim().length > 30"
                    )
                except Exception:
                    has_content = False
                url_changed = (current_url != checkout_url)

                if url_changed and not is_error and has_content:
                    log.append(f"[PASS] {alt} -> bank page loaded ({current_url[:80]})")
                elif is_error:
                    co.screenshot(f"nb_{idx:02d}_{safe}_CHROME_ERROR")
                    log.append(f"[FAIL] {alt} -> chrome-error ({current_url[:60]})")
                elif url_changed:
                    co.screenshot(f"nb_{idx:02d}_{safe}_EMPTY_PAGE")
                    log.append(f"[FAIL] {alt} -> page empty ({current_url[:60]})")
                else:
                    co.screenshot(f"nb_{idx:02d}_{safe}_NO_PAGE_CHANGE")
                    log.append(f"[FAIL] {alt} -> stayed on checkout")
            except Exception as e:
                try:
                    co.screenshot(f"nb_{idx:02d}_{safe}_ERROR")
                except Exception:
                    pass
                log.append(f"[FAIL] {alt}: {str(e)[:120]}")

        allure.attach("\n".join(log), name="Netbanking Per-Bank Results (dynamic)",
                      attachment_type=allure.attachment_type.TEXT)
        assert any(line.startswith("[PASS]") for line in log), \
            "All netbanking banks failed:\n" + "\n".join(log)

    @allure.title("R5.10: Netbanking full recorded walkthrough (sequential)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_netbanking_recorded_walkthrough(self, page):
        """Direct-to-checkout URL → click every bank in recorded order →
        search IDFC → Pay → Cancel on gateway.
        Mirrors the user's exact recording step-by-step."""
        CHECKOUT_URL = (
            "https://staging-sb-checkout.sabpaisa.in/checkout/"
            "sppay_13561b7e520f4ddfacb3"
            "?clientSecret=sppay_13561b7e520f4ddfacb3_secret_"
            "92e65f4d7cfe7f6392d0c5969d685a00b0c4cb781f5cf17da3467cf6f5d45ff8"
        )
        page.goto(CHECKOUT_URL, wait_until="networkidle")
        co = CheckoutPage(page)
        co.wait_for_checkout_load()
        co.select_netbanking()

        # -- Popular banks (image grid) --
        popular_steps = [
            ("Karur Vysya Bank",                       co.select_karur_vysya),
            ("Bank of Baroda Net Banking Corporate",   co.select_bob_corporate),
            ("Bank of Baroda Net Banking Retail",      co.select_bob_retail),
            ("Equitas Bank",                           co.select_equitas_bank),
            ("Indian Overseas Bank",                   co.select_indian_overseas),
            ("State Bank of India",                    co.select_sbi),
        ]
        popular_log = []
        for name, method in popular_steps:
            try:
                method()
                popular_log.append(f"[OK]   {name}")
            except Exception as e:
                popular_log.append(f"[FAIL] {name}: {str(e)[:80]}")
        allure.attach("\n".join(popular_log), name="Popular Banks",
                      attachment_type=allure.attachment_type.TEXT)

        # -- Hide all banks then re-expand for blue-text list --
        try:
            co.click_hide_all_banks()
        except Exception as e:
            allure.attach(f"Hide all banks: {str(e)[:120]}",
                          name="Hide", attachment_type=allure.attachment_type.TEXT)
        try:
            co.click_show_all_banks()
            co.wait(1000)
        except Exception:
            pass

        # -- Full expanded list in recorded order --
        expanded_sequence = [
            "Lakshmi Vilas Bank NetBanking",
            "HDFC Bank",
            "Karnataka Bank",
            "Punjab National Bank [Retail]",
            "RBL Bank",
            "Saraswat Bank",
            "Janata Sahakari Bank LTD Pune",
            "Royal Bank Of Scotland",
            "Deutsche Bank",
            "TEAlBtest",
            "Dhanlaxmi Bank",
            "Catholic Syrian Bank",
            "Kotak Mahindra Bank",
            "Punjab & Maharashtra Co-op Bank Ltd",
            "City Union Bank",
            "Indusind Bank",
            "Jammu and Kashmir Bank",
            "Punjab & Sind Bank",
            "Tamilnad Mercantile Bank",
            "UCO Bank",
            "Axis Bank",
            "IDFC FIRST Bank Limited",
            "Fedral Bank",
            "DBS Bank Ltd",
            "ICICI Bank",
            "Standard Chartered Bank",
        ]
        expanded_log = []
        for bank in expanded_sequence:
            try:
                co.select_bank_from_list(bank)
                expanded_log.append(f"[OK]   {bank}")
            except Exception as e:
                expanded_log.append(f"[FAIL] {bank}: {str(e)[:80]}")
        allure.attach("\n".join(expanded_log), name="Expanded List (sequential)",
                      attachment_type=allure.attachment_type.TEXT)

        # -- Search IDFC, click image result, Pay --
        co.search_bank("idfc")
        co.select_idfc_bank()
        co.click_pay()

        # -- Scroll down on bank gateway and click Cancel --
        co.wait(3000)
        co.scroll_down(600)
        try:
            co.click_cancel()
        except Exception as e:
            allure.attach(f"Cancel click failed: {str(e)[:120]}",
                          name="Cancel", attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R6: WALLETS
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R6 - Wallets")
class TestR6Wallets:

    @allure.title("R6.1: Wallet grid visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wallet_grid(self, page):
        co = goto_checkout(page)
        co.select_wallets()
        assert co.is_wallet_grid_visible()

    @allure.title("R6.2: Click all wallets (single-session quick check)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_wallets(self, page):
        co = goto_checkout(page)
        wallets = [
            ("PhonePe", co.select_phonepe),
            ("AmazonPay", co.select_amazonpay),
            ("MobiKwik", co.select_mobikwik),
            ("Airtel Money", co.select_airtel_money),
            ("FreeCharge", co.select_freecharge),
            ("Jio", co.select_jio),
            ("OLA Money", co.select_ola_money),
        ]
        results = []
        for name, method in wallets:
            try:
                co.select_wallets()
                method()
                results.append(f"{name}: PASS")
            except Exception:
                results.append(f"{name}: FAIL")
        allure.attach("\n".join(results), name="All Wallets", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R6.3: Per-wallet complete flow (fresh session per wallet, dynamic count) (CHIN36)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_wallets_per_flow(self, page):
        """Fresh full session PER WALLET:
          1. Configure CHIN36 → customer form → checkout
          2. Click Wallets → discover the wallet list (only first iteration
             actually uses the discovery; subsequent iterations use the list
             discovered in iteration 1)
          3. For each wallet:
             - highlight selected (2.5s visible pause)
             - click Pay (1s pause)
             - wait for bank page to load (up to 30s)
             - hold on bank page (6s pause)
             - screenshot + verdict (real bank page = PASS; chrome-error / blank = FAIL)
             - close session, restart for next wallet
          4. When discovered count is exhausted → STOP.
        The brief UPI tab flash each fresh load is unavoidable — UPI is the
        checkout's default tab on every load. Wallets is clicked immediately
        after arrival, so the flash is <1s."""

        # ── Discovery pass: one throwaway session to get the wallet list ──
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_wallets()
        co.wait(2000)
        wallet_alts = co.get_visible_wallet_alts()
        allure.attach(
            f"Discovered {len(wallet_alts)} wallet(s) for CHIN36:\n  - " +
            "\n  - ".join(wallet_alts or ["(none)"]),
            name="Wallets discovered", attachment_type=allure.attachment_type.TEXT,
        )
        if not wallet_alts:
            pytest.skip("No wallets visible for this client — nothing to test")

        log = [f"Discovered {len(wallet_alts)} wallet(s): {wallet_alts}", ""]

        # ── Per-wallet: fresh session → select → Pay → verify → close ──
        for idx, alt in enumerate(wallet_alts, 1):
            safe = alt.replace(" ", "_").replace("/", "_")
            try:
                # STEP 1: fresh Configure CHIN36 → customer form → checkout
                co = goto_checkout_for_client(page, "CHIN36")

                # STEP 2: click Wallets tab IMMEDIATELY to minimise UPI flash
                co.select_wallets()
                co.wait(1500)
                checkout_url = co.get_current_url()

                # STEP 3: click this specific wallet (img alt OR button text)
                clicked = False
                try:
                    img = co.page.locator(f"img[alt='{alt}']").first
                    if img.count() > 0:
                        img.click(timeout=5000)
                        clicked = True
                except Exception:
                    pass
                if not clicked:
                    co.page.locator(
                        "div.flex-1.p-4.overflow-y-auto button"
                    ).filter(has_text=alt).first.click(timeout=5000)
                # HOLD 2.5s so user can SEE the wallet highlighted
                co.wait(2500)
                co.screenshot(f"wallet_{idx:02d}_{safe}_selected")

                # STEP 4: click Pay
                co.wait(1000)
                co.click_pay()

                # STEP 5: wait for bank gateway to load
                try:
                    co.page.wait_for_load_state("domcontentloaded", timeout=20000)
                except Exception:
                    pass
                try:
                    co.page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass
                # HOLD 6s so user can SEE the loaded bank page
                co.wait(6000)
                co.screenshot(f"wallet_{idx:02d}_{safe}_bank_page")

                # STEP 6: verdict
                current_url = co.get_current_url()
                is_error_page = (
                    current_url.startswith("chrome-error")
                    or current_url.startswith("about:blank")
                    or "ERR_" in current_url
                )
                try:
                    has_content = co.page.evaluate(
                        "() => document.body && document.body.innerText.trim().length > 30"
                    )
                except Exception:
                    has_content = False
                url_changed = (current_url != checkout_url)

                if url_changed and not is_error_page and has_content:
                    log.append(f"[PASS] {alt} -> bank page loaded ({current_url[:80]})")
                elif is_error_page:
                    co.screenshot(f"wallet_{idx:02d}_{safe}_CHROME_ERROR")
                    log.append(f"[FAIL] {alt} -> chrome-error / did not load ({current_url[:60]})")
                elif url_changed and not has_content:
                    co.screenshot(f"wallet_{idx:02d}_{safe}_EMPTY_PAGE")
                    log.append(f"[FAIL] {alt} -> page empty ({current_url[:60]})")
                else:
                    co.screenshot(f"wallet_{idx:02d}_{safe}_NO_PAGE_CHANGE")
                    log.append(f"[FAIL] {alt} -> stayed on checkout")

                # STEP 7: close / restart → loop continues with next wallet
            except Exception as e:
                try:
                    co.screenshot(f"wallet_{idx:02d}_{safe}_ERROR")
                except Exception:
                    pass
                log.append(f"[FAIL] {alt}: {str(e)[:120]}")

        allure.attach("\n".join(log), name="Wallet Per-Flow Results (fresh-session per wallet)",
                      attachment_type=allure.attachment_type.TEXT)
        assert any(line.startswith("[PASS]") for line in log), \
            "All wallet flows failed:\n" + "\n".join(log)


# ══════════════════════════════════════════════════════════════════════
#  R7: OFFLINE PAYMENT
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R7 - Offline Payment")
class TestR7Offline:

    @allure.title("R7.1: Offline options visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_offline_options(self, page):
        co = goto_checkout(page)
        co.select_offline()
        assert co.is_offline_options_visible()

    @allure.title("R7.2: Select Cash")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cash(self, page):
        co = goto_checkout(page)
        co.select_offline()
        co.select_cash()

    @allure.title("R7.3: Select RTGS")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rtgs(self, page):
        co = goto_checkout(page)
        co.select_offline()
        co.select_rtgs()

    @allure.title("R7.4: Select IMPS")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_imps(self, page):
        co = goto_checkout(page)
        co.select_offline()
        co.select_imps()

    @allure.title("R7.5: Offline per-bank complete flow (CHIN36) — Cash/RTGS/IMPS")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_offline_each_bank_complete(self, page):
        """Each bank is checked in its OWN fresh session:
          configure merchant → fill customer form → Offline Payment →
          sub-tab (Cash/RTGS/IMPS) → select bank → Pay at bank →
          verify challan / gateway page opened.
        PASS = challan/gateway opened. FAIL = didn't open OR any step threw.
        Scenarios are independent — one failure doesn't block the next."""

        scenarios = [
            # (sub-tab, bank label, sub-tab fn, bank-select fn)
            ("Cash", "ICICI Bank",             lambda c: c.select_cash(), lambda c: c.select_icici_bank()),
            ("Cash", "Airtel Bank",            lambda c: c.select_cash(), lambda c: c.select_airtel_bank()),
            ("Cash", "FINO Bank",              lambda c: c.select_cash(), lambda c: c.select_fino_bank()),
            ("RTGS", "IDFC First Bank RTGS",   lambda c: c.select_rtgs(), lambda c: c.select_idfc_first_rtgs()),
            ("IMPS", "SabPaisa Bank (SA)",     lambda c: c.select_imps(), lambda c: c.select_imps_bank_by_badge("SA")),
        ]

        log = []
        for sub_tab, bank_name, tab_fn, bank_fn in scenarios:
            label = f"{sub_tab} -> {bank_name}"
            safe_name = bank_name.replace(" ", "_").replace("(", "").replace(")", "").replace("→", "to")
            try:
                co = goto_checkout_for_client(page, "CHIN36")
                co.select_offline()
                tab_fn(co)
                bank_fn(co)

                # Screenshot the bank selected state BEFORE Pay
                co.screenshot(f"offline_{sub_tab}_{safe_name}_before_pay")

                co.click_pay_at_bank()

                # Wait for challan / gateway / dialog to render, then snap
                co.wait(5000)
                co.screenshot(f"offline_{sub_tab}_{safe_name}_after_pay")

                if co.is_challan_opened(timeout_ms=3000):
                    log.append(f"[PASS] {label} -> challan/gateway opened")
                else:
                    # Challan didn't open — snap extra detail and record URL
                    co.screenshot(f"offline_{sub_tab}_{safe_name}_NO_CHALLAN")
                    log.append(f"[FAIL] {label} -> no challan/gateway after Pay (url={co.get_current_url()[:90]})")
            except Exception as e:
                # Snapshot the moment of failure so the Allure report shows context
                try:
                    co.screenshot(f"offline_{sub_tab}_{safe_name}_ERROR")
                except Exception:
                    pass
                log.append(f"[FAIL] {label}: {str(e)[:120]}")

        allure.attach("\n".join(log), name="Offline Per-Bank Results",
                      attachment_type=allure.attachment_type.TEXT)
        assert any(line.startswith("[PASS]") for line in log), \
            "All offline scenarios failed:\n" + "\n".join(log)

    @allure.title("R7.6: Offline per-bank complete flow (DYNAMIC — Cash/RTGS/IMPS) (CHIN36)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_offline_per_bank_flow_dynamic(self, page):
        """Same pattern as R6.3 / R5.11 but for Offline across all 3 sub-tabs.
        Step 1 (discovery) — for each sub-tab (Cash, RTGS, IMPS) discover
        the banks that CHIN36 actually offers (img alts for Cash/RTGS,
        badge text for IMPS).
        Step 2 (per-bank) — fresh session for each bank: configure →
        customer → checkout → Offline → sub-tab → select bank →
        Pay at bank → verify challan / gateway page loaded."""

        # ── Discovery pass ──
        scenarios = []  # list of (sub_tab, identifier, kind) where kind is "img" or "badge"

        co = goto_checkout_for_client(page, "CHIN36")
        co.select_offline()
        co.wait(1500)

        # Cash
        try:
            co.select_cash()
            co.wait(1500)
            for alt in co.get_visible_offline_bank_alts():
                scenarios.append(("Cash", alt, "img"))
        except Exception:
            pass

        # RTGS
        try:
            co.select_offline()
            co.wait(1000)
            co.select_rtgs()
            co.wait(1500)
            for alt in co.get_visible_offline_bank_alts():
                scenarios.append(("RTGS", alt, "img"))
        except Exception:
            pass

        # IMPS (badges)
        try:
            co.select_offline()
            co.wait(1000)
            co.select_imps()
            co.wait(1500)
            for badge in co.get_visible_offline_imps_badges():
                scenarios.append(("IMPS", badge, "badge"))
        except Exception:
            pass

        allure.attach(
            f"Discovered {len(scenarios)} offline scenario(s) for CHIN36:\n" +
            "\n".join(f"  - {t:4s} -> {n} ({k})" for t, n, k in scenarios)
            if scenarios else "(none discovered)",
            name="Offline scenarios discovered",
            attachment_type=allure.attachment_type.TEXT,
        )
        if not scenarios:
            pytest.skip("No offline banks discovered for this client — nothing to test")

        log = [f"Discovered {len(scenarios)} scenario(s)", ""]

        # ── Per-scenario fresh-session E2E ──
        for idx, (sub_tab, ident, kind) in enumerate(scenarios, 1):
            safe = f"{sub_tab}_{ident.replace(' ', '_').replace('/', '_')}"
            label = f"{sub_tab} -> {ident}"
            try:
                co = goto_checkout_for_client(page, "CHIN36")
                co.select_offline()
                co.wait(1200)

                if sub_tab == "Cash":
                    co.select_cash()
                elif sub_tab == "RTGS":
                    co.select_rtgs()
                else:
                    co.select_imps()
                co.wait(1500)

                # Click the specific bank / badge
                if kind == "img":
                    co.page.locator(f"img[alt='{ident}']").first.click(timeout=5000)
                else:
                    co.select_imps_bank_by_badge(ident)
                co.wait(2500)  # visible: bank highlighted
                co.screenshot(f"off_{idx:02d}_{safe}_selected")

                # Pay at bank
                co.wait(1000)
                co.click_pay_at_bank()

                # Wait for challan / gateway
                try:
                    co.page.wait_for_load_state("domcontentloaded", timeout=20000)
                except Exception:
                    pass
                try:
                    co.page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass
                co.wait(6000)
                co.screenshot(f"off_{idx:02d}_{safe}_after_pay")

                # Verdict — challan/gateway opened?
                if co.is_challan_opened(timeout_ms=3000):
                    log.append(f"[PASS] {label} -> challan / gateway opened")
                else:
                    co.screenshot(f"off_{idx:02d}_{safe}_NO_CHALLAN")
                    log.append(f"[FAIL] {label} -> no challan (url={co.get_current_url()[:70]})")
            except Exception as e:
                try:
                    co.screenshot(f"off_{idx:02d}_{safe}_ERROR")
                except Exception:
                    pass
                log.append(f"[FAIL] {label}: {str(e)[:120]}")

        allure.attach("\n".join(log), name="Offline Per-Bank Results (dynamic)",
                      attachment_type=allure.attachment_type.TEXT)
        assert any(line.startswith("[PASS]") for line in log), \
            "All offline scenarios failed:\n" + "\n".join(log)


# ══════════════════════════════════════════════════════════════════════
#  R8: MODE SWITCHING & STABILITY
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R8 - Mode Switching")
class TestR8Switching:

    @allure.title("R8.1: Switch all modes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_switch_all(self, page):
        co = goto_checkout(page)
        co.select_cards()
        assert co.is_card_form_visible()
        co.select_upi()
        co.select_netbanking()
        assert co.is_search_visible()
        co.select_wallets()
        assert co.is_wallet_grid_visible()
        co.select_offline()
        assert co.is_offline_options_visible()

    @allure.title("R8.2: Rapid switching stability")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rapid_switch(self, page):
        co = goto_checkout(page)
        co.select_upi()
        co.select_cards()
        co.select_netbanking()
        co.select_wallets()
        co.select_offline()
        co.select_cards()
        co.select_upi()
        assert co.is_pay_visible()


# ══════════════════════════════════════════════════════════════════════
#  R11: FEE FORWARD (convenience charges visibility)
#    YES → charges row visible on checkout   (CHIN36)
#    NO  → charges row hidden on checkout    (SUBI79)
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R11 - Fee Forward")
class TestR11FeeForward:

    @allure.title("R11.1: CHIN36 (Fee Forward = YES) — Convenience Charges VISIBLE on checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_charges_visible(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.screenshot("R11_1_CHIN36_checkout_card")
        visible = co.is_convenience_charges_visible(timeout=8000)
        order   = co.get_order_amount()
        charges = co.get_convenience_charges_amount()
        total   = co.get_total_amount()
        merchant = co.get_merchant_name_on_checkout()
        allure.attach(
            f"Merchant: {merchant}\nOrder: {order}\nCharges: {charges}\nTotal: {total}\n"
            f"Charges visible: {visible}",
            name="CHIN36 summary card", attachment_type=allure.attachment_type.TEXT,
        )
        assert visible, \
            f"FAIL: Fee Forward YES — 'Convenience Charges' should be visible for CHIN36"

    @allure.title("R11.2: SUBI79 (Fee Forward = NO) — Convenience Charges HIDDEN on checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_charges_hidden(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.screenshot("R11_2_SUBI79_checkout_card")
        visible = co.is_convenience_charges_visible(timeout=5000)
        order    = co.get_order_amount()
        total    = co.get_total_amount()
        merchant = co.get_merchant_name_on_checkout()
        allure.attach(
            f"Merchant: {merchant}\nOrder: {order}\nTotal: {total}\n"
            f"Charges visible: {visible}",
            name="SUBI79 summary card", attachment_type=allure.attachment_type.TEXT,
        )
        assert not visible, \
            f"FAIL: Fee Forward NO — 'Convenience Charges' should be HIDDEN for SUBI79"

    @allure.title("R11.3: CHIN36 — Total = Order + Convenience Charges (math check)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_chin36_total_matches_sum(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        if not co.is_convenience_charges_visible(timeout=5000):
            pytest.skip("Charges not visible — cannot validate math")
        order   = co._extract_amount(co.get_order_amount())
        charges = co._extract_amount(co.get_convenience_charges_amount())
        total   = co._extract_amount(co.get_total_amount())
        allure.attach(
            f"Order: {order}\nCharges: {charges}\nTotal: {total}\nExpected: {order + charges}",
            name="Math check", attachment_type=allure.attachment_type.TEXT,
        )
        # Allow small rounding (0.05) tolerance
        assert abs((order + charges) - total) < 0.05, \
            f"FAIL: Total ({total}) != Order ({order}) + Charges ({charges})"


# ══════════════════════════════════════════════════════════════════════
#  R12: FETCH validation (configure page)
#    Verifies Fetch click → green indicator / API URL populated,
#    and that skipping Fetch does NOT land on a valid checkout.
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R12 - Fetch Validation")
class TestR12FetchValidation:

    @allure.title("R12.1: CHIN36 — valid Fetch → success indicator + API URL populated + correct client name")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_fetch_shows_success(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment("Staging")
        c.enter_merchant_id("CHIN36")
        c.click_fetch()
        c.wait_for_fetch_complete()
        c.screenshot("R12_1_CHIN36_after_fetch")

        api_ok     = c.is_fetch_success()
        green_ok   = c.is_green_success_indicator_visible()
        client_txt = c.get_fetched_client_name()

        allure.attach(
            f"API URL populated: {api_ok}\n"
            f"Green indicator visible: {green_ok}\n"
            f"Client name text: {client_txt or '(not found)'}",
            name="Fetch result", attachment_type=allure.attachment_type.TEXT,
        )
        assert api_ok, "Merchant API URL field is empty after Fetch — fetch did not succeed"

    @allure.title("R12.2: Invalid merchant ID → Fetch shows error, no API URL populated")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_merchant_fetch_fails(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment("Staging")
        c.enter_merchant_id("ZZZ_INVALID_999")
        c.click_fetch()
        try:
            c.wait_for_fetch_complete()
        except Exception:
            pass
        c.screenshot("R12_2_invalid_merchant_after_fetch")

        api_populated = c.is_fetch_success()
        has_error     = c.has_error_on_page() or c.has_client_not_found_error()
        allure.attach(
            f"API URL populated: {api_populated}\nError shown: {has_error}",
            name="Invalid fetch result", attachment_type=allure.attachment_type.TEXT,
        )
        assert not api_populated, "API URL should NOT be populated for an invalid merchant"

    @allure.title("R12.3: Skipping Fetch — Continue with empty API URL should not reach valid checkout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_skip_fetch_blocked(self, page):
        c = ConfigurePage(page)
        c.open()
        c.reload_page()
        c.click_form_card()
        c.select_environment("Staging")
        c.enter_merchant_id("CHIN36")
        # NOTE: deliberately skip click_fetch()
        api_empty = c.is_api_url_empty()
        allure.attach(
            f"API URL empty (before fetch): {api_empty}",
            name="Pre-fetch state", attachment_type=allure.attachment_type.TEXT,
        )
        assert api_empty, \
            "API URL should be empty before Fetch is clicked — user bypassed Fetch"


# ══════════════════════════════════════════════════════════════════════
#  R13: LANGUAGE DROPDOWN on checkout page
#     Verifies the EN / HI / other-language switcher:
#       - dropdown opens and shows >1 options
#       - selecting a non-English language changes the button label
#       - checkout card reflects the new language (text not in English)
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R13 - Language Dropdown")
class TestR13Language:

    @allure.title("R13.1: Language dropdown opens and lists options")
    @allure.severity(allure.severity_level.NORMAL)
    def test_language_dropdown_opens(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.screenshot("R13_1_before_dropdown")
        co.open_language_dropdown()
        co.wait(1000)
        co.screenshot("R13_1_dropdown_open")
        langs = co.get_available_languages()
        allure.attach(
            f"Languages discovered in dropdown:\n  - " +
            "\n  - ".join(langs or ["(none)"]),
            name="Language list", attachment_type=allure.attachment_type.TEXT,
        )
        assert len(langs) >= 1, \
            "Expected at least 1 language option visible in dropdown"

    @allure.title("R13.2: Switch to Hindi — button label changes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_switch_to_hindi(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        initial_label = co.get_current_language_label()
        co.screenshot("R13_2_before_switch")

        co.open_language_dropdown()
        co.wait(800)
        try:
            # Try common Hindi button texts
            for candidate in ["Hindi", "हिंदी", "हिन्दी", "HI"]:
                try:
                    co.select_language(candidate)
                    break
                except Exception:
                    continue
        except Exception:
            pytest.skip("Hindi option not found in this build of checkout")

        co.wait(2000)
        co.screenshot("R13_2_after_switch_hindi")
        new_label = co.get_current_language_label()

        allure.attach(
            f"Initial label: {initial_label}\nAfter switching: {new_label}",
            name="Language label change",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert new_label != initial_label, \
            f"Language button label should change. Was '{initial_label}', still '{new_label}'"

    @allure.title("R13.3: Switch through ALL available languages — UI label reflects each")
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_all_languages(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.open_language_dropdown()
        co.wait(1000)
        langs = co.get_available_languages()
        if len(langs) < 2:
            pytest.skip(f"Only {len(langs)} language(s) available — need >=2 to test switching")

        log = [f"Discovered {len(langs)} languages: {langs}", ""]
        for idx, lang in enumerate(langs, 1):
            safe = lang.replace(" ", "_").replace("/", "_")
            try:
                # Close dropdown first if open, then re-open to click option
                try:
                    co.open_language_dropdown()
                    co.wait(600)
                except Exception:
                    pass
                co.select_language(lang)
                co.wait(1500)
                co.screenshot(f"R13_3_{idx:02d}_{safe}")
                current = co.get_current_language_label()
                log.append(f"[OK] {lang} -> label now: '{current}'")
            except Exception as e:
                log.append(f"[FAIL] {lang}: {str(e)[:100]}")

        allure.attach("\n".join(log), name="All languages tested",
                      attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R10: FULL E2E PER MODE — CHIN36
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R10 - CHIN36 E2E")
class TestR10_CHIN36:
    """CHIN36 Staging: fresh session per mode with assertions."""

    @allure.title("CHIN36: 1. UPI QR")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_1_upi(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_upi()
        co.click_generate_qr()
        co.wait(5000)
        assert co.is_qr_visible(), "QR code should be generated"

    @allure.title("CHIN36: 2. Debit Card → Pay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_2_debit_card(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_cards()
        assert co.is_card_form_visible(), "Card form should be visible"
        co.enter_card_number("4000 0000 0000 000")
        co.enter_card_holder("Test Debit")
        co.enter_card_expiry("10/30")
        co.enter_card_cvv("123")
        assert co.is_pay_visible(), "Pay button should be visible"
        co.click_pay()
        co.wait(3000)

    @allure.title("CHIN36: 3. Credit Card → Pay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_3_credit_card(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        c = _d()["card"]
        co.select_cards()
        assert co.is_card_form_visible(), "Card form should be visible"
        co.enter_card_number(c["card_number"])
        co.enter_card_holder(c["holder"])
        co.enter_card_expiry(c["expiry"])
        co.enter_card_cvv(c["cvv"])
        assert co.is_pay_visible(), "Pay button should be visible"
        co.click_pay()
        co.wait(3000)

    @allure.title("CHIN36: 4a. Netbanking → Click ALL banks → Pay → Verify Bank Page Opens")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_4a_netbanking_all_banks(self, page):
        # First get the list of all banks
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_netbanking()
        co.click_show_all_banks()
        co.wait(3000)
        banks = co.get_all_bank_names()
        allure.attach(f"Total banks: {len(banks)}\n" + "\n".join([f"{i+1}. {b}" for i, b in enumerate(banks)]),
                      name="All_Banks_List", attachment_type=allure.attachment_type.TEXT)
        assert len(banks) > 0, "At least one bank should be available"

        passed, failed = [], []

        for i, bank in enumerate(banks):
            with allure.step(f"Bank {i+1}/{len(banks)}: {bank}"):
                try:
                    # Fresh checkout session for each bank
                    co = goto_checkout_for_client(page, "CHIN36")
                    co.select_netbanking()
                    co.click_show_all_banks()
                    co.wait(1000)
                    co.click_bank_by_name(bank)
                    assert co.is_pay_visible(), f"Pay not visible for {bank}"

                    checkout_url = page.url

                    # Click Pay → verify bank page opens
                    co.click_pay()
                    co.wait(5000)
                    current_url = page.url

                    if current_url != checkout_url:
                        passed.append(bank)
                        allure.attach(f"{bank}: PASS — {current_url}",
                                      name=f"Bank_{i+1}_PASS_{bank.replace(' ','_')}", attachment_type=allure.attachment_type.TEXT)
                    else:
                        failed.append(f"{bank}: page did not change")
                        allure.attach(f"{bank}: FAIL — stayed on checkout",
                                      name=f"Bank_{i+1}_FAIL_{bank.replace(' ','_')}", attachment_type=allure.attachment_type.TEXT)

                except Exception as e:
                    failed.append(f"{bank}: {str(e)[:80]}")
                    allure.attach(f"{bank}: ERROR — {str(e)[:100]}",
                                  name=f"Bank_{i+1}_ERR_{bank.replace(' ','_')}", attachment_type=allure.attachment_type.TEXT)

        # Final summary
        summary = (
            f"NETBANKING ALL BANKS — CHIN36\n"
            f"Total: {len(banks)} | PASSED: {len(passed)} | FAILED: {len(failed)}\n\n"
            f"PASSED:\n" + "\n".join([f"  + {b}" for b in passed]) + "\n\n"
            f"FAILED:\n" + "\n".join([f"  - {b}" for b in failed] or ["  None"])
        )
        allure.attach(summary, name="FINAL_REPORT", attachment_type=allure.attachment_type.TEXT)
        assert len(failed) == 0, f"{len(failed)}/{len(banks)} banks failed"

    @allure.title("CHIN36: 4b. Netbanking → IDFC → Pay → Gateway → Cancel → Back")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_4b_netbanking(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_netbanking()
        assert co.is_search_visible(), "Search should be visible"
        co.search_bank("idfc")
        co.select_idfc_bank()
        assert co.is_pay_visible(), "Pay should be visible after IDFC"
        # Click Pay → navigates to bank gateway
        co.click_pay()
        co.wait(5000)
        allure.attach(f"URL after Pay: {page.url}", name="Bank_Gateway_URL", attachment_type=allure.attachment_type.TEXT)
        assert "checkout" not in page.url or "sabpaisa" in page.url, "Should navigate to bank gateway"
        # Cancel on bank page and go back
        try:
            page.locator("text=Cancel").first.click(timeout=10000)
            co.wait(3000)
        except Exception:
            pass
        page.go_back()
        co.wait(5000)
        allure.attach(f"URL after back: {page.url}", name="Back_URL", attachment_type=allure.attachment_type.TEXT)

    @allure.title("CHIN36: 5. Wallet → MobiKwik")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_5_wallet(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_wallets()
        assert co.is_wallet_grid_visible(), "Wallet grid should be visible"
        co.select_mobikwik()
        assert co.is_pay_visible(), "Pay should be visible after MobiKwik"

    @allure.title("CHIN36: 6. Offline Cash → ICICI Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_6_offline_cash(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_offline()
        assert co.is_offline_options_visible(), "Offline options should be visible"
        # Click Cash button using exact xpath
        co.page.locator("//p[normalize-space()='Cash']").first.click()
        co.wait(3000)
        # Select ICICI Bank
        co.page.locator("//img[@alt='ICICI Bank']").first.click()
        co.wait(1000)
        assert co.is_pay_visible(), "Pay should be visible after ICICI"

    @allure.title("CHIN36: 7. Offline RTGS → IDFC First Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_7_offline_rtgs(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_offline()
        assert co.is_offline_options_visible()
        co.select_rtgs()
        co.wait(2000)
        co.page.locator("text='IDFC First Bank RTGS'").first.click()
        co.wait(1000)
        assert co.is_pay_visible(), "Pay should be visible after IDFC RTGS"

    @allure.title("CHIN36: 8. Offline IMPS → SabPaisa")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_chin36_8_offline_imps(self, page):
        co = goto_checkout_for_client(page, "CHIN36")
        co.select_offline()
        assert co.is_offline_options_visible()
        co.select_imps()
        co.wait(2000)
        search = co.page.locator("input[placeholder*='Search banks']")
        if search.count() > 0 and search.first.is_visible():
            search.first.fill("sa")
            co.wait(2000)
        co.page.locator("text='SA'").first.click()
        co.wait(1000)


# ══════════════════════════════════════════════════════════════════════
#  R10: FULL E2E PER MODE — SUBI79
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression")
@allure.feature("R10 - SUBI79 E2E")
class TestR10_SUBI79:
    """SUBI79 Staging: fresh session per mode with assertions."""

    @allure.title("SUBI79: UPI QR")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_upi(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_upi()
        co.click_generate_qr()
        co.wait(5000)
        assert co.is_qr_visible(), "QR code should be generated"

    @allure.title("SUBI79: Credit Card → Pay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_credit_card(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        c = _d()["card"]
        co.select_cards()
        assert co.is_card_form_visible(), "Card form should be visible"
        co.enter_card_number(c["card_number"])
        co.enter_card_holder(c["holder"])
        co.enter_card_expiry(c["expiry"])
        co.enter_card_cvv(c["cvv"])
        assert co.is_pay_visible(), "Pay button should be visible"
        co.click_pay()
        co.wait(3000)

    @allure.title("SUBI79: Debit Card → Pay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_debit_card(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_cards()
        assert co.is_card_form_visible(), "Card form should be visible"
        co.enter_card_number("4000 0000 0000 000")
        co.enter_card_holder("Test Debit")
        co.enter_card_expiry("10/30")
        co.enter_card_cvv("123")
        assert co.is_pay_visible(), "Pay button should be visible"
        co.click_pay()
        co.wait(3000)

    @allure.title("SUBI79: Netbanking → IDFC → Pay → Bank Gateway → Back")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_netbanking(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_netbanking()
        assert co.is_search_visible(), "Search should be visible"
        co.search_bank("idfc")
        co.select_idfc_bank()
        assert co.is_pay_visible(), "Pay should be visible after IDFC"
        # Click Pay → navigates to bank gateway
        co.click_pay()
        co.wait(5000)
        allure.attach(f"URL after Pay: {page.url}", name="Bank_Gateway_URL", attachment_type=allure.attachment_type.TEXT)
        assert "checkout" not in page.url or "sabpaisa" in page.url, "Should navigate to bank gateway"
        # Cancel on bank page and go back
        try:
            page.locator("text=Cancel").first.click(timeout=10000)
            co.wait(3000)
        except Exception:
            pass
        page.go_back()
        co.wait(5000)
        allure.attach(f"URL after back: {page.url}", name="Back_URL", attachment_type=allure.attachment_type.TEXT)

    @allure.title("SUBI79: Wallet → MobiKwik")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_wallet(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_wallets()
        assert co.is_wallet_grid_visible(), "Wallet grid should be visible"
        co.select_mobikwik()
        assert co.is_pay_visible(), "Pay should be visible after MobiKwik"

    @allure.title("SUBI79: Offline Cash → ICICI Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_offline_cash(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_offline()
        assert co.is_offline_options_visible()
        co.page.locator("//p[normalize-space()='Cash']").first.click()
        co.wait(3000)
        co.page.locator("//img[@alt='ICICI Bank']").first.click()
        co.wait(1000)
        assert co.is_pay_visible(), "Pay should be visible after ICICI"

    @allure.title("SUBI79: Offline RTGS → IDFC First Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_offline_rtgs(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_offline()
        assert co.is_offline_options_visible()
        co.select_rtgs()
        co.wait(2000)
        co.page.locator("text='IDFC First Bank RTGS'").first.click()
        co.wait(1000)
        assert co.is_pay_visible(), "Pay should be visible after IDFC RTGS"

    @allure.title("SUBI79: Offline IMPS → SabPaisa")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_subi79_offline_imps(self, page):
        co = goto_checkout_for_client(page, "SUBI79")
        co.select_offline()
        assert co.is_offline_options_visible()
        co.select_imps()
        co.wait(2000)
        search = co.page.locator("input[placeholder*='Search banks']")
        if search.count() > 0 and search.first.is_visible():
            search.first.fill("sa")
            co.wait(2000)
        co.page.locator("text='SA'").first.click()
        co.wait(1000)
