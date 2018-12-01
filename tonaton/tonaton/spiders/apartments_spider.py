import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"

    start_urls = [
        'https://tonaton.com/en/ads/accra/apartments?sort=date_desc&by_paying_member=0&type=for_rent&filters%5B0%5D%5Btype%5D=money&filters%5B0%5D%5Bkey%5D=price&filters%5B0%5D%5Bmin%5D=36&filters%5B0%5D%5Bmax%5D=50000&filters%5B0%5D%5Bminimum%5D=&filters%5B0%5D%5Bmaximum%5D=720&filters%5B1%5D%5Btype%5D=numeric&filters%5B1%5D%5Bkey%5D=size&filters%5B1%5D%5Bmin%5D=1&filters%5B1%5D%5Bmax%5D=75347.3&filters%5B1%5D%5Bminimum%5D=&filters%5B1%5D%5Bmaximum%5D=&filters%5B2%5D%5Btype%5D=enum&filters%5B2%5D%5Bkey%5D=bedrooms&filters%5B2%5D%5Bvalues%5D%5B%5D=2&filters%5B2%5D%5Bvalues%5D%5B%5D=3&filters%5B2%5D%5Bvalues%5D%5B%5D=4&filters%5B2%5D%5Bvalues%5D%5B%5D=5&filters%5B2%5D%5Bvalues%5D%5B%5D=6&filters%5B2%5D%5Bvalues%5D%5B%5D=7&filters%5B2%5D%5Bvalues%5D%5B%5D=8&filters%5B2%5D%5Bvalues%5D%5B%5D=9&filters%5B2%5D%5Bvalues%5D%5B%5D=10&filters%5B2%5D%5Bvalues%5D%5B%5D=10%2B&filters%5B3%5D%5Btype%5D=enum&filters%5B3%5D%5Bkey%5D=bathrooms',
        'https://tonaton.com/en/ads/accra/houses?sort=date_desc&by_paying_member=0&type=for_rent&filters%5B0%5D%5Btype%5D=money&filters%5B0%5D%5Bkey%5D=price&filters%5B0%5D%5Bmin%5D=100&filters%5B0%5D%5Bmax%5D=69000&filters%5B0%5D%5Bminimum%5D=&filters%5B0%5D%5Bmaximum%5D=720&filters%5B1%5D%5Btype%5D=enum&filters%5B1%5D%5Bkey%5D=bedrooms&filters%5B1%5D%5Bvalues%5D%5B%5D=2&filters%5B1%5D%5Bvalues%5D%5B%5D=3&filters%5B1%5D%5Bvalues%5D%5B%5D=4&filters%5B1%5D%5Bvalues%5D%5B%5D=5&filters%5B1%5D%5Bvalues%5D%5B%5D=6&filters%5B1%5D%5Bvalues%5D%5B%5D=7&filters%5B1%5D%5Bvalues%5D%5B%5D=8&filters%5B1%5D%5Bvalues%5D%5B%5D=9&filters%5B1%5D%5Bvalues%5D%5B%5D=10&filters%5B1%5D%5Bvalues%5D%5B%5D=10%2B&filters%5B2%5D%5Btype%5D=enum&filters%5B2%5D%5Bkey%5D=bathrooms'
    ]

    def parse(self, response):
        # follow links to apartment pages
        for href in response.css('.ui-item .item-title::attr(href)'):
            yield response.follow(href, self.parse_apartment)

        # follow pagination links
        for href in response.css('div.ui-pagination a.pag-next::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_apartment(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        images = response.css('.gallery-items .gallery-item img[data-indicator="data-indicator"]::attr(data-srcset)').extract()
        images = [image.split(' ')[0] for image in images]

        yield {
            'url': response.request.url,
            'title': response.css('.item-top h1::text').extract_first().strip(),
            'price': response.css('.item-price .amount::text').extract_first().strip(),
            'images': images,

            'description': response.css('.item-description').extract_first(),
            'contacts': response.css('.item-contact-more span.h3::text').extract_first().strip(),

            'street_or_landmark': response.css(
                '.item-properties dt:contains("Street / Landmark:") + dd::text').extract_first(),
            'size': response.css('.item-properties dt:contains("Size:") + dd::text').extract_first(),
            'beds': response.css('.item-properties dt:contains("Beds:") + dd::text').extract_first(),
            'baths': response.css('.item-properties dt:contains("Baths:") + dd::text').extract_first(),

            'date': response.css('p.item-intro span.date::text').extract_first(),
            'location': response.css('p.item-intro span.location::text').extract_first(),
            'poster': response.css('p.item-intro span.poster a::text').extract_first()
        }
