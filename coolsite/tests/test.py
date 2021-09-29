
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://microgreen.ferumflex.com/')
burger = driver.find_element_by_xpath('//*[@id="mainmenu"]/li[7]/div/a')