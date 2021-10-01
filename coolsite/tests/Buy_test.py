import pickle
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pickle
import pathlib
from pathlib import Path
import random
url = 'https://microgreen.ferumflex.com/'

driver = webdriver.Firefox(executable_path=Path(pathlib.Path.cwd(), 'tests', "geckodriver.exe"))  


try:
    driver.get(url=url)
    # time.sleep(3)

    for cookie in pickle. load(open('cookies', 'rb')):
        driver.add_cookie(cookie)

    time.sleep(1)
    driver.refresh()
    time.sleep(2)

    cart_input = driver.find_element_by_id("id_quantity")
    cart_input.clear()
    cart_input.send_keys(random.randint(1, 9))
    time.sleep(3)

    buy_button = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/ul/li[1]/form/p[2]/input').click()
    time.sleep(3)

    buy_button = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/form/p/button').click()
    time.sleep(3)
    


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
