"""
Program Name: scraper.py
Author: Kevin Lindemann
Date: 10/18/2025
Purpose: Collect the data from Google Analytics. This requires that the Selenium connection with Chrome is already set up. 
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GA4Scraper: 
    def __init__(self, debugger="127.0.0.1:9222"):
        self.debugger = debugger
        self.driver = None

    def connect(self):
        options = webdriver.ChromeOptions()
        options.debugger_address = self.debugger
        self.driver = webdriver.Chrome(options=options)
        return self.driver
    
    def navigate(self, url):

        try:
            self.driver.execute_script("window.open('', '_blank');")
            time.sleep(1)
            new_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_tab)
            self.driver.get(url)
        except Exception as e: 
            print(f"Navigation Error: {e}")
            try:
                self.connect()
                self.driver.get(url)
            except Exception as e:
                print(f"Reconnection Issue in Scraper.Py. {e}")

    def get_active_users(self):
        try:
            wait = WebDriverWait(self.driver, 120)
            elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "counter")))
            val = int(elem.text.replace(",", ""))
            print(f"Active Users: {val}")
            #TODO: Add error for if invalid internal literal is not able to be recognized as an integer. 
            return val
        except Exception as e:
            print(f"GA4 Scraper Error: {e}")
            return "N/A"
        
    def quit(self):
        if self.driver:
            self.driver.quit()