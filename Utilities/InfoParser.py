import re

SAMPLE_SIZE = 8


def getIncome(table_info):
    response = {}

    param_dict = {
        "Sales": "Sales",
        "Sales Growth %": "YoY_Growth",
        "Expenses": "Expenses",
        "Material Cost %": "Material_Cost",
        "Employee Cost %": "Employee_Cost",
        "Manufacturing Cost %": "Manufacturing_Cost",
        "Other Cost %": "Other_Cost",
        "Operating Profit": "Operating_Profit",
        "OPM %": "OPM",
        "Other Income": "Other_Income",
        "Interest": "Interest",
        "Depreciation": "Depreciation",
        "Profit before tax": "PBT",
        "Tax %": "Tax",
        "Net Profit": "PAT",
        "EPS in Rs": "EPS"
    }

    response = parseValues("Income Statement", table_info, param_dict, 1)

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
        "Sales": "Sales",
        "YOY Sales Growth %": "YoY_Growth",
        "Expenses": "Expenses",
        "Material Cost %": "Material_Cost",
        "Employee Cost %": "Employee_Cost",
        "Manufacturing Cost %": "Manufacturing_Cost",
        "Other Cost %": "Other_Cost",
        "Operating Profit": "Operating_Profit",
        "OPM %": "OPM",
        "Other Income": "Other_Income",
        "Interest": "Interest",
        "Depreciation": "Depreciation",
        "Profit before tax": "PBT",
        "Tax %": "Tax",
        "Net Profit": "PAT"
    }

    response = parseValues("quarterlyPL", table_info, param_dict, 0)

    response['Interest_to_Revenue'] = []
    response['Depreciation_to_Revenue'] = []

    response['Face_Value'] = 1
    response['Equity'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Share Capital'], 0))

    response['EPS'] = []
    response['EPS_Growth'] = []

    for idx in range(len(response['head'])):

        response['EPS'].append(round(response['PAT'][idx]/response['Equity'][idx], 2) * float(table_info['Face Value']))

        response['Interest_to_Revenue'].append(round(response['Interest'][idx]/response['Sales'][idx], 2) * 100)

        response['Depreciation_to_Revenue'].append(round(response['Depreciation'][idx] / response['Sales'][idx], 2) * 100)

    for idx in range(len(response['head'])):
        if (idx - 1) >= 0:
            response['EPS_Growth'].append(growthCalculation(response['EPS'][idx], response['EPS'][idx-1]))
        else:
            response['EPS_Growth'].append(0)

    return response


def getCashFlow(table_info):
    response = {}

    param_dict = {
        "Cash from Operating Activity": "CFO",
        "Profit from operations": "Profit_From_Ops",
        "Working Capital Changes": "WCC",
        "Taxes paid": "Taxes_paid",
        "Cash from Investing Activity": "CFI",
        "Fixed Assets Purchased": "Fixed_Assets_Purchased",
        "Fixed Assets Sold": "Fixed_Assets_Sold",
        "Investments purchased": "Investments_Purchased",
        "Investments sold": "Investments_Sold",
        "Cash from Financing Activity": "CFF",
        "Proceeds from Borrowings": "Proceeds_from_Borrowings",
        "Repayment of Borrowings": "Repayment_of_Borrowings",
        "Interest Paid": "Interest_Paid",
        "Dividends Paid": "Dividends_Paid",
        "Net Cash Flow": "Net_Cash_Flow"
    }

    response = parseValues('Cash Flow Statement', table_info, param_dict)

    response['CFO_Growth'] = []
    response['5yr_CFO_CAGR'] = []
    response['CFO_to_PAT'] = []
    response['CFPS'] = []

    response['PAT'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Net Profit']))
    response['Depreciation'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Depreciation'], 0))
    response['Face_Value'] = 1
    response['Equity'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Share Capital'], 0))

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
    param_dict = {"Share Capital": "Share",
                  "Equity Capital": "Equity",
                  "Reserves": "Reserves",
                  "Borrowings": "Borrowings",
                  "Other Liabilities": "Other_Liabilities",
                  "Trade Payables": "Payables",
                  "Total Liabilities": "Total_Liabilities",
                  "Fixed Assets": "Fixed_Assets",
                  "Gross Block": "Gross_Block",
                  "Accumulated Depreciation": "Acc_Depreciation",
                  "CWIP": "CWIP",
                  "Investments": "Investments",
                  "Other Assets": "Other_Assets",
                  "Inventories": "Inventories",
                  "Trade receivables": "Receivables",
                  "Cash Equivalents": "Cash",
                  "Loans n Advances": "Loans",
                  "Other Assets etc": "ETC_Assets",
                  "Total Assets": "Total_Assets"}

    response = parseValues('Balance Sheet', table_info, param_dict)

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
        "Dividend Payout %": "Dividend_Payout"
    }

    response = parseValues('Income Statement', table_info, param_dict)

    return response


def getRatios(table_info):

    response = {}

    response["title"] = table_info["title"]
    response['head'] = sliceList(table_info['Balance Sheet'][0]['head'])

    response["Total_Equity"] = []
    response["Capital_Employed"] = []
    response["ROE"] = []
    response["ROCE"] = []
    response["ROA"] = []

    response["PBIT"] = []
    response["DOFL"] = []
    response["Debt_To_Equity"] = []

    response['Share'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Share Capital']))
    response['Reserves'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Reserves']))
    response['PAT'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Net Profit']))
    response['Borrowings'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Borrowings']))

    response['PBT'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Profit before tax']))
    response['Interest'] = cleanupComma(sliceList(table_info['Income Statement'][1]['Interest']))

    response['Total_Assets'] = cleanupComma(sliceList(table_info['Balance Sheet'][1]['Total Assets']))

    for idx in range(len(response['head'])):
        response["Total_Equity"].append(response["Share"][idx] + response["Reserves"][idx])
        response["ROE"].append(round(float(response["PAT"][idx]/response["Total_Equity"][idx]), 2)*100)

        response["Capital_Employed"].append(response["Total_Equity"][idx] + response["Borrowings"][idx])
        response["ROCE"].append(round(float(response["PAT"][idx] / response["Capital_Employed"][idx]), 2) * 100)

        response["PBIT"].append(response["PBT"][idx] + response["Interest"][idx])
        response["DOFL"].append(round(float(response["PBIT"][idx] / response["PBT"][idx]), 2))

        response["Debt_To_Equity"].append(round(float(response["Borrowings"][idx])/response["Total_Equity"][idx], 2))

        if (idx - 1) >= 0:
            response["ROA"].append(round(float(
                response["PBIT"][idx] / averageCalculation(response["Total_Assets"][idx], response["Total_Assets"][idx-1])), 4) * 100)
        else:
            response["ROA"].append(0)

    return response


def parseValues(table_name, table_info, param_dict, TTM_element_size = 1):
    response = {}

    response['title'] = table_info['title']
    response['head'] = sliceList(table_info[table_name][0]['head'])

    for key, val in param_dict.items():
        if key in table_info[table_name][1]:
            if '%' not in key:
                response[val] = cleanupComma(sliceList(table_info[table_name][1][key], TTM_element_size))
            else:
                response[val] = cleanupPercentage(sliceList(table_info[table_name][1][key], TTM_element_size))
        else:
            response[val] = [1] * SAMPLE_SIZE
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
    return float(round(((x - y) / y) * 100, 2))


def averageCalculation(num1, num2):
    return (num1 + num2) / 2.0

