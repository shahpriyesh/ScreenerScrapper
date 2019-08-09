import re

SAMPLE_SIZE = 10
LAST_EIGHT_QUARTERS = 8

BALANCE_SHEET = 'Balance Sheet'
INCOME_STATEMENT = "Income Statement"
QUARTER_STATEMENT = "quarterlyPL"
CASH_FLOW_STATEMENT = "Cash Flow Statement"

def getIncome(table_info):
    response = {}
    param_dict = {
        "Sales": ["Sales", 1],
        "Sales Growth %": ["YoY_Growth", 1],
        "Expenses": ["Expenses", 1],
        "Material Cost %": ["Material_Cost", 1],
        "Employee Cost %": ["Employee_Cost", 1],
        "Manufacturing Cost %": ["Manufacturing_Cost", 1],
        "Other Cost %": ["Other_Cost", 1],
        "Operating Profit": ["Operating_Profit", 1],
        "OPM %": ["OPM", 1],
        "Other Income": ["Other_Income", 1],
        "Interest": ["Interest", 1],
        "Depreciation": ["Depreciation", 1],
        "Profit before tax": ["PBT", 1],
        "Tax %": ["Tax", 0],
        "Net Profit": ["PAT", 1],
        "EPS in Rs": ["EPS", 0]
    }

    response = parseValues(INCOME_STATEMENT, table_info, param_dict)

    response['title'] = table_info['title']
    response['head'] = sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][0]['head'], 1)

    response['5yr_Sales_CAGR'] = []

    response['Expenses_Growth'] = []

    response['Interest_to_Revenue'] = []
    response['Depreciation_to_Revenue'] = []

    response['5yr_PAT_CAGR'] = []
    response['NPM'] = []
    response['EPS_Growth'] = []

    for idx in range(len(response['head'])):

        response['Interest_to_Revenue'].append(round(response['Interest'][idx]/response['Sales'][idx], 2) * 100)
        response['Depreciation_to_Revenue'].append(round(response['Depreciation'][idx] / response['Sales'][idx], 2) * 100)

        response['NPM'].append(round(response['PAT'][idx] / response['Sales'][idx], 2) * 100)

        if (idx - 4) >= 0:
            response['5yr_Sales_CAGR'].append(round( (float((float(response['Sales'][idx] / response['Sales'][(idx-4)]) ** float(1/5))) - 1)*100, 2))
            response['5yr_PAT_CAGR'].append(round( (float((float(response['PAT'][idx] / response['PAT'][(idx - 4)]) ** float(1 / 5))) - 1) * 100, 2))

        if (idx - 1) >= 0:
            response['Expenses_Growth'].append(growthCalculation(response['Expenses'][idx], response['Expenses'][idx - 1]))
            response['EPS_Growth'].append(growthCalculation(response['EPS'][idx], response['EPS'][idx-1]))
        else:
            response['Expenses_Growth'].append(0)
            response['EPS_Growth'].append(0)

    return response


