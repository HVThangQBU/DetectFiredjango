import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from web import browser
thisdict =	{
}
for x, y in thisdict.items():
  # Github credentials
  username = x
  password = y

  # initialize the Chrome driver
  driver = webdriver.Chrome(r"chromedriver")
  # head to github login page
  driver.get("https://www.netflix.com/vn-en/login")
  # find username/email field and send the username itself to the input field
  # driver.find_element_by_id("login_field").send_keys(username)
  driver.find_element(by=By.ID, value="id_userLoginId").send_keys(username)
  # find password input field and insert password as well
  #driver.find_element_by_id("password").send_keys(password)
  driver.find_element(by=By.ID, value="id_password").send_keys(password)

  # click login button
  #driver.find_element_by_name("commit").click()
  driver.find_element(By.CSS_SELECTOR, value=".btn.login-button.btn-submit.btn-small").click()
  print(x)
  time.sleep(5)


