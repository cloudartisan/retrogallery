import logging
import scrapy
from scrapy.crawler import CrawlerProcess

from retrogallery.items import ImageItem


logger = logging.getLogger(__name__)


class NostalgiaNerdGallerySpider(scrapy.Spider):
    """
    Crawls https://www.nostalgianerd.com/category/gallery
    """
    name = "NostalgiaNerdGallerySpider"
    start_urls = [
        'https://www.nostalgianerd.com/category/gallery',
    ]
    allowed_domains = [ 'nostalgianerd.com' ]

    def parse(self, response):
        """
        Follows links to gallery pages, which are identified as follows:
        <h3 class="preview-title"><a href="https://www.nostalgianerd.com/dragon-32/" title="Dragon 32">Dragon 32</a></h3>
        """
        for preview_title in response.css("h3.preview-title"):
            gallery_title = preview_title.css("a::attr(title)").get()
            gallery_url = preview_title.css("a::attr(href)").get()
            if not gallery_url:
                continue
            yield response.follow(gallery_url, self.parse_gallery, meta={
                'gallery_title': gallery_title,
                'gallery_url': gallery_url,
            })

    def parse_gallery(self, response):
        """
        Extracts image URLs from the gallery page, which are identified as follows:
        <div class="entry-content">
            <p><a href="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1.jpg"><img class="alignnone size-full wp-image-1029" src="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1.jpg" alt="Dragon 32" width="800" height="600" srcset="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1.jpg 800w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1-300x225.jpg 300w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1-768x576.jpg 768w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_1-600x450.jpg 600w" sizes="(max-width: 800px) 100vw, 800px" /></a></p>
            <p><a href="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2.jpg"><img class="alignnone size-full wp-image-1030" src="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2.jpg" alt="Dragon 32" width="800" height="600" srcset="https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2.jpg 800w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2-300x225.jpg 300w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2-768x576.jpg 768w, https://www.nostalgianerd.com/wp-content/uploads/2019/11/dragon32_2-600x450.jpg 600w" sizes="(max-width: 800px) 100vw, 800px" /></a></p>
            ...
        </div>
        """
        gallery_title = response.meta['gallery_title']
        gallery_url = response.meta['gallery_url']
        entry_content = response.css("div.entry-content")
        for img in entry_content.css("p a img"):
            image = ImageItem()
            image['gallery_title'] = gallery_title
            image['gallery_url'] = gallery_url
            # Defaults to the gallery title if there is no alt text or the alt
            # text is simply a default photo name (e.g., DSC_1234.jpg)
            image['image_title'] = img.css("::attr(alt)").get()
            if not image['image_title'] or image['image_title'].startswith('DSC_'):
                image['image_title'] = gallery_title
            image['image_urls'] = img.css("::attr(src)").getall()
            # TODO srcset contains the same image in different sizes. Do we
            # want the different sizes, too? How do we store them? How do we
            # store their sizes? How do we differentiate different sizes of
            # the same image to avoid duplication?
            yield image


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(NostalgiaNerdGallerySpider)
    process.start()