def getQuarter(table_info):
    response = {}

    param_dict = {
        "Sales": ["Sales", 0],
        "YOY Sales Growth %": ["YoY_Growth", 0],
        "Expenses": ["Expenses", 0],
        "Material Cost %": ["Material_Cost", 0],
        "Employee Cost %": ["Employee_Cost", 0],
        "Manufacturing Cost %": ["Manufacturing_Cost", 0],
        "Other Cost %": ["Other_Cost", 0],
        "Operating Profit": ["Operating_Profit", 0],
        "OPM %": ["OPM", 0],
        "Other Income": ["Other_Income", 0],
        "Interest": ["Interest", 0],
        "Depreciation": ["Depreciation", 0],
        "Profit before tax": ["PBT", 0],
        "Tax %": ["Tax", 0],
        "Net Profit": ["PAT", 0]
    }

    response = parseValues(QUARTER_STATEMENT, table_info, param_dict)

    response['title'] = table_info['title']
    response['head'] = sliceList(QUARTER_STATEMENT, table_info[QUARTER_STATEMENT][0]['head'], 0)

    response['Interest_to_Revenue'] = []
    response['Depreciation_to_Revenue'] = []

    response['Equity'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Share Capital'], 0))

    response['EPS'] = []
    response['EPS_Growth'] = []

    response['NPM'] = []

    for idx in range(len(response['head'])):

        response['EPS'].append(round(response['PAT'][idx]/response['Equity'][idx], 2) * float(table_info['Face Value']))

        response['Interest_to_Revenue'].append(round(response['Interest'][idx]/response['Sales'][idx], 2) * 100)

        response['Depreciation_to_Revenue'].append(round(response['Depreciation'][idx] / response['Sales'][idx], 2) * 100)

        response['NPM'].append(round(response['PAT'][idx] / response['Sales'][idx], 2) * 100)

    for idx in range(len(response['head'])):
        if (idx - 1) >= 0:
            response['EPS_Growth'].append(growthCalculation(response['EPS'][idx], response['EPS'][idx-1]))
        else:
            response['EPS_Growth'].append(0)

    return response


def getCashFlow(table_info):
    response = {}

    param_dict = {
        "Cash from Operating Activity": ["CFO", 0],
        "Profit from operations": ["Profit_From_Ops", 0],
        "Working Capital Changes": ["WCC", 0],
        "Taxes paid": ["Taxes_Paid", 0],
        "Cash from Investing Activity": ["CFI", 0],
        "Fixed Assets Purchased": ["Fixed_Assets_Purchased", 0],
        "Fixed Assets Sold": ["Fixed_Assets_Sold", 0],
        "Investments purchased": ["Investments_Purchased", 0],
        "Investments sold": ["Investments_Sold", 0],
        "Cash from Financing Activity": ["CFF", 0],
        "Proceeds from Borrowings": ["Proceeds_from_Borrowings", 0],
        "Repayment of Borrowings": ["Repayment_of_Borrowings", 0],
        "Interest Paid": ["Interest_Paid", 0],
        "Dividends Paid": ["Dividends_Paid", 0],
        "Net Cash Flow": ["Net_Cash_Flow", 0]
    }

    response = parseValues(CASH_FLOW_STATEMENT, table_info, param_dict)

    response['title'] = table_info['title']
    response['head'] = sliceList(CASH_FLOW_STATEMENT, table_info[CASH_FLOW_STATEMENT][0]['head'], 0)

    response['CFO_Growth'] = []
    response['5yr_CFO_CAGR'] = []
    response['CFO_to_PAT'] = []
    response['CFPS'] = []

    response['PAT'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Net Profit']))
    response['Depreciation'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Depreciation'], 0))
    response['Face_Value'] = 1
    response['Equity'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Share Capital'], 0))

    for idx in range(len(response['head'])):
        response['CFO_to_PAT'].append(round(response['CFO'][idx]/response['PAT'][idx], 2))
        response['CFPS'].append(round( (response['CFO'][idx] - response['Depreciation'][idx]) / response['Equity'][idx], 2) * float(table_info['Face Value']))

    for idx in range(len(response['head'])):
        if (idx - 4) >= 0:
            response['5yr_CFO_CAGR'].append(round( (float((float(response['CFO'][idx] / response['CFO'][(idx-4)]) ** float(1/5))) - 1)*100, 2))
        if (idx - 1) >= 0:
            response['CFO_Growth'].append(growthCalculation(response['CFO'][idx], response['CFO'][idx-1]))
        else:
            response['CFO_Growth'].append(0)

    return response


def getBalanceSheet(table_info):
    response = {}
    param_dict = {"Share Capital": ["Share", 0],
                  "Equity Capital": ["Equity", 0],
                  "Reserves": ["Reserves", 0],
                  "Borrowings": ["Borrowings", 0],
                  "Other Liabilities": ["Other_Liabilities", 0],
                  "Trade Payables": ["Payables", 0],
                  "Total Liabilities": ["Total_Liabilities", 0],
                  "Fixed Assets": ["Fixed_Assets", 0],
                  "Gross Block": ["Gross_Block", 0],
                  "Accumulated Depreciation": ["Acc_Depreciation", 0],
                  "CWIP": ["CWIP", 0],
                  "Investments": ["Investments", 0],
                  "Other Assets": ["Other_Assets", 0],
                  "Inventories": ["Inventories", 0],
                  "Trade receivables": ["Receivables", 0],
                  "Cash Equivalents": ["Cash", 0],
                  "Loans n Advances": ["Loans", 0],
                  "Other Assets etc": ["ETC_Assets", 0],
                  "Total Assets": ["Total_Assets", 0],
    }

    response = parseValues(BALANCE_SHEET, table_info, param_dict)

    response['title'] = table_info['title']
    response['head'] = sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][0]['head'], 0)

    response['5yr_Debt_CAGR'] = []
    response['Debt_Growth'] = []

    for idx in range(len(response['head'])):
        if (idx - 4) >= 0:
            response['5yr_Debt_CAGR'].append(round( (float((float(response['Borrowings'][idx] / response['Borrowings'][(idx-4)]) ** float(1/5))) - 1)*100, 2))
        if (idx - 1) >= 0:
            response['Debt_Growth'].append(growthCalculation(response['Borrowings'][idx], response['Borrowings'][idx-1]))
        else:
            response['Debt_Growth'].append(0)

    return response


def getDividend(table_info):
    response = {}
    param_dict = {
        "Dividend Payout %": ["Dividend_Payout", 1]
    }

    response = parseValues('Income Statement', table_info, param_dict)

    response['title'] = table_info['title']
    response['head'] = sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][0]['head'], 1)

    return response


