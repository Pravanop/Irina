#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
# In[1]:
chrome_options= Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_driver = os.getcwd() +"\\chromedriver.exe"

#company=input("Give the company name:")


# In[2]:
    
def stock_price(query):
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    driver.get("https://www.google.com") 
    import time 
    time.sleep(4)
    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.submit()
    time.sleep(3)
    price= driver.find_element_by_css_selector("span[jsname='vWLAgc']")
    percent=driver.find_element_by_css_selector("span[jsname='rfaVEf']")
    return 'It is at '+ price.text + 'and ' + percent.text 

# In[ ]:


#print(stock_price(company))

