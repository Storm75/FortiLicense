#!/usr/bin/python3

"""Forti License

Usage:
  fortilicense.py -n <customername> -c <contract> -s <serial>
  fortilicense.py (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import selenium.webdriver.support.ui as ui
import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='fortilicense 0.3beta')
    customername = "" if arguments['<customername>'] is None else arguments['<customername>']
    contract = "" if arguments['<contract>'] is None else arguments['<contract>']
    serial = "" if arguments['<serial>'] is None else arguments['<serial>']
    if len(contract) != 12: print("Contract number should be 12 caracters")
    if len(serial) != 16: print("Serial number should be 16 caracters")
    if len(contract) != 12 or len(serial) != 16: sys.exit(1)


def leave_customer(found):
    print("Number of customers found " + str(found) + " != 1")
    sys.exit(1)


STARTURL = "https://partnerportal.fortinet.com"
USER = ""
PASS = ""

chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)  # Optional argument, if not specified will search path.
driver.set_window_size(800, 600)
driver.implicitly_wait(5)
driver.get(STARTURL)

wait = ui.WebDriverWait(driver, 5)
#  Login
login_username = driver.find_element_by_xpath('html/body/form/section/div/div[1]/div/div[2]/div/div[1]/input')
login_pass = driver.find_element_by_xpath('/html/body/form/section/div/div[1]/div/div[2]/div/div[2]/input')
wait.until(lambda driver: login_username)
login_username.send_keys(USER)
wait.until(lambda driver: login_pass)
login_pass.send_keys(PASS)
driver.find_element_by_xpath('/html/body/form/section/div/div[1]/div/div[2]/div/a[1]').click()
# Go to registration 1/2
driver.get(
    driver.find_element_by_xpath('/html/body/form/header/section/nav/div/div[1]/div/ul/li[4]/a').get_attribute("href"))
time.sleep(0.5)
# Go to registration 2/2
driver.get('https://support.fortinet.com/product/RegistrationEntry.aspx')
# Select client
select = driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_RegCodeStep_UC_Partner_DDL_Customers")
selectsupport = Select(select)
allOptions = select.find_elements_by_tag_name("option")
found = 0
for option in allOptions:
    if customername.lower() in str(option.text).lower():
        print("Customer : " + str(option.text))
        targetOption = option.text
        found += 1

selectsupport.select_by_visible_text(targetOption) if found == 1 else leave_customer(found)
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_RegCodeStep_TB_Code").send_keys(contract)  # Fill Contract
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_RegCodeStep_rbNonGovUser").click()  # Non gov
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_BTN_Next").click()  # Next
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_RegContractStep_UC_RegCTL_TB_SerialNo").send_keys(serial)  # Fill Serial
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_BTN_Next").click()  # Next
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_BTN_Next").click()  # Next (doubleclick)
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_AggrementStep_chkAgreement").click()  # I have read, understood...
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_BTN_Next").click()  # Next
driver.find_element_by_id("ctl00_Content_UC_RegWizardControl_VerificationStep_UC_ContractTerm_cb_complete").click()  # By accepting these terms
