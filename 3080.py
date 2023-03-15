import time
import sys
import bs4
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

#RTX 3080 Link
#url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
#Test URL
#url = ''

#My FireFox
#commented out and removed my personal hard coded information
def create_driver():
    options = Options()
    options.headless = False
    #profile = webdriver.FirefoxProfile(r"") Path to firefox directory here
    web_driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
    return web_driver

def time_sleep(x, driver):
    #Page Refresh Time
    for i in range(x, -1, -1):
        sys.stdout.write('\r')
        sys.stdout.write("{:2d} seconds".format(i))
        sys.stdout.flush()
        time.sleep(.4)
    driver.execute_script("window.localStorage.clear();")
    driver.refresh()

def extract_page():
    html = driver.page_source
    #BeautifulSoup to find html elements 
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

def driver_click(driver, find_type, selector):
    while True:
        if find_type == 'css':
            try:
                driver.find_element_by_css_selector(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(1)
        elif find_type == 'name':
            try:
                driver.find_element_by_name(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(1)
        elif find_type == 'xpath':
            try:
                driver.find_element_by_xpath(f"//*[@class='{selector}']").click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(1)

def card_buyer(driver):
    driver.get(url)
    while True:
        soup = extract_page()
        wait = WebDriverWait(driver, 15)
        wait2 = WebDriverWait(driver, 5)
        try:
            add_to_cart_button = soup.find('button', {
                'class': 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'})
            if add_to_cart_button:
                print("3080 Releasing!")
                try:
                    # Entering queue and Waiting to click "add to cart" 2nd time
                    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.add-to-cart-button')))
                    driver_click(driver, 'css', '.add-to-cart-button')
                    print("In queue now")
                except NoSuchElementException as error:
                    print("Some Kind of Error Occurred")
                    pass

                # In queue, just waiting for "add to cart" button to turn clickable again.
                # Swapped to 1 hour of waiting after pressing the first add to cart button.
                while True:
                    try:
                        add_to_cart = driver.find_element_by_css_selector('.add-to-cart-button')
                        please_wait = add_to_cart.get_attribute('aria-describedby')
                        if please_wait:
                            time.sleep(3600)
                        else:  
                            # When Add to Cart appears. This will click button.
                            print("Add To Cart Button Clicked\n")
                            wait2.until(
                                ec.presence_of_element_located((By.CSS_SELECTOR, ".add-to-cart-button")))
                            time.sleep(2)
                            driver_click(driver, 'css', '.add-to-cart-button')
                            time.sleep(2)
                            break
                    except NoSuchElementException as error:
                        print("Some Kind of Error Occurred")

                # Going to cart faster
                driver.get("https://www.bestbuy.com/cart")

                # Checking if the card is still in the cart
                try:
                    wait.until(ec.presence_of_element_located((By.XPATH,
                        '''//*[@class='btn btn-lg btn-block btn-primary']''')))
                    time.sleep(1)
                    driver_click(driver, 'xpath', 'btn btn-lg btn-block btn-primary')
                    print("Still in Cart!")
                except NoSuchElementException:
                    print("not in cart.")
                    time_sleep(1, driver)
                    card_buyer(driver)

                # BestBuy has periodically been requiring a manual sign in so this will login just in case
                # commented out and removed the password for my Best Buy account
                try:
                    time.sleep(5)
                    wait.until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, '.btn-secondary')))
                    time.sleep(1)
                    # driver.find_element_by_id('fld-p1').send_keys("") Put password for BestBuy here
                    driver_click(driver, 'css', '.btn-secondary')
                except NoSuchElementException:
                    # FireFox will auto login if manual sign in is not needed
                    print("\nFireFox should auto sign in\n")
                    pass

                # Final Checkout
                try:
                    wait2.until(ec.presence_of_element_located((By.XPATH,
                        '''//*[@class='btn btn-lg btn-block btn-primary button__fast-track']''')))
                    print("Placing Order!")
                    # comment this below to test without purchasing
                    driver_click(driver, 'xpath', 'btn btn-lg btn-block btn-primary button__fast-track')
                    print("Finally got a graphics card!")
                    time.sleep(1800)
                    driver.quit()
                except NoSuchElementException:
                    print("Did Not Get the Card")

        except NoSuchElementException as error:
            print("Some Kind of Error Occurred")

        time_sleep(1, driver)

if __name__ == "__main__":
    driver = create_driver()
    card_buyer(driver)