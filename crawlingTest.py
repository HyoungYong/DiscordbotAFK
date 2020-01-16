import requests
from bs4 import BeautifulSoup

def getHighlight():
    URL = "https://www.ubisoft.com/ko-kr/game/rainbow-six/siege/news-updates"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    highlight = {
        'title': '',
        'subtitle': '',
        'imgURL': '',
        'URL': '',
        'year': '',
        'month': '',
        'day': ''
    }

    # Main Title
    css = soup.select('div.updatesFeed__item__wrapper__content > h2')
    highlight['title'] = list(css)[0].text

    # Sub Title
    css = soup.select('div.updatesFeed__item__wrapper__content > p')
    highlight['subtitle'] = list(css)[0].text

    # imgURL
    css = soup.select('div.updatesFeed__item__wrapper__media > img')
    highlight['imgURL'] = list(css)[0].get('src')

    # URL
    css = soup.select('div.updatesFeed__items > a')
    highlight['URL'] = \
        'https://www.ubisoft.com' + \
        list(css)[0].get('href')

    # year
    css = soup.select('div.updatesFeed__item__wrapper__content > span > span.date__year')
    highlight['year'] = list(css)[0].text

    # month
    css = soup.select('div.updatesFeed__item__wrapper__content > span > span.date__month')
    highlight['month'] = list(css)[0].text

    # day
    css = soup.select('div.updatesFeed__item__wrapper__content > span > span.date__day')
    highlight['day'] = list(css)[0].text

    return highlight

print(getHighlight())