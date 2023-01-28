import scrapy
from scrapy.selector import Selector

pages = ['revenue',
         'gross-profit',
         'net-income',
         'selling-general-administrative-expenses',
         'research-development-expenses',
         'total-depreciation-amortization-cash-flow']


class StockCrawler(scrapy.Spider):  # either scrapy.Spider or SrawlSpider

    name = 'stockSpider'

    allowed_domains = ['macrotrends.net']

    with open('/opt/stockAnalysis/data-scraping-and-fundamental-analysis/link.txt', 'r') as f:
        start_urls = f.readlines()

    def process_general(self, response, col_id, indicator):
        selector = Selector(text=response.body)
        col_path = '//*[@id="style-1"]/div[' + str(col_id) + ']/table/tbody'
        out = response.xpath(col_path)
        for row in out.css('tr'):
            r = []
            for td in row.css('td'):
                val = ''.join(td.xpath('.//text()').extract())
                self.logger.info("StockCrawler: val: %s ", val)
                if val == '' or val == '$':
                    val = '0'
                r.append(val)
            r.insert(0, (response.url).rsplit('/', 3)[-3])
            r.insert(0, (response.url).rsplit('/', 3)[-1])
            r[-1] = r[-1].replace('$', '')
            r[-1] = r[-1].replace(',', '')
            r = ','.join(r)
            r += "\n"
            with open('dump.txt', 'a') as f:
                f.writelines(r)

    def parse(self, response):
        print(response.url)
        indicator = (response.url).rsplit('/', 3)[-1]
        if indicator == 'total-depreciation-amortization-cash-flow':
            self.process_general(response, 2, indicator)
        if indicator in pages:
            self.process_general(response, 1, indicator)
