"""CustomerPage — Customer details form and checkout trigger."""

import allure
from pages.base_page import BasePage


class CustomerPage(BasePage):

    # ── Locators ──

    INPUT_CUSTOMER_ID    = {"xpath": "//input[@id='customerId']",    "css": "#customerId"}
    INPUT_CUSTOMER_NAME  = {"xpath": "//input[@id='customerName']",  "css": "#customerName"}
    INPUT_CUSTOMER_EMAIL = {"xpath": "//input[@id='customerEmail']", "css": "#customerEmail"}
    INPUT_CUSTOMER_PHONE = {"xpath": "//input[@id='customerPhone']", "css": "#customerPhone"}
    INPUT_AMOUNT         = {"xpath": "//input[@id='amount']",        "css": "#amount"}
    INPUT_DESCRIPTION    = {"xpath": "//input[@id='description']",   "css": "#description"}
    BTN_ADV_CHEVRON      = {"xpath": "//span[@id='advChevron']",     "css": "#advChevron"}
    BTN_ADV_OPTIONS      = {"xpath": "//button[@type='button']",     "css": "button[type='button']"}
    BOTTOM_BAR           = {"xpath": "//div[@class='bottom-bar']",   "css": ".bottom-bar"}
    BTN_CHECKOUT         = {"xpath": "//button[@id='checkoutBtn']",  "css": "#checkoutBtn", "text": "Proceed to Checkout"}

    # ── Actions ──

    @allure.step("Enter Customer ID: {value}")
    def enter_customer_id(self, value):
        self.engine.fill(self.INPUT_CUSTOMER_ID, value)

    @allure.step("Enter Customer Name: {value}")
    def enter_customer_name(self, value):
        self.engine.fill(self.INPUT_CUSTOMER_NAME, value)

    @allure.step("Enter Customer Email: {value}")
    def enter_customer_email(self, value):
        self.engine.fill(self.INPUT_CUSTOMER_EMAIL, value)

    @allure.step("Enter Customer Phone: {value}")
    def enter_customer_phone(self, value):
        self.engine.fill(self.INPUT_CUSTOMER_PHONE, value)

    @allure.step("Enter Amount: {value}")
    def enter_amount(self, value):
        self.engine.fill(self.INPUT_AMOUNT, value)

    @allure.step("Enter Description: {value}")
    def enter_description(self, value):
        self.engine.fill(self.INPUT_DESCRIPTION, value)

    @allure.step("Click Advanced Options chevron")
    def click_advanced_chevron(self):
        self.engine.click(self.BTN_ADV_CHEVRON)

    @allure.step("Click Advanced Options button")
    def click_advanced_options(self):
        self.engine.click(self.BTN_ADV_OPTIONS)

    @allure.step("Click bottom bar")
    def click_bottom_bar(self):
        self.engine.click(self.BOTTOM_BAR)

    @allure.step("Click Proceed to Checkout")
    def click_checkout(self):
        self.engine.click(self.BTN_CHECKOUT)

    # ── Validation Helpers ──

    @allure.step("Check if Checkout button is disabled")
    def is_checkout_disabled(self) -> bool:
        btn = self.engine.find(self.BTN_CHECKOUT)
        return btn.is_disabled()

    @allure.step("Check if Checkout button is visible")
    def is_checkout_visible(self) -> bool:
        return self.engine.is_visible(self.BTN_CHECKOUT, timeout=5000)

    @allure.step("Get field value: {field_css}")
    def get_field_value(self, field_css: str) -> str:
        return self.page.locator(field_css).input_value()

    @allure.step("Check if page stayed on customer form (no navigation)")
    def is_still_on_customer_form(self) -> bool:
        return self.engine.is_visible(self.INPUT_CUSTOMER_ID, timeout=5000)

    @allure.step("Check if validation error shown")
    def has_validation_error(self) -> bool:
        try:
            self.page.locator(".error, .invalid, [aria-invalid='true'], .text-red, .border-red, .text-danger").first.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    # ── Workflows ──

    @allure.step("Fill customer details")
    def fill_customer_details(self, customer_id, name, email, phone, amount, description):
        self.enter_customer_id(customer_id)
        self.enter_customer_name(name)
        self.enter_customer_email(email)
        self.enter_customer_phone(phone)
        self.enter_amount(amount)
        self.enter_description(description)

    @allure.step("Handle advanced options and proceed to checkout")
    def handle_advanced_and_checkout(self):
        self.click_advanced_chevron()
        self.scroll_down(400)
        self.wait(500)
        self.scroll_up(200)
        self.click_advanced_options()
        self.click_bottom_bar()
        self.click_checkout()
