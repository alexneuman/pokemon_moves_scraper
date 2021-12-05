import scrapy
from collections import defaultdict
import time

class PokemonspiderSpider(scrapy.Spider):
    name = 'pokemonspider'
    allowed_domains = ['serebii.net']

    def start_requests(self):
        urls = [f'https://www.serebii.net/pokedex/{str(n).zfill(3)}.shtml' for n in range(1, 152)]
        for i, url in enumerate(urls, start=1):
            yield scrapy.Request(url=url, cb_kwargs={'id': i}, callback=self.parse)

    def parse(self, response, id):
        # id = int(response.url.split('/')[-1].replace('.shtml', '').lstrip('0'))

        moves = defaultdict(list)
        for m in response.xpath('(.//table[@class="dextable"])[7]//a'):
            name = m.xpath('.//text()').get(),
            try:
                level = int(m.xpath('./../../td/text()').get())
            except:
                level = 0

            moves[level].append(*name)
        
        yield {
            int(id): dict(moves)
        }
