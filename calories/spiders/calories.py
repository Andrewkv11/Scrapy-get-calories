import scrapy


class QuotesSpider(scrapy.Spider):
    name = "calories"
    start_urls = [
        'https://calorizator.ru/product'
    ]

    def parse(self, response):
        for category in response.css('ul.product'):
            for sub_category in category.css('li'):
                sub_category_url = sub_category.css('a::attr(href)').get()
                yield response.follow(sub_category_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        category_name = response.xpath('//*[@id="page-title"]//text()').get()
        products = response.css('table.views-table tbody tr')
        for product in products:
            product_name = product.css('td.views-field-title a::text').get()
            product_proteins = product.css('td.views-field-field-protein-value::text').get().strip()
            product_fats = product.css('td.views-field-field-fat-value::text').get().strip()
            product_carbohydrates = product.css('td.views-field-field-carbohydrate-value::text').get().strip()
            product_kcal = product.css('td.views-field-field-kcal-value::text').get().strip()
            yield {
                'Наименование': product_name,
                'Белки': product_proteins,
                'Жиры': product_fats,
                'Углеводы': product_carbohydrates,
                'Ккал': product_kcal
            }