import sheet
import pdfScraper
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen
import time
import sys
import re

def scrapeSOS():

    filerId = sheet.getFilerId()
    filerId = filerId.replace(" ", "")
    if 'Nothing' in filerId:
        sys.exit("Nothing to tweet")

    print(filerId)
    display = Display(visible=0, size=(1341,810))
    display.start()
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
    driver = webdriver.Chrome('/root/darkmoney/chromedriver', chrome_options=opts)
    driver.get("http://apps.azsos.gov/apps/election/cfs/search/AdvancedSearch.aspx")
    time.sleep(6)

    #This needs to take the filerID from the spreadsheet
    
    filerIdField = driver.find_element_by_id("ctl00_ctl00_PageContent_Sear"+
            "chControlsContent_AdvancedSearchUserControl_FilerIdTextBox")

    actions = ActionChains(driver)
    actions.move_to_element(filerIdField)
    actions.click(filerIdField)
    filerIdField.clear()
    actions.send_keys(filerId + Keys.RETURN)
    actions.perform()

    time.sleep(6)

    address = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageConte'+
            'nt_SearchControlsContent_AdvancedSearchDataUserControl_FilerD'+
            'ataRadGrid_ctl00__0"]/td[1]')

    filing_committee = address.text
    address.click()

    time.sleep(6)

    driver.find_element(By.LINK_TEXT, 'More >>').click()

    time.sleep(6)
    pdf_link = driver.find_element_by_xpath('//*[@id="ctl00_ctl00_PageCont'+
    'ent_SearchControlsContent_CommitteeDetailsPopupWindow_C_CommitteeDeta'+
    'ilsControl_CommitteeReportsWindow_C_CommitteeReportsControl_AllReport'+
    's_ReportsPreviousTable"]/tbody/tr[3]/td[4]/a')

    pdf_link.click()

    regex = re.compile('PublicReports.*pdf') 
    pdf_link = pdf_link.get_attribute('href')
    pdf_link = regex.findall(pdf_link)[0]

    # Send the filing url to sheet.py 
    pdf_url = 'http://apps.azsos.gov/apps/election/cfs/search/'+pdf_link

    #Switch to the new tab
    #readPDF(urlopen('http://apps.azsos.gov/apps/election/cfs/search/'+pdf_link))
    req = Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
    pdf = urlopen(req)
    with open("scrapedPDF.pdf", 'wb') as f:
        f.write(pdf.read())
        f.close()
    darkmoney_rows = pdfScraper.scrape('scrapedPDF.pdf')
    sheet.fillSheet(darkmoney_rows, pdf_url, filing_committee, filerId)
    driver.quit()
scrapeSOS()
