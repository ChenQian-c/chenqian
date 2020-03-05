import requests
import easy_install
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
from io import BytesIO
url = 'https://www.qidian.com/all?'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

def get_font(url):
    response = requests.get(url)
    font = TTFont(BytesIO(response.content))
    cmap = font.getBestCmap()
    font.close()
    print(cmap)
    return cmap

def request(url):
    print(url)
    response = requests.get(url=url,headers=headers)
    return response
def parse(response):
    soup = BeautifulSoup(response.text,'lxml')
    li_list = soup.select('.all-img-list li')
    for li in li_list:
        title = li.select('h4')[0].get_text()
        author = ",".join([a.get_text() for a in li.select('.author a')])
        status = li.select('.author span')[0].get_text()
        intro = "".join([a.get_text().replace(" ","")for a in li.select('.intro')])
        src = li.select('.book-img-box img')[0].attrs['src']
        pattern = re.compile(r"<style>.*?font-family:(.*?);",re.S)
        font_urls = re.findall(pattern,response.text)
        font_full_url = 'https://qidian.gtimg.com/qd_anti_spider/' +font_urls[0].lstrip() + '.ttf'
        print(font_full_url)
        get_font(font_full_url)

        pattern1 = re.compile('<span.*?class="{}">(.*?)</span>'.format(font_urls[0].lstrip()),re.S)
        result = re.findall(pattern1,response.text)
        print(result)

def main():
    url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&'
    with ThreadPoolExecutor(max_workers=28) as executor:
        url_list = []
        for i in range(1,2):
            full_url = url + str(i)
            url_list.append(full_url)
        future = executor.map(request,url_list)
        for result in future:
            parse(result)


if __name__ == '__main__':
    main()