from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import pathlib


class VerificationSMS:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument(f'--user-data-dir={pathlib.Path().absolute()}/selenium') 

    def send_message(self, email, password, phone_number, verfication_code):
        shouldLogin = False
        if not os.path.isdir(f'{pathlib.Path().absolute()}/selenium'):
            shouldLogin = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.chrome_options) 
        driver.get(r'https://accounts.google.com/signin/v2/challenge/pwd?service=grandcentral&passive=1209600&continue=https%3A%2F%2Fvoice.google.com%2Fsignup&followup=https%3A%2F%2Fvoice.google.com%2Fsignup6') 
        driver.implicitly_wait(15) 
        if shouldLogin:
            email_phone = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
            email_phone.send_keys(email)
            driver.find_element_by_id("identifierNext").click()
            pw = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
            )
            pw.send_keys(password)
            driver.find_element_by_id("passwordNext").click()
            driver.implicitly_wait(10)
        messages = driver.find_elements_by_xpath('//*[@aria-label ="Messages"]') 
        messages[1].click() 
        newMessage=driver.find_elements_by_xpath('//*[@gv-id="send-new-message"]')
        newMessage[0].click()
        numberInput=driver.find_element_by_id("input_1")
        numberInput.send_keys(phone_number)
        confirmInput=driver.find_element_by_id("stp1")
        confirmInput.click()
        messageContent=driver.find_element_by_id("input_2")
        messageContent.send_keys(f"Your confirmation code is: {verfication_code}")
        messageContent.send_keys(Keys.ENTER)
        driver.close()

        

