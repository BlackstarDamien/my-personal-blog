from typing import List, Tuple
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)
    
    def wait_for(self, locator: Tuple[str, str]) -> WebElement:
        """Waits for given element to be displayed on page.

        Parameters
        ----------
        locator : Tuple[str, str]
            Element's locator as a pair of type and name.

        Returns
        -------
        WebElement
            Instance of element that appeared on page.
        """
        return self._wait.until(ec.presence_of_element_located(locator))
    
    def find(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Use given locator to fetch and return instances
        of given element.

        Parameters
        ----------
        locator : Tuple[str, str]
            Element's locator as a pair of type and name.

        Returns
        -------
        List[WebElement]
            List of elements for given locator.
        """
        return self.driver.find_elements(*locator)

