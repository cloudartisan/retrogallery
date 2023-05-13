from urllib.parse import urlparse

import scrapy
from scrapy.crawler import CrawlerProcess

from retrogallery.items import ImageItem


class OldCrapGallerySpider(scrapy.Spider):
    name = "OldCrapGallerySpider"
    start_urls = [
        "https://oldcrap.org",
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
        for div in response.css("div.iksm-term--is-post"):
            gallery_url = div.css("a.iksm-term__link::attr(href)").get()
            gallery_title = div.css("span.iksm-term__text::text").get()
            if not gallery_url:
                continue
            if not gallery_title:
                # If we have a URL but not a title, we can try to get the
                # title from the URL using the last path component.
                p = urlparse(gallery_url)
                gallery_title = p.path.rsplit("/", 1)[-1]
            yield response.follow(gallery_url, self.parse_gallery, meta={
                "gallery_title": gallery_title,
                "gallery_url": gallery_url,
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
        gallery_title = response.meta['gallery_title']
        gallery_url = response.meta['gallery_url']
        for figure in response.css("figure.tiled-gallery__item"):
            image = ImageItem()
            image['gallery_title'] = gallery_title
            image['gallery_url'] = gallery_url
            # Defaults to the gallery title if there is no alt text or the alt
            # text is simply a default photo name (e.g., DSC_1234.jpg)
            image['image_title'] = figure.css("noscript img::attr(alt)").get()
            if (
                not image['image_title']
                or image['image_title'].startswith('DSC_')
                or image['image_title'].startswith('IMG_')'
                or image['image_title'].startswith('fullsizeoutput_')
            ):
                image['image_title'] = gallery_title
            image['image_urls'] = figure.css("img::attr(data-orig-file)").getall()
            # TODO srcset contains the same image in different sizes. Do we
            # want the different sizes, too? How do we store them? How do we
            # store their sizes? How do we differentiate different sizes of
            # the same image to avoid duplication?
            yield image