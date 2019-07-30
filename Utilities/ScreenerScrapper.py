import requests
import time
import re
import math
from bs4 import BeautifulSoup
from selenium import webdriver

SAMPLE_SIZE = 8

class ScreenerScrapper():
    def __init__(self, url):
        self.url = url
        #self.response = requests.get(url)
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.soup = None
        #BeautifulSoup(self.response.text, "html.parser")
        self.table_info = {}

    def scrapUsingSelenium(self):
        self.driver.implicitly_wait(5)
        self.driver.get(self.url)

        python_buttons = self.driver.find_elements_by_class_name('show-schedules')
        for python_button in python_buttons:
            python_button.click()

        self.driver.switch_to_window(self.driver.window_handles[0])
        time.sleep(3)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        self.driver.quit()

    def getTitle(self):
        title = self.soup.find('title')
        return title.text

    def extractTables(self):

        # result variable
        self.table_info = {}

        # Find all the front information about stock
        front_info = self.soup.findAll(class_='four columns')
        for info in front_info:
            key = info.text
            try:
                value = info.find(b).text
            except:
                value = ''
            print(key, value)

        # Names of tables present in the page that we are scrapping
        table_names = ["","quarterlyPL","Income Statement","","","","Balance Sheet","Cash Flow Statement","Ratios"]
        # extract all the tables present in page
        tables = self.soup.findAll('table')

        # go through each table
        idx = 0
        for table in tables:

            curr_list = []

            # see if table head is present
            table_head = table.find('thead')
            if table_head:

                table_head_info = {}
                # extract all table head
                head_columns = table_head.findAll('th')

                head_row = []

                # go through each column the head row
                for head_column in head_columns:
                    head_row.append(head_column.text)

                # first idx has name of row and rest indices have data
                table_head_info['head'] = head_row[1:]
                # append the data as dictionary into a list
                curr_list.append(table_head_info)

                # Extract table body
                table_row_info = {}
                table_rows = table.findAll('tr')

                for table_row in table_rows:
                    columns = table_row.findAll('td')
                    output_row = []

                    for column in columns:
                        output_row.append(column.text)

                    if output_row:
                        table_row_info[output_row[0].strip()] = output_row[1:]

                curr_list.append(table_row_info)

                self.table_info[table_names[idx]] = curr_list

            idx = idx+1

        # This returns a dictionary of list of dictionaries (whose values are lists)
        return self.table_info

    def printExtractedTable(self, dict):
        for key, val in dict.items():
            print(key, "=>")
            for item in val:
                for inner_key, inner_val in item.items():
                    print(inner_key, "=>", inner_val)


