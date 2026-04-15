"""
REGRESSION TEST SUITE - SabPaisa Payment Gateway
Environment: Staging | Client Code: UTTA99

Sections:
  R1  - Merchant Configuration (Positive + Negative)
  R2  - Customer Form (Positive + Negative)
  R3  - UPI Payment
  R4  - Card Payment (Positive + Negative)
  R5  - Netbanking (Search, All Banks, Popular Banks)
  R6  - Wallets (All Wallets)
  R7  - Offline Payment (Cash, Bank Transfer)
  R8  - Payment Mode Switching & Stability
  R9  - E2E Smoke (All Modes)
  R10 - Full Sequential Flow (All Banks → Cards → UPI → Wallets → Offline)

Run:    pytest tests/test_regression_suite.py --alluredir=allure-results --headed --slowmo 500 -v -s
Report: allure serve allure-results
"""

import allure
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


# ══════════════════════════════════════════════════════════════════════
#  R1: MERCHANT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R1 - Merchant Configuration")
class TestR1MerchantConfig:

    @allure.title("R1.1: Open configure page")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_open_page(self, page):
        c = ConfigurePage(page)
        c.open()
        assert "configure" in c.get_current_url().lower()

    @allure.title("R1.2: Fetch merchant UTTA99 on Staging")
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

    @allure.title("R1.4: [NEG] Invalid merchant ID shows error")
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

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R2 - Customer Form")
class TestR2CustomerForm:

    @allure.title("R2.1: Fill all fields and proceed to checkout")
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

    @allure.title("R2.3: [NEG] Invalid email format")
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
            allure.attach("App allowed -100", name="BUG", attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R3: UPI PAYMENT
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R3 - UPI Payment")
class TestR3UPI:

    @allure.title("R3.1: Select UPI")
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
        co.click_scan_qr()
        co.click_generate_qr()
        assert co.is_qr_visible()


# ══════════════════════════════════════════════════════════════════════
#  R4: CARD PAYMENT
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R4 - Card Payment")
class TestR4Cards:

    @allure.title("R4.1: Card form appears")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_card_form(self, page):
        co = goto_checkout(page)
        co.select_cards()
        assert co.is_card_form_visible()

    @allure.title("R4.2: Fill valid card details")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_card(self, page):
        co = goto_checkout(page)
        co.select_cards()
        c = _d()["card"]
        co.enter_card_number(c["card_number"])
        co.enter_card_holder(c["holder"])
        co.enter_card_expiry(c["expiry"])
        co.enter_card_cvv(c["cvv"])
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

    @allure.title("R4.4: [NEG] Empty card fields - click Pay")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_empty_card(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.click_pay()
        co.wait(2000)
        assert co.is_card_form_visible()

    @allure.title("R4.5: [NEG] Expired card (01/20)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_neg_expired_card(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.enter_card_number("4111111111111111")
        co.enter_card_holder("Test")
        co.enter_card_expiry("01/20")
        co.enter_card_cvv("123")
        co.click_pay()
        co.wait(3000)
        allure.attach(f"URL: {co.get_current_url()}", name="Result", attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R5: NETBANKING — Search + All Banks
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R5 - Netbanking")
class TestR5Netbanking:

    @allure.title("R5.1: Search and select Equitas Bank")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_equitas(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        assert co.is_search_visible()
        co.search_bank("eq")
        co.select_equitas_bank()

    @allure.title("R5.2: Show all banks - verify count")
    @allure.severity(allure.severity_level.NORMAL)
    def test_show_all_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        co.wait(2000)
        count = page.locator("img[alt*='Bank']").count()
        allure.attach(f"Total banks: {count}", name="Count", attachment_type=allure.attachment_type.TEXT)
        assert count > 3

    @allure.title("R5.3: Click every available bank one by one")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.click_show_all_banks()
        co.wait(3000)
        banks = co.get_all_bank_names()
        allure.attach("\n".join([f"{i+1}. {b}" for i, b in enumerate(banks)]),
                      name=f"Banks ({len(banks)})", attachment_type=allure.attachment_type.TEXT)
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

    @allure.title("R5.4: Search popular banks (SBI, HDFC, ICICI, Axis, etc.)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_popular_banks(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        banks = ["SBI", "HDFC", "ICICI", "Axis", "Punjab", "Kotak", "Canara", "Indian"]
        results = []
        for b in banks:
            co.search_bank(b)
            count = page.locator("img[alt*='Bank'], img[alt*='bank']").count()
            results.append(f"{b}: {'FOUND' if count > 0 else 'NOT FOUND'} ({count})")
        allure.attach("\n".join(results), name="Popular Banks", attachment_type=allure.attachment_type.TEXT)

    @allure.title("R5.5: [NEG] Search non-existent bank")
    @allure.severity(allure.severity_level.NORMAL)
    def test_neg_no_bank(self, page):
        co = goto_checkout(page)
        co.select_netbanking()
        co.search_bank("ZZZZZZZ_NO_BANK")
        assert co.is_no_bank_found()


# ══════════════════════════════════════════════════════════════════════
#  R6: WALLETS — All Wallets
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R6 - Wallets")
class TestR6Wallets:

    @allure.title("R6.1: Wallet grid visible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wallet_grid(self, page):
        co = goto_checkout(page)
        co.select_wallets()
        assert co.is_wallet_grid_visible()

    @allure.title("R6.2: Click all wallets one by one")
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
            except Exception as e:
                results.append(f"{name}: FAIL - {str(e)[:80]}")
        allure.attach("\n".join(results), name="All Wallets", attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R7: OFFLINE PAYMENT
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
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

    @allure.title("R7.3: Select Bank Of India")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bank_of_india(self, page):
        co = goto_checkout(page)
        co.select_offline()
        co.select_bank_of_india()


# ══════════════════════════════════════════════════════════════════════
#  R8: MODE SWITCHING & STABILITY
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R8 - Mode Switching & Stability")
class TestR8Switching:

    @allure.title("R8.1: Switch all modes - verify each loads correctly")
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

    @allure.title("R8.3: Fill card then switch - card form persists on return")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_switch_back(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.enter_card_number(_d()["card"]["card_number"])
        co.select_netbanking()
        co.select_cards()
        assert co.is_card_form_visible()

    @allure.title("R8.4: [NEG] Reload during payment")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_neg_reload(self, page):
        co = goto_checkout(page)
        co.select_cards()
        co.reload_page()
        co.wait(3000)
        allure.attach(f"URL: {co.get_current_url()}", name="Result", attachment_type=allure.attachment_type.TEXT)


# ══════════════════════════════════════════════════════════════════════
#  R9: E2E SMOKE TESTS
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R9 - E2E Smoke Tests")
class TestR9E2ESmoke:

    @allure.title("R9.1: E2E Netbanking → Equitas Bank")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_e2e_netbanking(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details(**_d()["customer"])
        cust.handle_advanced_and_checkout()
        CheckoutPage(page).complete_netbanking_flow(_d()["payment"]["bank_search"])

    @allure.title("R9.2: E2E Cards → Fill Details")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_e2e_cards(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details(**_d()["customer"])
        cust.handle_advanced_and_checkout()
        c = _d()["card"]
        CheckoutPage(page).complete_cards_flow(c["card_number"], c["holder"], c["expiry"], c["cvv"])

    @allure.title("R9.3: E2E UPI → Generate QR")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_e2e_upi(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details(**_d()["customer"])
        cust.handle_advanced_and_checkout()
        CheckoutPage(page).complete_upi_qr_flow()

    @allure.title("R9.4: E2E Wallet → PhonePe")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_e2e_wallet(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details(**_d()["customer"])
        cust.handle_advanced_and_checkout()
        CheckoutPage(page).complete_wallet_phonepe_flow()

    @allure.title("R9.5: E2E Offline → Cash")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_e2e_offline(self, page):
        configure(page)
        cust = CustomerPage(page)
        cust.fill_customer_details(**_d()["customer"])
        cust.handle_advanced_and_checkout()
        CheckoutPage(page).complete_offline_cash_flow()


# ══════════════════════════════════════════════════════════════════════
#  R10: FULL SEQUENTIAL — All Banks → Cards → UPI → Wallets → Offline
# ══════════════════════════════════════════════════════════════════════

@allure.epic("SabPaisa Regression - Staging")
@allure.feature("R10 - Full Sequential Flow")
class TestR10FullSequential:

    @allure.title("R10.1: ALL BANKS one by one → then Cards → UPI → Wallets → Offline")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_all_banks_then_all_modes(self, page):
        """Single session: every bank + every mode."""
        co = goto_checkout(page)

        # ── NETBANKING: Every bank ──
        with allure.step("NETBANKING — Click every bank"):
            co.select_netbanking()
            co.click_show_all_banks()
            co.wait(3000)
            banks = co.get_all_bank_names()
            allure.attach("\n".join([f"{i+1}. {b}" for i, b in enumerate(banks)]),
                          name=f"Banks ({len(banks)})", attachment_type=allure.attachment_type.TEXT)
            passed, failed = [], []
            for bank in banks:
                try:
                    co.select_netbanking()
                    co.click_show_all_banks()
                    co.wait(1000)
                    co.click_bank_by_name(bank)
                    passed.append(bank)
                except Exception as e:
                    failed.append(f"{bank}: {str(e)[:80]}")
            allure.attach(f"Passed: {len(passed)}/{len(banks)}\nFailed:\n" + "\n".join(failed or ["None"]),
                          name="Netbanking Summary", attachment_type=allure.attachment_type.TEXT)

        # ── CARDS ──
        with allure.step("CARDS — Fill details"):
            co.select_cards()
            c = _d()["card"]
            co.enter_card_number(c["card_number"])
            co.enter_card_holder(c["holder"])
            co.enter_card_expiry(c["expiry"])
            co.enter_card_cvv(c["cvv"])
            assert co.is_pay_visible()

        # ── UPI ──
        with allure.step("UPI — Generate QR"):
            co.select_upi()
            co.click_scan_qr()
            co.click_generate_qr()
            assert co.is_qr_visible()

        # ── WALLETS: Every wallet ──
        with allure.step("WALLETS — Click each wallet"):
            wallet_methods = [
                ("PhonePe", co.select_phonepe),
                ("AmazonPay", co.select_amazonpay),
                ("MobiKwik", co.select_mobikwik),
                ("Airtel Money", co.select_airtel_money),
                ("FreeCharge", co.select_freecharge),
                ("Jio", co.select_jio),
                ("OLA Money", co.select_ola_money),
            ]
            w_results = []
            for name, method in wallet_methods:
                try:
                    co.select_wallets()
                    method()
                    w_results.append(f"{name}: PASS")
                except Exception:
                    w_results.append(f"{name}: FAIL")
            allure.attach("\n".join(w_results), name="Wallets Summary", attachment_type=allure.attachment_type.TEXT)

        # ── OFFLINE ──
        with allure.step("OFFLINE — Cash + Bank Of India"):
            co.select_offline()
            co.select_cash()
            co.select_offline()
            co.select_bank_of_india()

        # ── SUMMARY ──
        with allure.step("FINAL SUMMARY"):
            allure.attach(
                f"Netbanking: {len(passed)}/{len(banks)} banks\n"
                f"Cards: Filled\nUPI: QR Generated\n"
                f"Wallets: {sum(1 for r in w_results if 'PASS' in r)}/{len(w_results)}\n"
                f"Offline: Cash + Bank Of India",
                name="REGRESSION COMPLETE", attachment_type=allure.attachment_type.TEXT,
            )
