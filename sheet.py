import tweet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import sys

def getFilerId():

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'darkmoney-946284ca9b91.json',
            scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('Dark Money email sheet').sheet1
    list_of_rows = wks.get_all_values()
    row_count = len(list_of_rows)

    if list_of_rows[len(list_of_rows)-1][6] != 'tweeted':
        filer_cell = 'C' + str(len(list_of_rows))
        sh = gc.open('Dark Money email sheet')
        sh2 = sh.worksheet('Sheet2')
        val = sh2.acell(filer_cell).value
        #The line below needs to be called after the tweet
        #It'd be best to incorporate the 
        wks.update_acell('G' + str(row_count), 'tweeted')
    else:
        val = 'Nothing new to tweet'
    return val

def fillSheet(darkmoney_rows, pdf_url, filing_committee, filer_id):

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'darkmoney-946284ca9b91.json',
            scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('Dark Money Bank')
    filers_sheet = wks.worksheet('SOS pdf filing rows')
    row_list = filers_sheet.get_all_values()
    next_row_num = len(row_list)+1

    # Set up Twitter driver and open Tweets Sheet
    twitterDriver = tweet.authorizeTwitter()
    tweet_wks = wks.worksheet('Tweets')

    # Format row into filers_sheet columns
    """
    Coloumn headers:
        
        FilingID:         A
        Expenditure Date: B
        Filing Committee: C
        Elect or Defeat:  D
        Target Comm ID:   E
        Target Committee: F
        Amount:           G
        URL:              H
    """

    for item in darkmoney_rows:
        next_row_num = str(next_row_num)

        filers_sheet.update_acell('A'+next_row_num, filer_id)

        matched_date = re.search(r'(\d+/\d+/\d+)', item)
        date = matched_date.group(0)
        filers_sheet.update_acell('B'+next_row_num, date)

        filers_sheet.update_acell('C'+next_row_num, filing_committee)
        
        regex = re.search("Advocating (\w+)", item) 
        to_elect_or_defeat = regex.group(0) 
        filers_sheet.update_acell('D'+next_row_num, to_elect_or_defeat)

        regex = re.search(r'\D(\d{9})\D', item)
        target_committee_id = regex.group(0).strip() 
        filers_sheet.update_acell('E'+next_row_num, target_committee_id)
        
        # Target committee
        regex = re.compile('(?<=-)(.*)\$')  
        try:
            tc = regex.findall(item)[0].strip()
        except IndexError:
            regex = re.compile('(?<=-)(.*)$')
            tc = regex.findall(item)[0].strip()
        regex = re.search("Advocating (\w+)", tc)
        if regex != None:
            tc = tc.split(regex.group(0))[0].strip()
        filers_sheet.update_acell('F'+next_row_num, tc)

        regex = re.compile(r'\$+.*[.]\d\d')
        transaction_amount = regex.findall(item)[0]
        filers_sheet.update_acell('G'+next_row_num, transaction_amount)

        filers_sheet.update_acell('H'+next_row_num, pdf_url)

        item_tweet = tweet_wks.acell('G'+next_row_num).value
        
        tweet.sendTweet(twitterDriver, item_tweet)

        next_row_num = int(next_row_num)+1
