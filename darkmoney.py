import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import time
import re


def readPDF(pdffile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdffile)
    device.close()

    content = retstr.getvalue()
    retstr.close()

    print(content)
    with open('samplePDF.txt', 'w') as f:
        f.write(content)
        f.close()
    pdffile.close()

"""
***Not sure whether I can somehow use this to modify the headers when using
   PhantomJS, so we'll use chromedriver in the meantime.

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) 
            Gecko/20100101 Firefox/47.0", 
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

#This needs to take the filerID from the spreadsheet
filerId ='201400888' 

filerIdField = driver.find_element_by_id("ctl00_ctl00_PageContent_Sear"+
        "chControlsContent_AdvancedSearchUserControl_FilerIdTextBox")

actions = ActionChains(driver)
actions.move_to_element(filerIdField)
actions.click(filerIdField)
filerIdField.clear()
actions.send_keys(filerId + Keys.RETURN)

actions.perform()

#waitForLoad(driver)

time.sleep(3)

address = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageConte'+
        'nt_SearchControlsContent_AdvancedSearchDataUserControl_FilerD'+
        'ataRadGrid_ctl00__0"]/td[1]')
print(address.text)
address.click()

time.sleep(3)

driver.find_element(By.LINK_TEXT, 'More >>').click()

time.sleep(3)
pdf_link = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageCont'+
'ent_SearchControlsContent_CommitteeDetailsPopupWindow_C_CommitteeDeta'+
'ilsControl_CommitteeReportsWindow_C_CommitteeReportsControl_AllReport'+
's_ReportsPreviousTable"]/tbody/tr[3]/td[4]/a')

print(pdf_link.get_attribute('href'))
pdf_link.click()

regex = re.compile('PublicReports.*pdf') 
pdf_link = pdf_link.get_attribute('href')
pdf_link = regex.findall(pdf_link)[0]

#Switch to the new tab
readPDF(urlopen('http://apps.azsos.gov/apps/election/cfs/search/'+pdf_link))
driver.close()