def getRatios(table_info):

    response = {}

    response["title"] = table_info["title"]
    response['head'] = sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][0]['head'])

    response["Total_Equity"] = []
    response["Capital_Employed"] = []
    response["ROE"] = []
    response["ROCE"] = []
    response["ROA"] = []

    response["PBIT"] = []
    response["DOFL"] = []
    response["Debt_To_Equity"] = []
    response["ICR"] = []

    response['Share'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Share Capital']))
    response['Reserves'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Reserves']))
    response['PAT'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Net Profit']))
    response['Borrowings'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Borrowings']))

    response['PBT'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Profit before tax']))
    response['Interest'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Interest']))

    response['Total_Assets'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Total Assets']))

    response['PBT'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Profit before tax']))
    response['Depreciation'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['Depreciation']))

    for idx in range(len(response['head'])):
        response["Total_Equity"].append(response["Share"][idx] + response["Reserves"][idx])
        response["ROE"].append(round(float(response["PAT"][idx])/response["Total_Equity"][idx], 2)*100)

        response["Capital_Employed"].append(response["Total_Equity"][idx] + response["Borrowings"][idx])
        response["ROCE"].append(round(float(response["PAT"][idx]) / response["Capital_Employed"][idx], 2) * 100)

        response["PBIT"].append(response["PBT"][idx] + response["Interest"][idx])
        response["DOFL"].append(round(float(response["PBIT"][idx]) / response["PBT"][idx], 2))

        response["Debt_To_Equity"].append(round(float(response["Borrowings"][idx])/response["Total_Equity"][idx], 2))

        if response["Interest"][idx] != 0:
            response["ICR"].append(round(float(response["PBT"][idx] + response["Depreciation"][idx]) / response["Interest"][idx], 2))
        else:
            response["ICR"].append(5)

        if (idx - 1) >= 0:
            response["ROA"].append(round(float(
                response["PBIT"][idx]) / averageCalculation(response["Total_Assets"][idx], response["Total_Assets"][idx-1]), 4) * 100)
        else:
            response["ROA"].append(0)

    return response


def getPriceInfo(table_info):
    response = {}
    local = {}

    for key,val in table_info['price_info']["Time Series (Daily)"].items():

        #extract year and month from data
        extracted_year = key.strip()[0:4]
        extracted_month = int(key.strip()[5:7])

        if extracted_year not in response:
            # create entry for year in dictionary
            response[extracted_year] = []
            # create 12 lists representing each month for this year
            for month in range(12):
                empty_list = []
                response[extracted_year].append(empty_list)

        for year in range(2008, 2020):
            year_str = str(year)
            if year_str in extracted_year:
                temp = {}
                temp["price"] = float(val["5. adjusted close"].strip())
                temp["volume"] = float(val["6. volume"].strip())
                response[extracted_year][extracted_month-1].append(temp)
                break

    avgDict = getPriceAverage(response)
    quarterlyAvgDict = getQuarterlyPriceAverage(response)


    response['head'] = sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][0]['head'], 1)
    for idx in range(len(response['head'])):
        response['head'][idx] = response['head'][idx][4:8]

    local['EPS'] = cleanupComma(sliceList(INCOME_STATEMENT, table_info[INCOME_STATEMENT][1]['EPS in Rs']))

    response['Price_To_Earnings'] = []
    entries = 0
    total = 0
    for year, eps in zip(response['head'], local['EPS']):
        if year in avgDict:
            response['Price_To_Earnings'].append(round(avgDict[year]/float(eps), 2))
            total = total + response['Price_To_Earnings'][-1]
            entries = entries + 1
        else:
            response['Price_To_Earnings'].append(0)

    response['avg_PE'] = round(total / float(entries), 2)

    # calculate quarterly PE
    response["quarterlyPE"] = {}

    local['Equity'] = cleanupComma(sliceList(BALANCE_SHEET, table_info[BALANCE_SHEET][1]['Share Capital'], 0))
    local['PAT'] = cleanupComma(sliceList(QUARTER_STATEMENT, table_info[QUARTER_STATEMENT][1]['Net Profit'], 0))

    response['quarter_head'] = sliceList(QUARTER_STATEMENT, table_info[QUARTER_STATEMENT][0]['head'], 0)

    # Go over each quarter
    for idx in range(len(response['quarter_head'])):

        # figure out year for quarter
        quarter = response['quarter_head'][idx]
        quarters_year = quarter[4:8]
        quarters_month = quarter[0:3]

        if quarters_year not in response["quarterlyPE"]:
            response["quarterlyPE"][quarters_year] = {}
        fiscal_year = convertToFiscal(quarters_year)
        if fiscal_year not in response["quarterlyPE"]:
            response["quarterlyPE"][fiscal_year] = {}

        years_dict = quarterlyAvgDict[quarters_year]
        yr_idx = int(response['head'][-1]) - int(quarters_year)

        eps = round(local['PAT'][idx]/local['Equity'][yr_idx], 2) * float(table_info['Face Value'])

        if quarters_month == "Jun":
            Q1_avg = round(float(years_dict[4] + years_dict[5] + years_dict[6])/3, 2)
            response["quarterlyPE"][fiscal_year]['Q1'] = round(float(Q1_avg/eps), 2)
        elif quarters_month == "Sep":
            Q2_avg = round(float(years_dict[7] + years_dict[8] + years_dict[9]) / 3, 2)
            response["quarterlyPE"][fiscal_year]['Q2'] = round(float(Q2_avg / eps), 2)
        elif quarters_month == "Dec":
            Q3_avg = round(float(years_dict[10] + years_dict[11] + years_dict[12]) / 3, 2)
            response["quarterlyPE"][fiscal_year]['Q3'] = round(float(Q3_avg / eps), 2)
        elif quarters_month == "Mar":
            Q4_avg = round(float(years_dict[1] + years_dict[2] + years_dict[3]) / 3, 2)
            response["quarterlyPE"][quarters_year]['Q4'] = round(float(Q4_avg / eps), 2)
        else:
            print("ERROR: With parsing Month for Quarterly PE")

    return response


def convertToFiscal(year):
    return str(int(year)+1)


def getPriceAverage(dict):
    avgDict = {}

    for key, val in dict.items():

        # separate price data for this year in a list for further calculation
        years_price_list = []
        for monthdata in val:
            for item in monthdata:
                if item["price"] != 0:
                    years_price_list.append(item["price"])
        # now we have list of prices for one particular year

        # use following calculation to find average of all prices of a particular year
        length = len(years_price_list)
        if length > 0:
            avgDict[key] = round(sum(years_price_list) / float(length), 2)

    # now we have a dictionary of price average for each year {2008: 55}, {2009: 85}
    return avgDict


def getQuarterlyPriceAverage(dict):
    avgDict = {}

    for year, val in dict.items():

        # create a list of averages for each month for a particular year
        year_avg_price_list = [0] * 12

        for month in range(len(val)):
            monthdata = val[month]

            # separate price data for this month in a list for further calculation
            months_price_list = []

            for item in monthdata:
                if item["price"] != 0:
                    months_price_list.append(item["price"])

            # now we have list of prices for one particular month

            # use following calculation to find average of all prices of a particular month
            length = len(months_price_list)
            if length > 0:
                year_avg_price_list[month] = round(sum(months_price_list) / float(length), 2)
            else:
                year_avg_price_list[month] = 0

        # create a dictionary to hold monthly averages for this particular year
        avgDict[year] = {}
        # store each month's average into year's dictionary
        for month in range(len(year_avg_price_list)):
            avgDict[year][month+1] = year_avg_price_list[month]

    # now we have a dictionary of price average for each year {2008: 55}, {2009: 85}
    return avgDict

def parseValues(table_name, table_info, param_dict):
    response = {}

    for key, val in param_dict.items():
        if key in table_info[table_name][1]:
            if '%' not in key:
                response[val[0]] = cleanupComma(sliceList(table_name, table_info[table_name][1][key], val[1]))
            else:
                response[val[0]] = cleanupPercentage(sliceList(table_name, table_info[table_name][1][key], val[1]))
        else:
            response[val[0]] = [1] * SAMPLE_SIZE
    return response


def sliceList(table_name, dataList, TTM_element_size = 0):
    length = len(dataList) - TTM_element_size
    sample_size = SAMPLE_SIZE

    if table_name is "quarterlyPL":
        sample_size = LAST_EIGHT_QUARTERS

    if length > sample_size:
        return dataList[length-sample_size:length]
    else:
        return dataList[0:length]


def cleanupComma(dataList):
    for idx in range(len(dataList)):
        dataList[idx] = re.sub(',', '', dataList[idx])
        if dataList[idx] is not "":
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
    return float(round(((x - y) / y) * 100, 2))


def averageCalculation(num1, num2):
    return (num1 + num2) / 2.0

