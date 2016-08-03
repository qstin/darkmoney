import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
        filer_cell = 'C' + str(len(list_of_rows)-1)
        sh = gc.open('Dark Money email sheet')
        sh2 = sh.worksheet('Sheet2')
        val = sh2.acell(filer_cell)
        wks.update_acell('G' + str(row_count-1), 'tweeted')
    else:
        val = 'Nothing new to tweet'
    return val
