from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pathlib
from pathlib import Path
import pickle

url = 'https://microgreen.ferumflex.com/'

# driver = webdriver.Firefox(executable_path=Path(pathlib.Path.home(), "geckodriver.exe"))  # домашняя директория
driver = webdriver.Firefox(executable_path=Path(pathlib.Path.cwd(), 'tests', "geckodriver.exe"))  # рабочая директория


try:
    driver.get(url=url)
    # time.sleep(3)

    enter_link = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[1]/td/div/ul/li[4]/a[2]').click()
    # time.sleep(3)

    login_input = driver.find_element_by_name("username")
    login_input.clear()
    login_input.send_keys('12345678')
    # time.sleep(3)

    pass_input = driver.find_element_by_name("password")
    pass_input.clear()
    pass_input.send_keys('Testpassword1')
    # time.sleep(3)

    # enter_link = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/form/button').click()

    pass_input.send_keys(Keys.ENTER)
    time.sleep(6)

    #  запись cookies
    pickle.dump(driver.get_cookies(), open("cookies", "wb"))

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
