import logging
from urllib.parse import urlparse

import scrapy
from scrapy.crawler import CrawlerProcess

from retrogallery import utils
from retrogallery.items import ImageItem


logger = logging.getLogger(__name__)


class OldCrapGallerySpider(scrapy.Spider):
    name = 'OldCrapGallerySpider'
    start_urls = [
        'https://oldcrap.org',
    ]
    allowed_domains = ["oldcrap.org"]

    def parse(self, response):
        """
        Example section that leads to a gallery page:

        <div class="iksm-term iksm-term--id-post-1449 iksm-term--child iksm-term--is-post" data-id="post-1449">
            <div class="iksm-term__inner" tabindex='0'>
                <a class="iksm-term__link" href='https://oldcrap.org/2018/02/21/texas-instruments-ti-99-4a/' target='_self' tabindex='-1'>
                    <div
                        class="iksm-term__shifts"
                        style="width:30px; min-width:30px; max-width:30px;"></div>
                    <div class="iksm-term__image-container">
                        <div
                            class="iksm-term__image"
                            style="background-image: url(https://i0.wp.com/oldcrap.org/wp-content/uploads/2018/02/fullsizeoutput_1662.jpeg?resize=150%2C150&ssl=1)"></div>
                    </div>
                    <span class="iksm-term__text">Texas Instruments TI-99/4A</span>
                </a>
            </div>
        </div>
        """
        for div in response.css('div.iksm-term--is-post'):
            gallery_url = div.css('a.iksm-term__link::attr(href)').get('').strip()
            # NOTE this is an interim title, we'll try to get a better one
            # from the gallery page.
            gallery_title = div.css('span.iksm-term__text::text').get('').strip()
            if not gallery_url:
                continue
            if not gallery_title:
                # If we have a URL but no title, we need to construct a
                # title from the URL
                gallery_title = utils.construct_gallery_title_from_url(gallery_url)
            yield response.follow(gallery_url, self.parse_gallery, meta={
                'gallery_title': gallery_title,
                'gallery_url': gallery_url,
            })
    
    def parse_gallery(self, response):
        """
        <figure class="tiled-gallery__item">
            <img data-attachment-id="914" data-permalink="https://oldcrap.org/2017/12/06/robotron-kc85-3/fullsizeoutput_134e/" data-orig-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=3249%2C1661&amp;ssl=1" data-orig-size="3249,1661" data-comments-opened="1" data-image-meta="{&quot;aperture&quot;:&quot;5.6&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;NIKON D80&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;1512585380&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;26&quot;,&quot;iso&quot;:&quot;400&quot;,&quot;shutter_speed&quot;:&quot;0.016666666666667&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;1&quot;}" data-image-title="fullsizeoutput_134e" data-image-description data-image-caption data-medium-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=300%2C153&amp;ssl=1" data-large-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=740%2C379&amp;ssl=1" decoding="async" alt data-height="1661" data-id="914" data-link="https://oldcrap.org/2017/12/06/robotron-kc85-3/fullsizeoutput_134e/" data-url="https://oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg" data-width="3249" src="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?ssl=1" data-amp-layout="responsive" data-lazy-srcset="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=600&#038;ssl=1 600w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=900&#038;ssl=1 900w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1200&#038;ssl=1 1200w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1500&#038;ssl=1 1500w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1800&#038;ssl=1 1800w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=2000&#038;ssl=1 2000w" data-lazy-src="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?ssl=1&amp;is-pending-load=1" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" class=" jetpack-lazy-image">
            <noscript>
                <img data-lazy-fallback="1" data-attachment-id="914" data-permalink="https://oldcrap.org/2017/12/06/robotron-kc85-3/fullsizeoutput_134e/" data-orig-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=3249%2C1661&amp;ssl=1" data-orig-size="3249,1661" data-comments-opened="1" data-image-meta="{&quot;aperture&quot;:&quot;5.6&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;NIKON D80&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;1512585380&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;26&quot;,&quot;iso&quot;:&quot;400&quot;,&quot;shutter_speed&quot;:&quot;0.016666666666667&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;1&quot;}" data-image-title="fullsizeoutput_134e" data-image-description="" data-image-caption="" data-medium-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=300%2C153&amp;ssl=1" data-large-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=740%2C379&amp;ssl=1" decoding="async" data-attachment-id="914" data-permalink="https://oldcrap.org/2017/12/06/robotron-kc85-3/fullsizeoutput_134e/" data-orig-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=3249%2C1661&amp;ssl=1" data-orig-size="3249,1661" data-comments-opened="1" data-image-meta="{&quot;aperture&quot;:&quot;5.6&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;NIKON D80&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;1512585380&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;26&quot;,&quot;iso&quot;:&quot;400&quot;,&quot;shutter_speed&quot;:&quot;0.016666666666667&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;1&quot;}" data-image-title="fullsizeoutput_134e" data-image-description="" data-image-caption="" data-medium-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=300%2C153&amp;ssl=1" data-large-file="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e.jpeg?fit=740%2C379&amp;ssl=1" srcset="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=600&#038;ssl=1 600w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=900&#038;ssl=1 900w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1200&#038;ssl=1 1200w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1500&#038;ssl=1 1500w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=1800&#038;ssl=1 1800w,https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?strip=info&#038;w=2000&#038;ssl=1 2000w" alt="" data-height="1661" data-id="914" data-link="https://oldcrap.org/2017/12/06/robotron-kc85-3/fullsizeoutput_134e/" data-url="https://oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg" data-width="3249" src="https://i0.wp.com/oldcrap.org/wp-content/uploads/2017/12/fullsizeoutput_134e-1024x524.jpeg?ssl=1" data-amp-layout="responsive" />
            </noscript>
        </figure>
        """
        # If the gallery page has a better title available, use it, otherwise
        # use the gallery title obtained from the linking/previous page.
        # There are a couple of options available:
        # - <h1 class="entry-title">Apple ///</h1>
        #   response.css('h1.entry-title::text').get()
        #   "Apple ///"
        # - <meta property="article:section" content="Apple III" />
        #   response.css("meta[property='article:section']::attr(content)").get()
        #   "Apple III"
        gallery_title = response.css('h1.entry-title::text').get(response.meta['gallery_title'])
        gallery_url = response.meta['gallery_url']

        carousels = response.xpath('//div[@data-carousel-extra]')
        for carousel in carousels:
            image = ImageItem()
            image['gallery_title'] = gallery_title
            image['gallery_url'] = gallery_url
            # TODO srcset contains the same image in different sizes. Do
            # we want the different sizes, too? How do we store them? How
            # do we store their sizes? How do we differentiate different
            # sizes of the same image to avoid duplication?
            image['image_urls'] = carousel.css("noscript img::attr(data-orig-file)").getall()

            # Get the immediately preceding heading element, if any.
            heading = carousel.xpath('preceding-sibling::*[self::h1 or self::h2 or self::h3][1]')
            heading_text = heading.xpath('string()').get('').strip() if heading else ''

            # Get the preceding parent heading element, if any.
            if heading and heading.xpath('self::h3'):
                parent_heading = carousel.xpath('preceding-sibling::*[self::h2][1]')
            elif heading and heading.xpath('self::h2'):
                parent_heading = carousel.xpath('preceding-sibling::*[self::h1][1]')
            else:
                parent_heading = None
            parent_heading_text = parent_heading.xpath('string()').get('').strip() if parent_heading else ''

            # Get the preceding grandparent heading element, if any.
            if parent_heading and parent_heading.xpath('self::h2'):
                grandparent_heading = carousel.xpath('preceding-sibling::*[self::h1][1]')
            else:
                grandparent_heading = None
            grandparent_heading_text = grandparent_heading.xpath('string()').get('').strip() if grandparent_heading else ''

            # Use the immediately preceding heading/subheading elements as the
            # image title, since most of the images do not provide alt text
            image['image_title'] = ' '.join([
                grandparent_heading_text,
                parent_heading_text,
                heading_text,
            ]).strip()

            # If we STILL don't have an image title, extract what we can from
            # the img tag
            if not image['image_title']:
                img = carousel.css("noscript img")
                image['image_title'] = utils.extract_image_title(img, default=gallery_title)

            yield image