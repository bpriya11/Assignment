from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
import sys
import json

def get_captcha():
   capt = input('enter captcha')
   return capt

chromedriver_location = "/Users/DELL/Downloads/chromedriver"
driver = webdriver.Chrome(chromedriver_location)
driver.get('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')

#xpath of all the input fields
licence_no='//*[@id="form_rcdl:tf_dlNO"]'
dob='//*[@id="form_rcdl:tf_dob_input"]'
captcha='//*[@id="form_rcdl:j_idt32:CaptchaID"]'
submit='//*[@id="form_rcdl:j_idt43"]'

#provide inputs to the input fields

#dl_NO=input('enter dl NO')
#driver.find_element_by_xpath(licence_no).send_keys(dl_no)
driver.find_element_by_xpath(licence_no).send_keys("DL-0420110149646")
#dob=input('enter dob')
#driver.find_element_by_xpath(dob).send_keys(dob)
driver.find_element_by_xpath(dob).send_keys("09-02-1976")
captt=get_captcha()
driver.find_element_by_xpath(captcha).send_keys(captt)
driver.find_element_by_xpath(submit).click()

#sleep to load for the logged in page
sleep(3)

#getting the details of the driving licence.
try:
    element = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt13"]/div/ul/li/span[1]').text
    if(element=='Verification code does not match.'):
        print('Invalid captcha')
        driver.quit()
except:
    finalans=[]
    p=[]
    soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
    #getting data from each table
    for table in soup_level1.find_all('table'):
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            p.append(row)
        ad=pd.DataFrame(p)
        p=[]
        x=ad.to_json(orient='records')
        finalans.append(x)
    print(finalans[:-1])
