from django.shortcuts import render
from Utilities import ScreenerScrapper, InfoParser
from django import forms
import json


# Create your views here.
def home_view(request):
    if request.method == 'POST':
        print(request.POST['URL'])
        print(request.POST['Ticker'])
        object = ScreenerScrapper.ScreenerScrapper(request.POST['URL'], request.POST['Ticker'])
        object.scrapUsingSelenium()
        price_info = {}
        price_info = object.getPriceInfo()
        dict = {}
        dict = object.extractTables()
        dict['price_info'] = price_info
        #object.printExtractedTable(dict)
        request.session['object'] = dict
    return render(request, 'home.html', locals())


def income_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getIncome(dict)

    EPSlist = zip(dict["head"], dict["EPS"])
    Saleslist = zip(dict["head"], dict["Sales"])
    Expenseslist = zip(dict["head"], dict["Expenses"])
    OPlist = zip(dict["head"], dict["Operating_Profit"])
    OIlist = zip(dict["head"], dict["Other_Income"])
    PBTlist = zip(dict["head"], dict["PBT"])
    PATlist = zip(dict["head"], dict["PAT"])
    Growthlist = zip(dict["head"], dict["YoY_Growth"], dict["EPS_Growth"], dict["Expenses_Growth"])
    CAGRlist = zip(dict["head"], dict["5yr_Sales_CAGR"], dict["5yr_PAT_CAGR"])
    Costlist = zip(dict["head"], dict["Material_Cost"], dict["Employee_Cost"], dict["Manufacturing_Cost"], dict["Other_Cost"])
    OPMlist = zip(dict["head"], dict["OPM"])
    NPMlist = zip(dict["head"], dict["NPM"])
    Interestlist = zip(dict["head"], dict["Interest"])
    InterestToRevenuelist = zip(dict["head"], dict["Interest_to_Revenue"])
    Depreciationlist = zip(dict["head"], dict["Depreciation"])
    DepreciationToRevenuelist = zip(dict["head"], dict["Depreciation_to_Revenue"])
    Taxlist = zip(dict["head"], dict["Tax"])

    return render(request, 'income.html', locals())


def quarter_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getQuarter(dict)

    EPSlist = zip(dict["head"], dict["EPS"])
    Growthlist = zip(dict["head"], dict["YoY_Growth"])
    Costlist = zip(dict["head"], dict["Material_Cost"], dict["Employee_Cost"], dict["Manufacturing_Cost"], dict["Other_Cost"])
    OPMlist = zip(dict["head"], dict["OPM"])
    NPMlist = zip(dict["head"], dict["NPM"])
    Interestlist = zip(dict["head"], dict["Interest"])
    InterestToRevenuelist = zip(dict["head"], dict["Interest_to_Revenue"])
    Depreciationlist = zip(dict["head"], dict["Depreciation"])
    DepreciationToRevenuelist = zip(dict["head"], dict["Depreciation_to_Revenue"])
    Taxlist = zip(dict["head"], dict["Tax"])

    return render(request, 'quarter.html', locals())


def cash_flow_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getCashFlow(dict)

    CFOlist = zip(dict["head"], dict["CFO"])
    CFIlist = zip(dict["head"], dict["CFI"])
    CFFlist = zip(dict["head"], dict["CFF"])
    CFPSlist = zip(dict["head"], dict["CFPS"])
    CFOGrowthlist = zip(dict["head"], dict["CFO_Growth"])
    CFOCAGRlist = zip(dict["head"], dict["5yr_CFO_CAGR"])
    CFOtoPATlist = zip(dict["head"], dict["CFO_to_PAT"])
    ProfitFromOpslist = zip(dict["head"], dict["Profit_From_Ops"])
    WCClist = zip(dict["head"], dict["WCC"])
    TPlist = zip(dict["head"], dict["Taxes_Paid"])
    FAPlist = zip(dict["head"], dict["Fixed_Assets_Purchased"])
    FASlist = zip(dict["head"], dict["Fixed_Assets_Sold"])
    IPlist = zip(dict["head"], dict["Investments_Purchased"])
    ISlist = zip(dict["head"], dict["Investments_Sold"])
    BorrowingsTakenlist = zip(dict["head"], dict["Proceeds_from_Borrowings"])
    BorrowingsRepaylist = zip(dict["head"], dict["Repayment_of_Borrowings"])
    InterestRepaylist = zip(dict["head"], dict["Interest_Paid"])
    DividendPaylist = zip(dict["head"], dict["Dividends_Paid"])
    NCFlist = zip(dict["head"], dict["Net_Cash_Flow"])

    return render(request, 'cashflow.html', locals())


def balance_sheet_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getBalanceSheet(dict)

    Equitylist = zip(dict["head"], dict["Equity"])
    Reserveslist = zip(dict["head"], dict["Reserves"])
    Borrowingslist = zip(dict["head"], dict["Borrowings"])
    DGlist = zip(dict["head"], dict["Debt_Growth"])
    DCAGRlist = zip(dict["head"], dict["5yr_Debt_CAGR"])
    OLlist = zip(dict["head"], dict["Other_Liabilities"])
    Payableslist = zip(dict["head"], dict["Payables"])
    TLlist = zip(dict["head"], dict["Total_Liabilities"])
    FAlist = zip(dict["head"], dict["Fixed_Assets"])
    Investmentslist = zip(dict["head"], dict["Investments"])
    OAlist = zip(dict["head"], dict["Other_Assets"])
    Inventorieslist = zip(dict["head"], dict["Inventories"])
    Receivableslist = zip(dict["head"], dict["Receivables"])
    Cashlist = zip(dict["head"], dict["Cash"])
    Loanslist = zip(dict["head"], dict["Loans"])
    Etclist = zip(dict["head"], dict["ETC_Assets"])
    TAlist = zip(dict["head"], dict["Total_Assets"])

    return render(request, 'balancesheet.html', locals())


def dividend_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getDividend(dict)

    DPlist = zip(dict["head"], dict["Dividend_Payout"])

    return render(request, 'dividend.html', locals())


def ratios_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getRatios(dict)

    ROElist = zip(dict['head'], dict['ROE'], dict['ROCE'], dict['ROA'])
    DOFLlist = zip(dict['head'], dict['DOFL'])
    DElist = zip(dict['head'], dict['Debt_To_Equity'])
    ICRlist = zip(dict['head'], dict['ICR'])

    return render(request, 'ratios.html', locals())


def price_view(request):
    dict = {}
    price_info = {}
    dict = request.session.get('object')
    dict = InfoParser.getPriceInfo(dict)

    PElist = zip(dict['head'], dict['Price_To_Earnings'])

    return render(request, 'price.html', locals())