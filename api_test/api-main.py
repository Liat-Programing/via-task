from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service


def login(driver, name, password, s) -> None:
    driver.find_element(By.ID, 'login2').click()
    driver.find_element(By.ID, 'loginusername').clear()
    driver.find_element(By.ID, 'loginusername').send_keys(name)
    driver.find_element(By.ID, 'loginpassword').clear()
    driver.find_element(By.ID, 'loginpassword').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#logInModal > div > div > div.modal-footer > button.btn.btn-primary').click()
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present(), 'wait for alert')
        alert1 = driver.switch_to.alert
        # if had problem with login make s variable as flag
        if 'User does not exist.' in alert1.text or 'Wrong password.' in alert1.text:
            s = 1
        # accept alert
        alert1.accept()
        # close
        driver.find_element(By.CSS_SELECTOR, '#logInModal > div > div > div.modal-footer > button.btn.btn-secondary') \
            .click()
        if s == 1:
            s = 2
            # go to signup
            signup(driver, name, password, s)
    except TimeoutException:
        pass


def signup(driver, name, password, s) -> None:
    driver.find_element(By.ID, 'signin2').click()
    driver.find_element(By.ID, 'sign-username').send_keys(name)
    driver.find_element(By.ID, 'sign-password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR,
                        '#signInModal > div > div > div.modal-footer > button.btn.btn-primary').click()
    # catch the alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present(), 'wait for alert')
        alert = driver.switch_to.alert
        # accept alert
        alert.accept()
    except TimeoutException:
        pass
    login(driver, name, password, s)


def buy_nexus_6(driver) -> int:
    driver.find_element(By.CSS_SELECTOR, '#tbodyid > div:nth-child(3) > div > div > h4 > a').click()
    driver.find_element(By.CSS_SELECTOR, '#tbodyid > div.row > div > a').click()
    url_id = ''
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present(), 'wait for alert')
        alert2 = driver.switch_to.alert
        alert2.accept()
        url_id = driver.current_url
        return url_id.split('idp_=', 1)[1].split('#')[0]
    except TimeoutException:
        print('was not alert')
        pass


def check_cart(driver, id) -> None:
    # navigate to the cart
    driver.find_element(By.ID, 'cartur').click()
    all_tr = driver.find_elements(By.CSS_SELECTOR, '#tbodyid > tr')
    if len(all_tr) == 1:
        price = driver.find_element(By.CSS_SELECTOR, '#tbodyid > tr > td:nth-child(3)').text
        if price == '650':
            product_name = driver.find_element(By.CSS_SELECTOR, '#tbodyid > tr > td:nth-child(2)').text
            if 'Nexus 6' in product_name:
                if '3' in id:
                    print('yes!! you buy Nexus 6!')
    else:
        print("Oh! you did not buy Nexus 6!")


def logout(driver):
    driver.find_element(By.CSS_SELECTOR, '#logout2').click()


def main() -> None:
    # create driver
    path = r'C:\automation\drivers\chromedriver.exe'
    s = Service(path)
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()

    # api url
    url_scraping = "https://www.demoblaze.com/"
    # send get request
    driver.get(url_scraping)

    name = 'Liat'
    password = 'liat1234'
    s = 0

    driver.implicitly_wait(3.5)
    # go to login func
    login(driver, name, password, s)
    # let's start shopping!
    id = buy_nexus_6(driver)
    check_cart(driver, id)

    driver.implicitly_wait(20)
    logout(driver)
    driver.quit()
    driver.close()


main()
