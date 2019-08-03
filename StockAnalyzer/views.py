from django.shortcuts import render
from Utilities import ScreenerScrapper, InfoParser
from django import forms
import json


# Create your views here.
def home_view(request):
    if request.method == 'POST':
        print(request.POST['URL'])
        object = ScreenerScrapper.ScreenerScrapper(request.POST['URL'])
        object.scrapUsingSelenium()
        dict = {}
        dict = object.extractTables()
        object.printExtractedTable(dict)
        request.session['object'] = dict
    return render(request, 'home.html', locals())


def income_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getIncome(dict)

    return render(request, 'income.html', locals())


def quarter_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getQuarter(dict)

    return render(request, 'quarter.html', locals())


def cash_flow_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getCashFlow(dict)

    return render(request, 'cashflow.html', locals())


def balance_sheet_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getBalanceSheet(dict)

    return render(request, 'balancesheet.html', locals())


def dividend_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getDividend(dict)

    return render(request, 'dividend.html', locals())


def ratios_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = InfoParser.getRatios(dict)

    ROElist = zip(dict['head'], dict['ROE'], dict['ROCE'], dict['ROA'])
    DOFLlist = zip(dict['head'], dict['DOFL'])
    DElist = zip(dict['head'], dict['Debt_To_Equity'])

    return render(request, 'ratios.html', locals())
