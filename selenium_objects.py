from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os


# options
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.page_load_strategy = 'normal'
userDataDir = os.path.abspath('./chromium-user-data')
options.add_argument(f'--user-data-dir={userDataDir}')


# Create required instances
client = webdriver.Chrome(executable_path='chromedriver', options=options)
wait = WebDriverWait(client, 10)