def getIncome(table_info):
    response = {}

    response['head'] = sliceList(table_info['Income Statement'][0]['head'])

    response['Sales'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Sales']))
    response['YoY_Growth'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Sales Growth %']))
    response['5yr_Sales_CAGR'] = []

    response['Expenses'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Expenses']))
    response['Material_Cost'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Material Cost %']))
    response['Employee_Cost'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Employee Cost %']))
    response['Manufacturing_Cost'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Manufacturing Cost %']))
    response['Other_Cost'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Other Cost %']))

    response['Operating_Profit'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Operating Profit']))
    response['OPM'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['OPM %']))

    response['Other_Income'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Other Income']))

    response['Interest'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Interest']))
    response['Interest_to_Revenue'] = []

    response['Depreciation'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Depreciation']))
    response['Depreciation_to_Revenue'] = []

    response['PBT'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Profit before tax']))

    response['Tax'] = cleanupPercentage(sliceList(table_info['Income Statement'][1]['Tax %']))

    response['PAT'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Net Profit']))
    response['5yr_PAT_CAGR'] = []

    response['EPS'] = cleanupComma(sliceList(table_info['Income Statement'][1]['EPS in Rs']))
    response['EPS_Growth'] = []

    for idx in range(len(response['head'])):

        response['Interest_to_Revenue'].append(round(response['Interest'][idx]/response['Sales'][idx], 2) * 100)

        response['Depreciation_to_Revenue'].append(round(response['Depreciation'][idx] / response['Sales'][idx], 2) * 100)

    for idx in range(len(response['head'])):
        if (idx - 4) >= 0:
            response['5yr_Sales_CAGR'].append(round( (float((float(response['Sales'][idx] / response['Sales'][(idx-4)]) ** float(1/5))) - 1)*100, 2))
            response['5yr_PAT_CAGR'].append(round( (float((float(response['PAT'][idx] / response['PAT'][(idx - 4)]) ** float(1 / 5))) - 1) * 100, 2))
        if (idx - 1) >= 0:
            response['EPS_Growth'].append(growthCalculation(response['EPS'][idx], response['EPS'][idx-1]))
        else:
            response['EPS_Growth'].append(0)

    return response


def getQuarter(table_info):
    response = {}

    response['head'] = sliceList(table_info['quarterlyPL'][0]['head'], 0)

    response['Sales'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Sales'], 0))
    response['YoY_Growth'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Sales Growth %'], 0))
    response['5yr_Sales_CAGR'] = []

    response['Expenses'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Expenses'], 0))
    if 'Material Cost %' in table_info['quarterlyPL'][1]:
        response['Material_Cost'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Material Cost %'], 0))
    if 'Employee Cost %' in table_info['quarterlyPL'][1]:
        response['Employee_Cost'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Employee Cost %'], 0))
    if 'Manufacturing Cost %' in table_info['quarterlyPL'][1]:
        response['Manufacturing_Cost'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Manufacturing Cost %'], 0))
    if 'Other Cost %' in table_info['quarterlyPL'][1]:
        response['Other_Cost'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Other Cost %'], 0))

    response['Operating_Profit'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Operating Profit'], 0))
    response['OPM'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['OPM %'], 0))

    response['Other_Income'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Other Income'], 0))

    response['Interest'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Interest'], 0))
    response['Interest_to_Revenue'] = []

    response['Depreciation'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Depreciation'], 0))
    response['Depreciation_to_Revenue'] = []

    response['PBT'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Profit before tax'], 0))

    response['Tax'] = cleanupPercentage(sliceList(table_info['quarterlyPL'][1]['Tax %'], 0))

    response['PAT'] = cleanupComma(sliceList(table_info['quarterlyPL'][1]['Net Profit'], 0))
    response['5yr_PAT_CAGR'] = []

    response['Face_Value'] = 1
    response['Equity'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Share Capital'], 0))

    response['EPS'] = []
    response['EPS_Growth'] = []

    for idx in range(len(response['head'])):

        response['EPS'].append(round(response['PAT'][idx]/response['Equity'][idx], 2) * response['Face_Value'])

        response['Interest_to_Revenue'].append(round(response['Interest'][idx]/response['Sales'][idx], 2) * 100)

        response['Depreciation_to_Revenue'].append(round(response['Depreciation'][idx] / response['Sales'][idx], 2) * 100)

    for idx in range(len(response['head'])):
        if (idx - 4) >= 0:
            response['5yr_Sales_CAGR'].append(round( (float((float(response['Sales'][idx] / response['Sales'][(idx-4)]) ** float(1/5))) - 1)*100, 2))
            response['5yr_PAT_CAGR'].append(round( (float((float(response['PAT'][idx] / response['PAT'][(idx - 4)]) ** float(1 / 5))) - 1) * 100, 2))
        if (idx - 1) >= 0:
            response['EPS_Growth'].append(growthCalculation(response['EPS'][idx], response['EPS'][idx-1]))
        else:
            response['EPS_Growth'].append(0)

    return response


def sliceList(dataList, TTM_element_size = 1):
    length = len(dataList) - TTM_element_size
    if length > SAMPLE_SIZE:
        return dataList[length-SAMPLE_SIZE:length]
    else:
        return ['1'] * (SAMPLE_SIZE-length) + dataList[0:length]


def cleanupComma(dataList):
    for idx in range(len(dataList)):
        dataList[idx] = re.sub(',', '', dataList[idx])
        dataList[idx] = float(dataList[idx])
    return dataList


def cleanupPercentage(dataList):
    for idx in range(len(dataList)):
        dataList[idx] = re.sub('%', '', dataList[idx])
        if dataList[idx] == '':
            dataList[idx] = '0'
        dataList[idx] = float(dataList[idx])
    return dataList


def growthCalculation(x, y):
    return round(((x - y) / y) * 100, 2)

#url = "https://www.screener.in/company/CAPLIPOINT/consolidated/"
#object = ScreenerScrapper(url)
#object.scrapUsingSelenium()
#print(object.getTitle())
#dict = object.extractTables()
#object.printExtractedTable(dict)
#print(object.getSales())
