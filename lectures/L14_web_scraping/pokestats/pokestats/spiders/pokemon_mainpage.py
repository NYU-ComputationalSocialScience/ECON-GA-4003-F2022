import scrapy


class PokemonMainpageSpider(scrapy.Spider):
    name = 'pokemon_mainpage'
    allowed_domains = ['pokemondb.net']
    start_urls = ['https://pokemondb.net/']

    def parse(self, response):
        for type_page_link in response.css("a.type-icon::attr(href)").getall():
            next_page = response.urljoin(type_page_link)
            yield scrapy.Request(next_page, callback=self.parse_type_page)

    def parse_type_page(self, response):
        for pokemon_link in response.css("div.infocard span a.ent-name::attr(href)"):
            poke_page = response.urljoin(pokemon_link.get())
            yield scrapy.Request(poke_page, callback=self.parse_pokemon_page)

    def parse_pokemon_page(self, response):
        tbody = response.xpath('//div[div[@id="dex-stats"]]/div/table/tbody')
        for tr in tbody.xpath('.//tr'):
            start, min, max = tr.css("td.cell-num::text").getall()
            yield {
                "attribute": tr.css("th::text").get(),
                "start": start,
                "min": min,
                "max": max,
                "name": response.url.split("/")[-1],
            }
