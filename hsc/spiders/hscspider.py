import scrapy
from urllib.parse import urlparse, urljoin  # Import the required methods

def is_relative_url(url):
    parsed_url = urlparse(url)
    return not all([parsed_url.scheme, parsed_url.netloc])

class HscspiderSpider(scrapy.Spider):
    name = "hscspider"
    allowed_domains = ["online.hsc.com.vn"]
    start_urls = ["https://online.hsc.com.vn"]

    def parse(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        if 'text' in content_type or 'html' in content_type or 'json' in content_type:
            yield {
                'url': response.url,
                'page_title': response.css('title::text').get(),
                'content': response.text  # This should be safe now
            }
            url = response.url
            links = response.css('a::attr(href)').getall()
            for link in links:
                if is_relative_url(link):
                    href = urljoin(url, link)
                else:
                    href = link
                
                parsed_url = urlparse(href)
                if parsed_url.scheme in ['http', 'https']:
                    yield response.follow(href, callback=self.parse)
        else:
            self.log(f"Skipping URL {response.url} due to unsupported Content-Type: {content_type}")

