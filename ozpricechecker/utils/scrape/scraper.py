"""Scrape Functionality."""

import logging

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

USER_AGENT_CHROME = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'  # pylint: disable=line-too-long


class SeleniumChromeSession():
    """Context Manager wrapper for a Selenium Chrome Session."""

    def __init__(self, *, chrome, chrome_webdriver):
        """Initialize the Session."""
        # Using Portable Chrome, we see some issues
        #   "DevToolsActivePort file doesn't exist"
        # raised from selenium sometimes, not always for the same tests
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument(
            F'user-agent={USER_AGENT_CHROME}')
        chrome_options.binary_location = chrome

        chrome_options.add_argument('--headless')

        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Disable Listening STDOUT message
        # https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        # Avoiding Selenium Detection
        # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=chrome_webdriver)

        # Avoiding Selenium Detection
        # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
        })

    def __enter__(self):
        return self.driver.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.__exit__(exc_type, exc_val, exc_tb)


class WaitCondition():
    """Define a Wait Condition."""

    def __init__(self, name, locator_type, search_str):
        """Create a Wait Condition."""
        self.name = name
        self.type = locator_type
        self.search_str = search_str

    def __str__(self):
        return F'{self.name} - {self.type} - {self.search_str}'


class ScraperWait():
    """Handle simple multiple conditions for waiting for Elements to Load."""

    # pylint: disable=too-few-public-methods

    def __init__(self, conditions):
        """Initialize the Waiter object."""
        self.conditions = conditions
        self.found_elements = {}

    def __call__(self, driver):
        """Handle Object Calls."""
        # Test all outstanding events
        for cond in self.conditions:
            if cond.name not in self.found_elements:
                elem = self._find_element(driver, cond.type, cond.search_str)

                if elem:
                    self.found_elements[cond.name] = elem.text

        # Verify if we have everything we need
        if len(self.found_elements) == len(self.conditions):
            # We need to return an element, so pick any
            return list(self.found_elements.values())[0]

        # We haven't all elements needed to fulfill our conditions
        return False

    @staticmethod
    def _find_element(driver, locator_type, search_str):
        found_elem = None
        try:
            candidate_elem = driver.find_element(locator_type, search_str)
        except NoSuchElementException:
            pass
        else:
            found_elem = candidate_elem

        return found_elem


def scrape_with_selenium(chrome, chrome_webdriver, url, xpath_tup_list, timeout):
    """Scrape using Selenium and Chrome."""
    result_dic = {}

    with SeleniumChromeSession(chrome=chrome, chrome_webdriver=chrome_webdriver) as driver:
        wait_conditions = []
        for xpath_tup in xpath_tup_list:
            wait_conditions.append(WaitCondition(xpath_tup[0], By.XPATH, xpath_tup[1]))

        try:
            driver.get(url)
        except WebDriverException as error:
            logger.error(F'Issue: {error} for url "{url}"')
        else:
            scraper_wait = ScraperWait(wait_conditions)
            try:
                WebDriverWait(driver, timeout).until(scraper_wait)
            except TimeoutException:
                logger.error(F'Timeout waiting for url "{url}"')
            else:
                result_dic = scraper_wait.found_elements

    return result_dic


def scrape_page(*, chrome, chrome_webdriver, url, xpath_tup_list):
    """xpath_tup_list = [(Name, Xpath), (Name, Xpath)]."""
    if not xpath_tup_list:
        raise ValueError('No Xpath Specified')

    # Ensure Names are Unique
    unique_names = list(set(entry[0] for entry in xpath_tup_list))
    if len(unique_names) != len(xpath_tup_list):
        raise ValueError('Cannot have Duplicate Xpth Identifier')

    logger.info(F'Scrape Url: "{url}"')

    timeout = 10
    return scrape_with_selenium(chrome, chrome_webdriver, url, xpath_tup_list, timeout)
