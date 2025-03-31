import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_bidding():
    geckodriver_path = "/snap/bin/geckodriver"
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

    driver = webdriver.Firefox(service=driver_service)
    # driver = webdriver.Firefox()
    driver.get("http://localhost:8000/")
    driver.find_element(By.NAME, "username").send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("AnotherPassword")
    driver.find_element(By.NAME, "submit").click()

    driver.find_element(By.CLASS_NAME, "auction").click()
    price_input = driver.find_element(By.NAME, "price")
    price = price_input.get_attribute("value")
    price_input.clear()
    price_input.send_keys(f'{round(float(price) + 0.01, 2)}')
    driver.find_element(By.NAME, "submit").click()
    # time.sleep(100)
    driver.quit()


def test_bidding_multiple():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(10):
            executor.submit(test_bidding)


if __name__ == '__main__':
    test_bidding_multiple()