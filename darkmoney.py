import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time

"""
***Not sure whether I can somehow use this to modify the headers when using
   PhantomJS, so we'll use chromedriver in the meantime.

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", 
            "Accept":"text/html,applicaiton/xhtml+xml; q=0.9,image/webp,*/*;q=0.8"}
"""
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("body")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("body")
        except StaleElementReferenceException:
            return

driver = webdriver.Chrome('/home/qstin/chromedriver')
driver.set_window_size(1440, 900)
driver.get("http://apps.azsos.gov/apps/election/cfs/search/AdvancedSearch.aspx")
time.sleep(5)
filerId = "201400888"
filerIdField = driver.find_element_by_id("ctl00_ctl00_PageContent_SearchControlsContent_AdvancedSearchUserControl_FilerIdTextBox")
#hiddenInput = driver.find_element_by_id("ctl00_ctl00_PageContent_SearchControlsContent_AdvancedSearchUserControl_FilerIdTextBox_ClientState")
actions = ActionChains(driver)
actions.move_to_element(filerIdField)
actions.click(filerIdField)
filerIdField.clear()
actions.send_keys(filerId + Keys.RETURN)
#actions.send_keys_to_element(hiddenInput,
#        '{"enabled":true,"emptyMessage":"","validationText":"201400888","valueAsString":"201400888","lastSetTextBoxValue":"201400888"}')
actions.perform()
#waitForLoad(driver)
time.sleep(3)
address = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageContent_SearchControlsContent_AdvancedSearchDataUserControl_FilerDataRadGrid_ctl00__0"]/td[1]')
print(address.text)
address.click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageContent_SearchControlsContent_CommitteeDetailsPopupWindow_C_CommitteeDetailsControl_MoreInfoLink"]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageContent_SearchControlsContent_CommitteeDetailsPopupWindow_C_CommitteeDetailsControl_CommitteeReportsWindow_C_CommitteeReportsControl_AllReports_ReportsPreviousTable"]/tbody/tr[3]/td[4]/a').click()
driver.close()
