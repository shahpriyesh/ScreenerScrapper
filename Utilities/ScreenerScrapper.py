import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScreenerScrapper():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def scrapUsingSelenium(self):
        self.driver.implicitly_wait(30)
        self.driver.get(self.url)
        python_button = self.driver.find_element(By.XPATH, '//*[@id="quarters"]/div/table/tbody/tr[1]/td[1]/button')
        python_button.click()
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        print(self.soup.prettify())
        self.driver.quit()

    def getTitle(self):
        title = self.soup.find('title')
        return title.text

    def extractTables(self):

        # result variable
        table_info = {}
        # Names of tables present in the page that we are scrapping
        table_names = ["quarterlyPL","Income Statement","","","","Balance Sheet","Cash Flow Statement","Ratios"]
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
                print(curr_list)
                table_info[table_names[idx]] = curr_list
            idx = idx+1

        # This returns a dictionary of list of dictionaries (whose values are lists)
        return table_info

    def printExtractedTable(self, dict):
        for key, val in dict.items():
            print(key, "=>")
            for item in val:
                for inner_key, inner_val in item.items():
                    print(inner_key, "=>", inner_val)


url = "https://www.screener.in/company/CAPLIPOINT/consolidated/"
object = ScreenerScrapper(url)
#print(object.getTitle())
object.scrapUsingSelenium()
dict = object.extractTables()
object.printExtractedTable(dict)
