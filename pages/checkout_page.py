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

    BTN_GENERATE_QR = {
        "xpath": "//button[normalize-space()='Generate QR']",
        "text": "Generate QR",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Card Form
    # ══════════════════════════════════════════════

    INPUT_CARD_NUMBER = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//input[@id='secure-card-number']",
        "css": "input#secure-card-number",
    }

    INPUT_CARD_HOLDER = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//input[@id='secure-card-name']",
        "css": "input#secure-card-name",
    }

    INPUT_CARD_EXPIRY = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//input[@id='secure-card-expiry']",
        "css": "input#secure-card-expiry",
    }

    INPUT_CARD_CVV = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//input[@id='secure-card-cvv']",
        "css": "input#secure-card-cvv",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Netbanking
    # ══════════════════════════════════════════════

    INPUT_SEARCH_BANK = {
        "xpath": "//input[contains(@placeholder,'Search banks')]",
        "css": "input[placeholder*='Search banks']",
    }

    # -- Popular banks (image grid) --
    IMG_KARUR_VYSYA = {
        "xpath": "//img[@alt='Karur Vysya Bank']",
        "css": "img[alt='Karur Vysya Bank']",
    }

    IMG_BOB_CORPORATE = {
        "xpath": "//img[@alt='Bank of Baroda Net Banking Corporate']",
        "css": "img[alt='Bank of Baroda Net Banking Corporate']",
    }

    IMG_BOB_RETAIL = {
        "xpath": "//img[@alt='Bank of Baroda Net Banking Retail']",
        "css": "img[alt='Bank of Baroda Net Banking Retail']",
    }

    IMG_EQUITAS_BANK = {
        "xpath": "//img[@alt='Equitas Bank']",
        "css": "img[alt='Equitas Bank']",
    }

    IMG_INDIAN_OVERSEAS = {
        "xpath": "//img[@alt='Indian Overseas Bank']",
        "css": "img[alt='Indian Overseas Bank']",
    }

    IMG_SBI = {
        "xpath": "//img[@alt='State Bank of India']",
        "css": "img[alt='State Bank of India']",
    }

    IMG_IDFC_BANK = {
        "xpath": "//img[@alt='IDFC FIRST Bank Limited']",
        "css": "img[alt*='IDFC']",
    }

    # -- Show/Hide all banks toggle --
    BTN_SHOW_ALL_BANKS = {
        "xpath": "//button[normalize-space()='Show all banks']",
        "text": "Show all banks",
    }

    BTN_HIDE_ALL_BANKS = {
        "xpath": "//button[normalize-space()='Hide all banks']",
        "text": "Hide all banks",
    }

    # -- Bank gateway "Cancel" dialog --
    BTN_CANCEL = {
        "xpath": "//h4[normalize-space()='Cancel']",
        "css": "h4:has-text('Cancel')",
        "text": "Cancel",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Wallets
    # ══════════════════════════════════════════════

    IMG_PHONEPE = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//img[@alt='Phonepe']",
        "css": "img[alt='Phonepe']",
    }

    IMG_AMAZONPAY = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//img[@alt='AMAZONPAY']",
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
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//p[@class='text-sm font-bold leading-tight text-emerald-800'][normalize-space()='Cash']",
        "text": "Cash",
    }

    BTN_RTGS = {
        "xpath": "//p[normalize-space()='RTGS']",
        "text": "RTGS",
    }

    BTN_IMPS = {
        "xpath": "//p[normalize-space()='IMPS']",
        "text": "IMPS",
    }

    IMG_BANK_OF_INDIA = {
        "xpath": "//div[@class='flex-1 p-4 overflow-y-auto']//div//img[contains(@alt,'Bank Of India')]",
        "css": "img[alt*='Bank Of India']",
    }

    IMG_BANK_OF_INDIA_RETAIL = {
        "xpath": "//img[@alt='Bank of India Retail']",
        "css": "img[alt='Bank of India Retail']",
    }

    IMG_AIRTEL_BANK = {
        "xpath": "//img[@alt='Airtel Bank']",
        "css": "img[alt='Airtel Bank']",
    }

    IMG_FINO_BANK = {
        "xpath": "//img[contains(@alt,'Fino') or contains(@alt,'FINO')]",
        "css": "img[alt*='ino']",
        "text": "FINO",
    }

    IMG_ICICI_BANK = {
        "xpath": "//img[contains(@alt,'ICICI')]",
        "css": "img[alt*='ICICI']",
        "text": "ICICI Bank",
    }

    IMG_IDFC_FIRST_RTGS = {
        "xpath": "//img[@alt='IDFC First Bank RTGS']",
        "css": "img[alt='IDFC First Bank RTGS']",
    }

    # "Pay at bank" — shown on offline payment confirmation
    BTN_PAY_AT_BANK = {
        "xpath": "//button[.//p[normalize-space()='Pay at bank']]",
        "css": "button:has(p:text-is('Pay at bank'))",
        "text": "Pay at bank",
    }

    # ══════════════════════════════════════════════
    #  LOCATORS — Pay / Proceed Button + Amount
    # ══════════════════════════════════════════════

    BTN_PAY_PROCEED = {
        "xpath": "//button[@class='w-full py-4 rounded-lg font-bold text-base flex items-center justify-center gap-2 transition-all active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-400 focus-visible:ring-offset-2']",
        "text": "Pay",
    }

    SPAN_AMOUNT = {
        "xpath": "//span[@class='tabular-nums']",
        "css": "span.tabular-nums",
    }

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

    @allure.step("Click Generate QR")
    def click_generate_qr(self):
        self.engine.click(self.BTN_GENERATE_QR, timeout=10000)
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

    # ══════════════════════════════════════════════
    #  ACTIONS — Pay / Proceed Button
    # ══════════════════════════════════════════════

    @allure.step("Click Pay button")
    def click_pay(self):
        self.engine.click(self.BTN_PAY_PROCEED, timeout=10000)
        self.wait(3000)

    @allure.step("Get payment amount from Pay button")
    def get_pay_amount(self) -> str:
        return self.engine.get_text(self.SPAN_AMOUNT, timeout=5000)

    # ══════════════════════════════════════════════
    #  Fee Forward / Summary Card validation
    #  (Checkout card: merchant name, SabPaisa Trusted badge,
    #   Order Amount, Convenience Charges, Total Amount)
    # ══════════════════════════════════════════════

    @allure.step("Check if 'Convenience Charges' row is visible (Fee Forward = YES)")
    def is_convenience_charges_visible(self, timeout: int = 5000) -> bool:
        try:
            self.page.get_by_text("Convenience Charges").first.wait_for(
                state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def _read_amount_for_label(self, label: str) -> str:
        """Robust label→amount extractor for the checkout summary card.

        Different rows on the SabPaisa card use different DOM structures:
          - Order Amount / Convenience Charges:  label + amount are siblings
            inside the same parent → 1 level up gets the row text.
          - Total Amount: label and amount are in DIFFERENT sibling divs
            inside a wrapper → may need 2-3 levels up to reach a container
            that holds both.

        Strategy: locate label by EXACT text, then walk up parents until we
        find one whose inner_text contains a numeric token. The amount is
        the LAST number in that text (label never has digits)."""
        import re
        try:
            label_node = self.page.locator(
                f"xpath=//*[normalize-space(text())='{label}']"
            ).first
            label_node.wait_for(state="visible", timeout=5000)

            # Walk up to 5 levels until we find a container with a number
            for level in range(1, 6):
                up_xpath = "/".join([".."] * level)
                try:
                    container = label_node.locator(f"xpath={up_xpath}")
                    text = container.inner_text().strip()
                    matches = re.findall(r"[\d,]+\.?\d*", text)
                    if matches:
                        # The last number is the amount (label never has digits)
                        return f"{label}  {matches[-1]}"
                except Exception:
                    continue
            return ""
        except Exception:
            return ""

    @allure.step("Get Convenience Charges amount")
    def get_convenience_charges_amount(self) -> str:
        return self._read_amount_for_label("Convenience Charges")

    @allure.step("Get Order Amount value")
    def get_order_amount(self) -> str:
        return self._read_amount_for_label("Order Amount")

    @allure.step("Get Total Amount value")
    def get_total_amount(self) -> str:
        return self._read_amount_for_label("Total Amount")

    @allure.step("Get merchant name shown on checkout summary card")
    def get_merchant_name_on_checkout(self) -> str:
        """Returns the merchant display name (e.g. 'Chinmay Bharat Academy')."""
        try:
            # Closest heading above the 'SabPaisa Trusted' badge
            badge = self.page.get_by_text("SabPaisa Trusted").first
            el = badge.locator(
                "xpath=preceding::*[self::h1 or self::h2 or self::h3 or "
                "self::p or self::span][1]"
            )
            return el.first.inner_text().strip()
        except Exception:
            return ""

    @allure.step("Check SabPaisa Trusted badge visible")
    def is_sabpaisa_trusted_badge_visible(self) -> bool:
        try:
            self.page.get_by_text("SabPaisa Trusted").first.wait_for(
                state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @staticmethod
    def _extract_amount(text: str) -> float:
        """Pull the first numeric amount (float) from a string like
        'Total Amount  ₹19.9' → 19.9. Returns 0.0 if none."""
        import re
        m = re.search(r"[\d,]+\.?\d*", (text or "").replace(",", ""))
        return float(m.group(0)) if m else 0.0

    # ══════════════════════════════════════════════
    #  Language dropdown (EN / HI / etc.)
    # ══════════════════════════════════════════════

    BTN_LANG_DROPDOWN = {
        "xpath": "//button[.//*[contains(@class,'lucide-chevron-down')]]",
        "css": "button:has(.lucide-chevron-down)",
    }

    @allure.step("Open language dropdown")
    def open_language_dropdown(self):
        self.engine.click(self.BTN_LANG_DROPDOWN, timeout=10000)
        self.wait(800)

    @allure.step("Get available languages in dropdown")
    def get_available_languages(self) -> list:
        """Returns the visible language choices inside the open dropdown.
        Must be called AFTER open_language_dropdown()."""
        try:
            langs = self.page.evaluate("""() => {
                // Look for any open list items / menu options below the
                // language button. Heuristic: recently-visible list items
                // whose text is short (language names are <= 15 chars).
                const items = document.querySelectorAll(
                    'div[role="menu"] button, ul[role="listbox"] li, div[class*="dropdown"] button, div[class*="menu"] button'
                );
                const out = [];
                for (const el of items) {
                    if (el.offsetParent === null) continue;
                    const t = (el.innerText || '').trim();
                    if (t && t.length <= 20 && !out.includes(t)) out.push(t);
                }
                return out;
            }""")
            return langs or []
        except Exception:
            return []

    @allure.step("Select language: {name}")
    def select_language(self, name: str):
        """Click the language option with the given visible text.
        Dropdown must already be open."""
        self.page.get_by_text(name, exact=False).first.click(timeout=8000)
        self.wait(1000)

    @allure.step("Get current language label (e.g. 'EN')")
    def get_current_language_label(self) -> str:
        try:
            btn = self.engine.find(self.BTN_LANG_DROPDOWN, timeout=5000)
            return btn.inner_text().strip()
        except Exception:
            return ""

    # ══════════════════════════════════════════════
    #  ACTIONS — Netbanking
    # ══════════════════════════════════════════════

    @allure.step("Search bank: {query}")
    def search_bank(self, query: str):
        self.engine.fill(self.INPUT_SEARCH_BANK, query, timeout=20000)
        self.wait(2000)

    @allure.step("Select Karur Vysya Bank")
    def select_karur_vysya(self):
        self.engine.click(self.IMG_KARUR_VYSYA, timeout=20000)
        self.wait(1000)

    @allure.step("Select Bank of Baroda Net Banking Corporate")
    def select_bob_corporate(self):
        self.engine.click(self.IMG_BOB_CORPORATE, timeout=20000)
        self.wait(1000)

    @allure.step("Select Bank of Baroda Net Banking Retail")
    def select_bob_retail(self):
        self.engine.click(self.IMG_BOB_RETAIL, timeout=20000)
        self.wait(1000)

    @allure.step("Select Equitas Bank")
    def select_equitas_bank(self):
        self.engine.click(self.IMG_EQUITAS_BANK, timeout=20000)
        self.wait(1000)

    @allure.step("Select Indian Overseas Bank")
    def select_indian_overseas(self):
        self.engine.click(self.IMG_INDIAN_OVERSEAS, timeout=20000)
        self.wait(1000)

    @allure.step("Select State Bank of India")
    def select_sbi(self):
        self.engine.click(self.IMG_SBI, timeout=20000)
        self.wait(1000)

    @allure.step("Select IDFC FIRST Bank")
    def select_idfc_bank(self):
        self.engine.click(self.IMG_IDFC_BANK, timeout=20000)
        self.wait(1000)

    @allure.step("Click Show all banks")
    def click_show_all_banks(self):
        self.engine.click(self.BTN_SHOW_ALL_BANKS, timeout=10000)
        self.wait(2000)

    @allure.step("Click Hide all banks")
    def click_hide_all_banks(self):
        self.engine.click(self.BTN_HIDE_ALL_BANKS, timeout=10000)
        self.wait(1000)

    @allure.step("Select bank from full list: {bank_name}")
    def select_bank_from_list(self, bank_name: str):
        """Click a bank row in the expanded 'Show all banks' list.
        The row is a <button> containing a <span> with the bank name.
        Matched by visible text so both normal and highlighted (bg-blue-50)
        states resolve to the same locator."""
        self.page.locator("button").filter(has_text=bank_name).first.click()
        self.wait(800)

    @allure.step("Click Cancel on bank gateway dialog")
    def click_cancel(self):
        self.engine.click(self.BTN_CANCEL, timeout=10000)
        self.wait(1000)

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
        self.engine.click(self.BTN_CASH, timeout=10000)
        self.wait(1000)

    @allure.step("Select RTGS option")
    def select_rtgs(self):
        self.engine.click(self.BTN_RTGS, timeout=10000)
        self.wait(1000)

    @allure.step("Select IMPS option")
    def select_imps(self):
        self.engine.click(self.BTN_IMPS, timeout=10000)
        self.wait(1000)

    @allure.step("Select Bank Of India")
    def select_bank_of_india(self):
        self.engine.click(self.IMG_BANK_OF_INDIA, timeout=10000)
        self.wait(1000)

    @allure.step("Select Bank of India Retail")
    def select_bank_of_india_retail(self):
        self.engine.click(self.IMG_BANK_OF_INDIA_RETAIL, timeout=10000)
        self.wait(1000)

    @allure.step("Select Airtel Bank")
    def select_airtel_bank(self):
        self.engine.click(self.IMG_AIRTEL_BANK, timeout=10000)
        self.wait(1000)

    @allure.step("Select FINO Bank")
    def select_fino_bank(self):
        self.engine.click(self.IMG_FINO_BANK, timeout=10000)
        self.wait(1000)

    @allure.step("Select ICICI Bank")
    def select_icici_bank(self):
        self.engine.click(self.IMG_ICICI_BANK, timeout=10000)
        self.wait(1000)

    @allure.step("Select IDFC First Bank RTGS")
    def select_idfc_first_rtgs(self):
        self.engine.click(self.IMG_IDFC_FIRST_RTGS, timeout=10000)
        self.wait(1000)

    @allure.step("Select IMPS bank by badge: {badge}")
    def select_imps_bank_by_badge(self, badge: str):
        """IMPS banks render a 2-letter initials badge (e.g., 'SA').
        Target the button whose uppercase badge div matches."""
        self.page.locator(
            f"button:has(div.uppercase.font-bold:has-text('{badge}'))"
        ).first.click()
        self.wait(1000)

    @allure.step("Click 'Pay at bank'")
    def click_pay_at_bank(self):
        self.engine.click(self.BTN_PAY_AT_BANK, timeout=10000)
        self.wait(2000)

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
    def is_qr_visible(self, timeout: int = 30000) -> bool:
        """The UPI QR can take 15-25 seconds to render (it has a generation
        timer / spinner first). Wait up to `timeout` ms (default 30s) for any
        QR element to appear: <canvas>, <img alt='QR'>, <svg class='qr'>,
        <div class*='qr'>, or any element with 'qr-code' / 'qrcode' class."""
        try:
            self.page.locator(
                "canvas, "
                "img[alt*='QR'], img[alt*='qr'], "
                "svg[class*='qr'], svg[class*='QR'], "
                "[class*='qr-code'], [class*='qrcode'], [class*='QrCode'], "
                "[class*='qr']"
            ).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    @allure.step("Check if card form is visible")
    def is_card_form_visible(self) -> bool:
        return self.engine.is_visible(self.INPUT_CARD_NUMBER, timeout=5000)

    @allure.step("Check if Pay button is visible")
    def is_pay_visible(self) -> bool:
        return self.engine.is_visible(self.BTN_PAY_PROCEED, timeout=5000)

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

    @allure.step("Check if challan / bank-gateway page opened after Pay at bank")
    def is_challan_opened(self, timeout_ms: int = 8000) -> bool:
        """Heuristic: after 'Pay at bank', we either (a) navigate off the
        checkout page to a gateway/challan URL, or (b) a challan panel
        renders on the same page with keywords like 'challan', 'reference',
        'download', 'payment instruction', etc."""
        self.wait(timeout_ms)
        url = self.page.url.lower()
        if "checkout" not in url and "configure" not in url and "about:blank" not in url:
            return True
        try:
            indicator = self.page.locator(
                "text=/challan|download.*challan|reference.*no|payment.*instruction|bank.*details/i"
            ).first
            indicator.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    @allure.step("Get current page URL")
    def get_current_url(self) -> str:
        return self.page.url

    @allure.step("Get all bank names from Netbanking")
    def get_all_bank_names(self) -> list:
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
        self.page.locator(f"img[alt='{bank_name}']").first.click()
        self.wait(1000)

    @allure.step("Get all wallet names")
    def get_all_wallet_names(self) -> list:
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

    @allure.step("Discover visible netbanking popular banks (dynamic per client)")
    def get_visible_netbanking_popular_alts(self) -> list:
        """Call AFTER self.select_netbanking() and a brief wait.
        Returns alt attributes for every bank image in the popular-banks
        grid — only real banks, mode tabs filtered out."""
        try:
            self.page.evaluate("""() => {
                const el = document.querySelector('div.flex-1.p-4.overflow-y-auto');
                if (el) { el.scrollTo({top: 0}); }
            }""")
            self.wait(400)
            alts = self.page.evaluate("""() => {
                const MODE_NAMES = ['upi','card','netbanking','net banking',
                                    'offline','wallet','wallets','scan qr','generate qr'];
                const grids = document.querySelectorAll(
                    'div[class*="grid-cols-3"], div[class*="grid-cols-4"]'
                );
                const out = [];
                for (const grid of grids) {
                    if (grid.offsetParent === null) continue;
                    for (const btn of grid.querySelectorAll('button')) {
                        if (btn.offsetParent === null) continue;
                        const img = btn.querySelector('img');
                        if (!img) continue;
                        const alt = (img.alt || '').trim();
                        if (!alt) continue;
                        const low = alt.toLowerCase();
                        if (MODE_NAMES.some(m => low === m || low.startsWith(m + ' '))) continue;
                        if (!out.includes(alt)) out.push(alt);
                    }
                }
                return out;
            }""")
            return alts or []
        except Exception:
            return []

    @allure.step("Discover visible offline banks on current sub-tab (Cash / RTGS)")
    def get_visible_offline_bank_alts(self) -> list:
        """Call AFTER selecting an offline sub-tab (Cash or RTGS).
        Returns image-alt identifiers for each bank shown."""
        try:
            alts = self.page.evaluate("""() => {
                const MODE_NAMES = ['upi','card','netbanking','net banking',
                                    'offline','wallet','wallets','cash','rtgs','imps','neft'];
                const grids = document.querySelectorAll(
                    'div[class*="grid-cols-3"], div[class*="grid-cols-4"]'
                );
                const out = [];
                for (const grid of grids) {
                    if (grid.offsetParent === null) continue;
                    for (const btn of grid.querySelectorAll('button')) {
                        if (btn.offsetParent === null) continue;
                        const img = btn.querySelector('img');
                        if (!img) continue;
                        const alt = (img.alt || '').trim();
                        if (!alt) continue;
                        const low = alt.toLowerCase();
                        if (MODE_NAMES.some(m => low === m || low.startsWith(m + ' '))) continue;
                        if (!out.includes(alt)) out.push(alt);
                    }
                }
                return out;
            }""")
            return alts or []
        except Exception:
            return []

    @allure.step("Discover visible IMPS banks (badge-based — e.g. 'SA')")
    def get_visible_offline_imps_badges(self) -> list:
        """IMPS banks are often rendered with 2-letter initials badges
        (e.g. 'SA' for SabPaisa) instead of icons. Returns the badge text."""
        try:
            badges = self.page.evaluate("""() => {
                const badges = document.querySelectorAll(
                    'div.flex-1.p-4.overflow-y-auto div.uppercase.font-bold'
                );
                const out = [];
                for (const b of badges) {
                    if (b.offsetParent === null) continue;
                    const t = (b.innerText || '').trim();
                    if (t && !out.includes(t)) out.push(t);
                }
                return out;
            }""")
            return badges or []
        except Exception:
            return []

    @allure.step("Discover visible wallets (dynamic — whatever the current client offers)")
    def get_visible_wallet_alts(self) -> list:
        """After clicking Wallets tab, returns a list of identifiers — one
        per wallet button in the grid. Works per-client: 4 for CHIN36,
        7 for another, 9 for another — no hardcoded list.

        Uses page.evaluate() to read the DOM in the browser directly,
        avoiding Playwright auto-wait hangs. Also scrolls the panel
        top → bottom → top first so any lazy-mounted buttons render."""
        try:
            # Scroll reveal (JS side, no auto-wait)
            self.page.evaluate("""() => {
                const el = document.querySelector('div.flex-1.p-4.overflow-y-auto');
                if (!el) return;
                el.scrollTo({top: el.scrollHeight});
            }""")
            self.wait(500)
            self.page.evaluate("""() => {
                const el = document.querySelector('div.flex-1.p-4.overflow-y-auto');
                if (!el) return;
                el.scrollTo({top: 0});
            }""")
            self.wait(300)

            # Two-stage filter:
            #  1. Scope to the WALLET GRID only (div with grid-cols-* class).
            #     Payment-mode tabs use a vertical layout, NOT grid-cols.
            #  2. Blacklist obvious mode names as a safety net in case
            #     another grid-cols div exists elsewhere.
            alts = self.page.evaluate("""() => {
                const MODE_NAMES = [
                    'upi', 'card', 'netbanking', 'net banking',
                    'offline', 'wallet', 'wallets',
                    'scan qr', 'generate qr'
                ];
                // Find grid containers (wallets + banks use grid-cols-3/4)
                const grids = document.querySelectorAll(
                    'div[class*="grid-cols-3"], div[class*="grid-cols-4"]'
                );
                const out = [];
                for (const grid of grids) {
                    // Skip hidden grids
                    if (grid.offsetParent === null) continue;
                    const buttons = grid.querySelectorAll('button');
                    for (const btn of buttons) {
                        if (btn.offsetParent === null) continue;
                        const img = btn.querySelector('img');
                        if (!img) continue;
                        const alt = (img.alt || '').trim();
                        if (!alt) continue;
                        // Skip if alt matches a known payment-mode name
                        const low = alt.toLowerCase();
                        if (MODE_NAMES.some(m => low === m || low.startsWith(m + ' '))) continue;
                        if (!out.includes(alt)) out.push(alt);
                    }
                }
                return out;
            }""")
            return alts or []
        except Exception:
            return []

    # ══════════════════════════════════════════════
    #  COMPOSED WORKFLOWS
    # ══════════════════════════════════════════════

    @allure.step("Complete Cards flow")
    def complete_cards_flow(self, number, holder, expiry, cvv):
        self.wait_for_checkout_load()
        self.select_cards()
        self.enter_card_number(number)
        self.enter_card_holder(holder)
        self.enter_card_expiry(expiry)
        self.enter_card_cvv(cvv)
