import scrapy
from scrapy.selector import Selector

pages = ['revenue',
         'gross-profit',
         'net-income',
         'selling-general-administrative-expenses',
         'research-development-expenses']


class Myspider2Spider(scrapy.Spider):  # either scrapy.Spider or SrawlSpider

    name = 'stockSpider'

    allowed_domains = ['macrotrends.net']

    with open('/Users/ad/PycharmProjects/StockAnalysis/link.txt', 'r') as f:
        start_urls = f.readlines()

    def process_general(self, response, indicator):
        selector = Selector(text=response.body)
        out = response.xpath('//*[@id="style-1"]/div[1]/table/tbody')
        for row in out.css('tr'):
            r = []
            for td in row.css('td'):
                val = ''.join(td.xpath('.//text()').extract())
                if val == '':
                    val = '?'
                r.append(val)
            r.insert(0, (response.url).rsplit('/', 3)[-3])
            r.insert(0, (response.url).rsplit('/', 3)[-1])
            r[-1] = r[-1].replace('$', '')
            r[-1] = r[-1].replace(',', '')
            r = ','.join(r)
            r += "\n"
            with open('dump.txt', 'a') as f:
                f.writelines(r)

    def process_column(self, response, col_id, indicator):
        selector = Selector(text=response.body)
        out = response.xpath('//*[@id="style-1"]/table/tbody')
        ticker = (response.url).rsplit('/', 3)[-3]
        for row in out.css('tr'):
            r = []
            for td in row.css('td'):
                val = ''.join(td.xpath('.//text()').extract())
                if val == '':
                    val = '?'
                r.append(val)
            # r = row.css('td::text').getall()
            r = [r[0], r[col_id]]
            r.insert(0, ticker)
            r.insert(0, indicator)
            r[-1] = r[-1].replace('$', '')
            r[-1] = r[-1].replace(',', '')
            r = ','.join(r)
            r += "\n"
            with open('dump.txt', 'a') as f:
                f.writelines(r)

    def parse(self, response):
        print(response.url)
        indicator = (response.url).rsplit('/', 3)[-1]
        if indicator == 'pe-ratio':
            self.process_column(response, 3, 'PE')
            self.process_column(response, 2, 'ttmNetEPS')
            self.process_column(response, 1, 'stockPrice')
        if indicator == 'price-sales':
            self.process_column(response, 3, 'PS')
            self.process_column(response, 2, 'ttmSalesPerShare')
        if indicator == 'price-book':
            self.process_column(response, 3, 'PB')
            self.process_column(response, 2, 'BVPS')
        if indicator == 'price-fcf':
            self.process_column(response, 3, 'PriceFCF')
            self.process_column(response, 2, 'ttmFCFps')
        if indicator == 'current-ratio':
            self.process_column(response, 3, 'CurrentRatio')
            self.process_column(response, 2, 'CurrentLiabilities')
            self.process_column(response, 1, 'CurrentAssets')
        if indicator == 'quick-ratio':
            self.process_column(response, 3, 'QuickRatio')
            self.process_column(response, 1, 'CurrentAssetsInventory')
        if indicator == 'debt-equity-ratio':
            self.process_column(response, 3, 'DE')
        if indicator == 'roe':
            self.process_column(response, 3, 'ROE')
            self.process_column(response, 1, 'ttmNetIncome')
        if indicator == 'roa':
            self.process_column(response, 3, 'ROA')
        if indicator == 'roi':
            self.process_column(response, 3, 'ROI')
            self.process_column(response, 2, 'LTinvestAndDebt')
        if indicator == 'return-on-tangible-equity':
            self.process_column(response, 3, 'RoTangibleEquity')
            self.process_column(response, 2, 'TangibleEquity')

        if indicator in pages:
            self.process_general(response, indicator)
