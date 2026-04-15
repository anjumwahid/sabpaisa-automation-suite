"""CheckoutPage — All payment methods on staging checkout screen."""

import allure
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # ══════════════════════════════════════════════
    #  LOCATORS — Payment Mode Buttons
    # ══════════════════════════════════════════════

    BTN_UPI = {
        "xpath": "//button[.//p[contains(text(),'UPI')]]",
        "text": "UPI",
    }

    BTN_CARDS = {
        "xpath": "//button[.//p[contains(text(),'Cards')]]",
        "text": "Cards",
    }

    BTN_NETBANKING = {
        "xpath": "//button[.//p[contains(text(),'Netbanking')]]",
        "text": "Netbanking",
    }

    BTN_WALLETS = {
        "xpath": "//button[.//p[contains(text(),'Wallet')]]",
        "text": "Wallet",
    }

    BTN_OFFLINE = {
        "xpath": "//button[.//p[contains(text(),'Offline')]]",
        "text": "Offline Payment",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — UPI / QR
    # ══════════════════════════════════════════════

    TAB_SCAN_QR = {"text": "Scan QR"}
    TAB_UPI_ID = {"text": "UPI ID"}
    BTN_GENERATE_QR = {"text": "Generate QR"}

    # ══════════════════════════════════════════════
    #  LOCATORS — Card Form (secure-card-*)
    # ══════════════════════════════════════════════

    INPUT_CARD_NUMBER = {
        "xpath": "//input[@id='secure-card-number']",
        "css": "input#secure-card-number",
    }

    INPUT_CARD_HOLDER = {
        "xpath": "//input[@id='secure-card-name']",
        "css": "input#secure-card-name",
    }

    INPUT_CARD_EXPIRY = {
        "xpath": "//input[@id='secure-card-expiry']",
        "css": "input#secure-card-expiry",
    }

    INPUT_CARD_CVV = {
        "xpath": "//input[@id='secure-card-cvv']",
        "css": "input#secure-card-cvv",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Netbanking
    # ══════════════════════════════════════════════

    INPUT_SEARCH_BANK = {
        "xpath": "//input[contains(@placeholder,'Search banks')]",
        "css": "input[placeholder*='Search banks']",
    }

    IMG_EQUITAS_BANK = {
        "xpath": "//img[@alt='Equitas Bank']",
        "css": "img[alt='Equitas Bank']",
    }

    BTN_SHOW_ALL_BANKS = {"text": "Show all banks"}

    # ══════════════════════════════════════════════
    #  LOCATORS — Wallets
    # ══════════════════════════════════════════════

    IMG_PHONEPE = {
        "xpath": "//img[@alt='Phonepe']",
        "css": "img[alt='Phonepe']",
    }

    IMG_AMAZONPAY = {
        "xpath": "//img[@alt='AMAZONPAY']",
        "css": "img[alt='AMAZONPAY']",
    }

    IMG_MOBIKWIK = {
        "xpath": "//img[@alt='MOBIKWIK']",
        "css": "img[alt='MOBIKWIK']",
    }

    IMG_AIRTEL_MONEY = {
        "xpath": "//img[@alt='Airtel money']",
        "css": "img[alt='Airtel money']",
    }

    IMG_FREECHARGE = {
        "xpath": "//img[contains(@alt,'FreeCharge') or contains(@alt,'FR')]",
        "css": "img[alt*='reeCharge']",
    }

    IMG_JIO = {
        "xpath": "//img[contains(@alt,'Jio')]",
        "css": "img[alt*='Jio']",
    }

    IMG_OLA_MONEY = {
        "xpath": "//img[contains(@alt,'OLA')]",
        "css": "img[alt*='OLA']",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Offline Payment
    # ══════════════════════════════════════════════

    BTN_CASH = {
        "xpath": "//p[normalize-space()='Cash']",
        "text": "Cash",
    }

    IMG_BANK_OF_INDIA = {
        "xpath": "//img[contains(@alt,'Bank Of India')]",
        "css": "img[alt*='Bank Of India']",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Common
    # ══════════════════════════════════════════════

    BTN_PAY = {"text": "Pay"}

    # ══════════════════════════════════════════════
    #  ACTIONS — Common
    # ══════════════════════════════════════════════

    @allure.step("Wait for checkout page to load")
    def wait_for_checkout_load(self):
        self.page.wait_for_load_state("networkidle", timeout=30000)
        self.wait(5000)

    def _click_pay_mode(self, text: str):
        self.page.locator("button", has_text=text).first.click()

    # ══════════════════════════════════════════════
    #  ACTIONS — Payment Mode Selection
    # ══════════════════════════════════════════════

    @allure.step("Select UPI payment")
    def select_upi(self):
        self._click_pay_mode("UPI")
        self.wait(2000)

    @allure.step("Select Cards payment")
    def select_cards(self):
        self._click_pay_mode("Cards")
        self.wait(2000)

    @allure.step("Select Netbanking payment")
    def select_netbanking(self):
        self._click_pay_mode("Netbanking")
        self.wait(3000)

    @allure.step("Select Wallets payment")
    def select_wallets(self):
        self._click_pay_mode("Wallet")
        self.wait(2000)

    @allure.step("Select Offline Payment")
    def select_offline(self):
        self._click_pay_mode("Offline Payment")
        self.wait(2000)

    # ══════════════════════════════════════════════
    #  ACTIONS — UPI / QR
    # ══════════════════════════════════════════════

    @allure.step("Click Scan QR tab")
    def click_scan_qr(self):
        self.page.locator("button", has_text="Scan QR").first.click()
        self.wait(2000)

    @allure.step("Click Generate QR")
    def click_generate_qr(self):
        self.page.locator("button", has_text="Generate QR").first.click()
        self.wait(3000)

    # ══════════════════════════════════════════════
    #  ACTIONS — Cards
    # ══════════════════════════════════════════════

    @allure.step("Enter Card Number: {value}")
    def enter_card_number(self, value: str):
        self.engine.fill(self.INPUT_CARD_NUMBER, value, timeout=10000)

    @allure.step("Enter Cardholder Name: {value}")
    def enter_card_holder(self, value: str):
        self.engine.fill(self.INPUT_CARD_HOLDER, value, timeout=10000)

    @allure.step("Enter Expiry: {value}")
    def enter_card_expiry(self, value: str):
        self.engine.fill(self.INPUT_CARD_EXPIRY, value, timeout=10000)

    @allure.step("Enter CVV: {value}")
    def enter_card_cvv(self, value: str):
        self.engine.fill(self.INPUT_CARD_CVV, value, timeout=10000)

    @allure.step("Click Pay button")
    def click_pay(self):
        self.page.locator("button", has_text="Pay").first.click()
        self.wait(3000)

    # ══════════════════════════════════════════════
    #  ACTIONS — Netbanking
    # ══════════════════════════════════════════════

    @allure.step("Search bank: {query}")
    def search_bank(self, query: str):
        self.engine.fill(self.INPUT_SEARCH_BANK, query, timeout=20000)
        self.wait(2000)

    @allure.step("Select Equitas Bank")
    def select_equitas_bank(self):
        self.engine.click(self.IMG_EQUITAS_BANK, timeout=20000)

    @allure.step("Click Show all banks")
    def click_show_all_banks(self):
        self.page.locator("button", has_text="Show all banks").first.click()
        self.wait(2000)

    # ══════════════════════════════════════════════
    #  ACTIONS — Wallets
    # ══════════════════════════════════════════════

    @allure.step("Select PhonePe wallet")
    def select_phonepe(self):
        self.engine.click(self.IMG_PHONEPE, timeout=10000)
        self.wait(1000)

    @allure.step("Select AmazonPay wallet")
    def select_amazonpay(self):
        self.engine.click(self.IMG_AMAZONPAY, timeout=10000)
        self.wait(1000)

    @allure.step("Select MobiKwik wallet")
    def select_mobikwik(self):
        self.engine.click(self.IMG_MOBIKWIK, timeout=10000)
        self.wait(1000)

    @allure.step("Select Airtel Money wallet")
    def select_airtel_money(self):
        self.engine.click(self.IMG_AIRTEL_MONEY, timeout=10000)
        self.wait(1000)

    @allure.step("Select FreeCharge wallet")
    def select_freecharge(self):
        self.engine.click(self.IMG_FREECHARGE, timeout=10000)
        self.wait(1000)

    @allure.step("Select Jio wallet")
    def select_jio(self):
        self.engine.click(self.IMG_JIO, timeout=10000)
        self.wait(1000)

    @allure.step("Select OLA Money wallet")
    def select_ola_money(self):
        self.engine.click(self.IMG_OLA_MONEY, timeout=10000)
        self.wait(1000)

    # ══════════════════════════════════════════════
    #  ACTIONS — Offline Payment
    # ══════════════════════════════════════════════

    @allure.step("Select Cash option")
    def select_cash(self):
        self.page.locator("button", has_text="Cash").first.click()
        self.wait(1000)

    @allure.step("Select Bank Of India")
    def select_bank_of_india(self):
        self.engine.click(self.IMG_BANK_OF_INDIA, timeout=10000)
        self.wait(1000)

    # ══════════════════════════════════════════════
    #  ACTIONS — Page
    # ══════════════════════════════════════════════

    @allure.step("Final reload")
    def reload_page(self):
        self.reload()

    # ══════════════════════════════════════════════
    #  VALIDATION HELPERS
    # ══════════════════════════════════════════════

    @allure.step("Check if bank search shows no results")
    def is_no_bank_found(self) -> bool:
        try:
            self.page.locator("text=No banks found").first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return self.page.locator("img[alt*='Bank']").count() == 0

    @allure.step("Check if search input is visible")
    def is_search_visible(self) -> bool:
        return self.engine.is_visible(self.INPUT_SEARCH_BANK, timeout=5000)

    @allure.step("Check if QR code is visible")
    def is_qr_visible(self) -> bool:
        try:
            self.page.locator("canvas, img[alt*='QR'], svg[class*='qr'], [class*='qr']").first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    @allure.step("Check if card form is visible")
    def is_card_form_visible(self) -> bool:
        return self.engine.is_visible(self.INPUT_CARD_NUMBER, timeout=5000)

    @allure.step("Check if Pay button is visible")
    def is_pay_visible(self) -> bool:
        try:
            self.page.locator("button", has_text="Pay").first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Check if wallet grid is visible")
    def is_wallet_grid_visible(self) -> bool:
        try:
            self.page.locator("img[alt='Phonepe'], img[alt='AMAZONPAY']").first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Check if offline options visible")
    def is_offline_options_visible(self) -> bool:
        try:
            self.page.get_by_text("Cash").first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Get current page URL")
    def get_current_url(self) -> str:
        return self.page.url

    @allure.step("Get all bank names from Netbanking")
    def get_all_bank_names(self) -> list:
        """Returns list of all bank alt texts visible in Netbanking section."""
        bank_imgs = self.page.locator("img[alt*='Bank'], img[alt*='bank']").all()
        names = []
        for img in bank_imgs:
            try:
                alt = img.get_attribute("alt")
                if alt:
                    names.append(alt)
            except Exception:
                pass
        return names

    @allure.step("Click bank by name: {bank_name}")
    def click_bank_by_name(self, bank_name: str):
        """Click a bank image by its alt text."""
        self.page.locator(f"img[alt='{bank_name}']").first.click()
        self.wait(1000)

    @allure.step("Get all wallet names")
    def get_all_wallet_names(self) -> list:
        """Returns list of all wallet alt texts."""
        wallet_imgs = self.page.locator(
            "img[alt='Phonepe'], img[alt='AMAZONPAY'], img[alt='MOBIKWIK'], "
            "img[alt='Airtel money'], img[alt*='reeCharge'], img[alt*='Jio'], img[alt*='OLA']"
        ).all()
        names = []
        for img in wallet_imgs:
            try:
                alt = img.get_attribute("alt")
                if alt:
                    names.append(alt)
            except Exception:
                pass
        return names

    # ══════════════════════════════════════════════
    #  COMPOSED WORKFLOWS
    # ══════════════════════════════════════════════

    @allure.step("Complete UPI QR flow")
    def complete_upi_qr_flow(self):
        self.wait_for_checkout_load()
        self.select_upi()
        self.click_scan_qr()
        self.click_generate_qr()

    @allure.step("Complete Cards flow")
    def complete_cards_flow(self, number, holder, expiry, cvv):
        self.wait_for_checkout_load()
        self.select_cards()
        self.enter_card_number(number)
        self.enter_card_holder(holder)
        self.enter_card_expiry(expiry)
        self.enter_card_cvv(cvv)

    @allure.step("Complete Netbanking flow")
    def complete_netbanking_flow(self, bank_search="eq"):
        self.wait_for_checkout_load()
        self.select_netbanking()
        self.search_bank(bank_search)
        self.select_equitas_bank()

    @allure.step("Complete Wallet flow - PhonePe")
    def complete_wallet_phonepe_flow(self):
        self.wait_for_checkout_load()
        self.select_wallets()
        self.select_phonepe()

    @allure.step("Complete Offline Cash flow")
    def complete_offline_cash_flow(self):
        self.wait_for_checkout_load()
        self.select_offline()
        self.select_cash()

    @allure.step("Complete Offline Bank Transfer flow")
    def complete_offline_bank_flow(self):
        self.wait_for_checkout_load()
        self.select_offline()
        self.select_bank_of_india()
