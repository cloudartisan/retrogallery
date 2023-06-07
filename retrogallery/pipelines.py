# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import logging
import os
from contextlib import suppress
from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import DropItem, NotConfigured
from scrapy.pipelines.images import ImagesPipeline
from itemadapter.adapter import ItemAdapter

from retrogallery import utils


class RetroGalleryLocalPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        # If we can find a RETROGALLERYLOCALPIPELINE_IMAGES_STORE setting,
        # use that, otherwise use the default store_uri
        if settings:
            store_uri = settings.get('RETROGALLERYLOCALPIPELINE_IMAGES_STORE', store_uri)
        super().__init__(
            store_uri=store_uri,
            download_func=download_func,
            settings=settings
        )

    def get_media_requests(self, item, info):
        """
        get_media_requests() is called for each item that needs to be
        downloaded, which might represent multiple images. The URLs of
        the images are contained in the item's image_urls field. Builds
        a scrapy.Request for each image_url and adds gallery title and
        image title metadata. Yields a Request, including metadata, for
        every URL in self.image_urls.
        """
        images_urls = ItemAdapter(item).get(self.images_urls_field, [])
        for url in images_urls:
            request = scrapy.Request(url)
            request.meta['gallery_title'] = item.get('gallery_title')
            request.meta['image_title'] = item.get('image_title')
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
        gallery_title = request.meta.get('gallery_title') or item.get('gallery_title')
        if not gallery_title:
            raise DropItem("Missing gallery title")
        image_title = request.meta.get('image_title') or item.get('image_title')
        if not image_title:
            raise DropItem("Missing image title")
        # deepcode ignore InsecureHash: <not used in a security context>
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        image_ext = utils.extract_image_extension(request.url)
        file_path = f"{spider}/{gallery_title}/{image_title}/{image_guid}{image_ext}"
        self.logger.debug(f"Saving {file_path}")
        return file_path

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
    

class RetroGalleryS3Pipeline(ImagesPipeline):
    """
    Uploads images to S3.
    """
    def __init__(self, store_uri, download_func=None, settings=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        # If we do not have AWS credentials, raise NotConfigured
        if (not settings or (
                not settings.get('AWS_ACCESS_KEY_ID') and
                not settings.get('AWS_SECRET_ACCESS_KEY')
            ) and not settings.get('AWS_SESSION_TOKEN')):
            raise NotConfigured("No AWS credentials found")
        # If we can find a RETROGALLERYS3PIPELINE_IMAGES_STORE setting,
        # use that, otherwise use the default store_uri
        if settings:
            store_uri = settings.get('RETROGALLERYS3PIPELINE_IMAGES_STORE', store_uri)
        super().__init__(
            store_uri=store_uri,
            download_func=download_func,
            settings=settings
        )
"""
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        gallery_title = adapter['gallery_title']
        image_title = adapter['image_title']
        images = adapter.get('images', [])
        for image in images:
            image_path = image['path']
            s3_path = f"retrogallery/{spider.name}/{gallery_title}/{image_title}/{image_path}"
            self.s3_client.upload_file(image_path, self.bucket_name, s3_path)
        return item
        """