"""ConfigurePage — Environment selection, merchant ID, fetch config."""

import allure
from pages.base_page import BasePage
from config.settings_manager import BASE_URL, ENVIRONMENT


class ConfigurePage(BasePage):

    # ── Locators ──

    FORM_CARD         = {"xpath": "//div[@id='formCard']",                    "css": "#formCard"}
    BTN_STAGING       = {"xpath": "//button[normalize-space()='Staging']",     "text": "Staging"}
    BTN_PRODUCTION    = {"xpath": "//button[normalize-space()='Production']",  "text": "Production"}
    INPUT_MERCHANT_ID = {"xpath": "//input[@id='merchantId']",                 "css": "#merchantId"}
    BTN_FETCH         = {"xpath": "//button[@id='fetchBtn']",                  "css": "#fetchBtn"}
    INPUT_API_URL     = {"xpath": "//input[@id='merchantApiUrl']",             "css": "#merchantApiUrl"}
    INPUT_CHECKOUT_URL= {"xpath": "//input[@id='checkoutBaseUrl']",            "css": "#checkoutBaseUrl"}
    BTN_CONTINUE      = {"xpath": "//button[normalize-space()='Continue']",    "css": "button[type='submit']", "text": "Continue"}

    # ── Actions ──

    @allure.step("Open configure page")
    def open(self):
        self.navigate(BASE_URL)

    @allure.step("Reload page")
    def reload_page(self):
        self.reload()

    @allure.step("Click environment form card")
    def click_form_card(self):
        self.engine.click(self.FORM_CARD)

    @allure.step("Select Staging environment")
    def select_staging(self):
        self.engine.click(self.BTN_STAGING)

    @allure.step("Select Production environment")
    def select_production(self):
        self.engine.click(self.BTN_PRODUCTION)

    @allure.step("Select environment: {env}")
    def select_environment(self, env: str = None):
        """Select environment from config or override."""
        env = env or ENVIRONMENT
        if env.lower() == "staging":
            self.select_staging()
        else:
            self.select_production()

    @allure.step("Enter Merchant ID: {merchant_id}")
    def enter_merchant_id(self, merchant_id: str):
        self.engine.fill(self.INPUT_MERCHANT_ID, merchant_id)

    @allure.step("Click Fetch button")
    def click_fetch(self):
        self.engine.click(self.BTN_FETCH)

    @allure.step("Wait for fetch to complete")
    def wait_for_fetch_complete(self):
        self.page.wait_for_function(
            """() => {
                const btn = document.querySelector('#fetchBtn');
                return btn && !btn.textContent.includes('Fetching');
            }""",
            timeout=30000,
        )

    @allure.step("Click Merchant API URL field")
    def click_merchant_api_url(self):
        self.engine.click(self.INPUT_API_URL)

    @allure.step("Click Checkout Base URL field")
    def click_checkout_base_url(self):
        self.engine.click(self.INPUT_CHECKOUT_URL)

    @allure.step("Click Continue")
    def click_continue(self):
        self.engine.click(self.BTN_CONTINUE)

    # ── Validation Helpers ──

    @allure.step("Check if Fetch button is disabled")
    def is_fetch_disabled(self) -> bool:
        btn = self.engine.find(self.BTN_FETCH)
        return btn.is_disabled()

    @allure.step("Check if Continue button is visible")
    def is_continue_visible(self) -> bool:
        return self.engine.is_visible(self.BTN_CONTINUE, timeout=5000)

    @allure.step("Check if Merchant API URL is empty")
    def is_api_url_empty(self) -> bool:
        el = self.engine.find(self.INPUT_API_URL)
        return el.input_value() == ""

    @allure.step("Get Fetch button text")
    def get_fetch_button_text(self) -> str:
        return self.engine.find(self.BTN_FETCH).inner_text()

    @allure.step("Check if error/alert is shown on page")
    def has_error_on_page(self) -> bool:
        try:
            self.page.locator(
                ".error, .alert, [role='alert'], .toast-error, .text-red, "
                ".text-danger, .Toastify, [class*='toast'], [class*='Toast']"
            ).first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Check if 'Client not found' error is shown")
    def has_client_not_found_error(self) -> bool:
        try:
            self.page.get_by_text("Client not found").first.wait_for(state="visible", timeout=8000)
            return True
        except Exception:
            return False

    @allure.step("Check if fetch succeeded (API URL populated)")
    def is_fetch_success(self) -> bool:
        """A successful fetch populates the Merchant API URL field.
        Empty URL after fetch → fetch failed or wasn't clicked."""
        try:
            el = self.engine.find(self.INPUT_API_URL, timeout=5000)
            val = (el.input_value() or "").strip()
            return bool(val)
        except Exception:
            return False

    @allure.step("Check if green success indicator / trust badge visible after fetch")
    def is_green_success_indicator_visible(self) -> bool:
        """After a good fetch, a green badge/icon typically renders
        (client-trusted / verified / SabPaisa badge). Covers multiple
        common class names since the exact one varies."""
        try:
            self.page.locator(
                "[class*='success'], [class*='text-green'], [class*='text-emerald'], "
                "[class*='bg-green'], [class*='bg-emerald'], "
                ".fa-check-circle, .fa-cloud, [data-status='success']"
            ).first.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    @allure.step("Get merchant/client name shown after fetch")
    def get_fetched_client_name(self) -> str:
        """Returns the merchant display name rendered after fetch
        (empty string if not found)."""
        try:
            # Try common containers: merchant card, client info label, etc.
            candidates = self.page.locator(
                "[class*='merchant'], [class*='client-name'], "
                "[class*='client-display'], [class*='clientInfo']"
            )
            if candidates.count() > 0 and candidates.first.is_visible():
                return candidates.first.inner_text().strip()
            return ""
        except Exception:
            return ""

    @allure.step("Get page URL")
    def get_current_url(self) -> str:
        return self.page.url

    # ── Workflow ──

    @allure.step("Configure merchant: {merchant_id}")
    def configure_merchant(self, merchant_id: str):
        self.open()
        self.reload_page()
        self.click_form_card()
        self.select_environment()
        self.enter_merchant_id(merchant_id)
        self.click_fetch()
        self.wait_for_fetch_complete()
        self.scroll_down(300)
        self.click_merchant_api_url()
        self.click_checkout_base_url()
        self.click_continue()
