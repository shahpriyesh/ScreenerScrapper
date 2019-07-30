from django.shortcuts import render
from Utilities import ScreenerScrapper


# Create your views here.
def home_view(request):
    object = ScreenerScrapper.ScreenerScrapper("https://www.screener.in/company/MARUTI/consolidated/")
    object.scrapUsingSelenium()
    dict = {}
    dict = object.extractTables()
    object.printExtractedTable(dict)
    request.session['object'] = dict
    return render(request, 'home.html', locals())


def income_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = ScreenerScrapper.getIncome(dict)

    return render(request, 'income.html', locals())


def quarter_view(request):
    dict = {}
    dict = request.session.get('object')
    dict = ScreenerScrapper.getQuarter(dict)

    return render(request, 'quarter.html', locals())
