import scrapy

dictionary = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

class ThespiderSpider(scrapy.Spider):
    name = "thespider"
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        books = response.css("ol.row")
        for book in books:
            for b in book.css("article.product_pod"):
                data = {}
                data["title"] = b.css("h3 a::attr(title)").get()
                data["price"] = b.css("div.product_price p.price_color::text").get()
                data["stock"] = b.css("div.product_price p.instock.availability::text").getall()[1].strip()
                data["rating"] = b.css("p.star-rating::attr(class)").get().split()[-1]
                data["star"] = [v for k, v in dictionary.items() if k == data["rating"]][0]
                yield data
        
        # Pagination link
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
