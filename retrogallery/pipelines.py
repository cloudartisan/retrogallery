# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
from contextlib import suppress

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from itemadapter.adapter import ItemAdapter


class RetrogalleryPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        get_media_requests() is called for each item that needs to be
        downloaded, which might represent multiple images. The URLs of
        the images are contained in the item's image_urls field. Builds
        a scrapy.Request for each image_url and adds gallery title and
        image title metadata. Yields a Request, including metadata, for
        every URL in self.image_urls.
        """
        print("ITEM: ", item)
        images_urls = ItemAdapter(item).get(self.images_urls_field, [])
        for url in images_urls:
            request = scrapy.Request(url)
            request.meta['gallery_title'] = item['gallery_title']
            request.meta['image_title'] = item['image_title']
            yield request

    def process_item(self, item, spider):
        """
        process_item() is called for every item pipeline component. It
        accepts the item and spider and returns either the processed item,
        or raises a DropItem exception to discard the item.
        """
        adapter = ItemAdapter(item)
        adapter['spider'] = spider.name
        return super().process_item(item, spider)

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        file_path() is called for each image that is downloaded. It
        accepts the response and request and returns the path of the
        downloaded image relative to the IMAGES_STORE setting. The
        default implementation uses the request URL's path component
        as the filename. We override this method to construct a path
        based on the gallery title, image title, and image URL hash.
        """
        spider = self.spiderinfo.spider.name
        gallery_title = request.meta['gallery_title']
        if not gallery_title:
            raise DropItem("Missing gallery title")
        image_title = request.meta['image_title']
        if not image_title:
            raise DropItem("Missing image title")
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        return f"retrogallery/{spider}/{gallery_title}/{image_title}/{image_guid}.jpg"

    def item_completed(self, results, item, info):
        """
        item_completed() is called when an item has been downloaded. It
        accepts the download results and original item as parameters.
        Returns either a dict with data for a new item, or raises a DropItem
        exception to discard the item.

        Iterates over the results, extracting the the path field from every
        successful result. The list of image paths is added to the image_paths
        field of the item. 
        
        Finally, we return the item so that the next pipeline component can 
        process it.

        Parameters:
            results (list[tuple]): List of two-element tuples. Each tuple
            contains a boolean indicating whether a download succeeded
            or failed and either a dict about the downloaded image OR a
            Failure object.

            The dict about each download includes: url, path, checksum, and
            status. Status can be one of: 'cached', 'uptodate', 'downloaded'.

            The Failure object contains the exception that was raised when
            trying to download the image.

            Example:
            [
                (
                    True,
                    {
                        "checksum": "2b00042f7481c7b056c4b410d28f33cf",
                        "path": "full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg",
                        "url": "http://www.example.com/files/image1.jpg",
                        "status": "downloaded",
                    },
                ),
                (False, Failure(...)),
            ]

            item (Item): The scraped item. If an exception is raised in this
            method, the item will be dropped. Otherwise, it is returned after
            adding the successful results to the item.

            info (dict): Additional information about the item's processing
            containing the following keys:
                spider (Spider): The Spider object that scraped the item.
                downloader (Downloader): The Downloader instance that downloaded
                the item.
                crawler (Crawler): The Crawler object of this crawl.
                reason (str): The reason of the failure (available when status
                is 'failed').
        
        Returns:
            item (Item): The scraped item with image_paths added to it.
        """
        downloads = [x for ok, x in results if ok]
        if not downloads:
            raise DropItem("Item contains no images")
        with suppress(KeyError):
            ItemAdapter(item)[self.images_result_field] = downloads # type: ignore
        return item