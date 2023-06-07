import os
import re
from urllib.parse import urlparse


def extract_image_urls(img):
    """
    Extracts the URLs from an img tag.

    Parameters:
        img (Response): The img tag to extract the URLs from.

    Returns:
        urls (list[str]): A list of URLs extracted from the img tag,
        including the URLs from the srcset attribute.
    """
    urls = img.css("::attr(src)").getall()
    urls.extend(extract_srcset(img))
    # Remove duplicate elements from urls list while preserving order.
    urls = list(dict.fromkeys(urls))
    return urls


def extract_srcset(img):
    """
    Extracts the URLs from the srcset attribute of an img tag.
    """
    # The srcset attribute contains the same image in different sizes
    srcset = img.css("::attr(srcset)").get()
    if not srcset:
        return []
    urls = re.findall(r'(https?://[^\s]+)', srcset)
    return urls


def extract_image_extension(url):
    """
    Extracts the image extension from a URL, stripping any query params
    and fragments.

    Parameters:
        url (str): The URL to extract the image extension from.

    Returns:
        image_ext (str): The image extension (including the .), or None if
        the image extension cannot be extracted.
    """
    url_without_params_or_fragments = urlparse(url)._replace(query='', fragment='').geturl()
    image_ext = os.path.splitext(url_without_params_or_fragments)[1]
    return image_ext


def extract_image_title(img, default=None):
    """
    Extracts the image title from an img tag. Defaults to the gallery title if
    there is no alt text or the alt text is simply a common photo name (e.g.,
    DSC_1234.jpg).

    Common prefixes for photo filenames (by no means a complete list):
        _DSCxxxx - Sony a6000
        _MG_xxxx - Canon EOS
        _XXXxxxx - Canon EOS
        DJI_xxxx - DJI Mavic 2 Pro
        DSC_xxxx - Sony, Nikon
        DSCxxxxx - Sony mirrorless and point and shoot / action models, Nikon 
                   depending on colour space used
        DSCFxxxx - Fuji
        DSCNxxxx - Nikon
        IMG_xxxx - Sony, Canon, Nikon, Olympus, Fuji, Panasonic, Samsung
        IMGPxxxx - Pentax
        Pxxxxxxx - Panasonic Lumix, Olymupus Tough
        SDCxxxxx - Samsung

    Parameters:
        img (Response): The img tag to extract the image title from.
        default (str): The default image title to use if the image title is
        not found.

    Returns:
        The image title, or the default if the image title is not found.
        If no default is provided, returns None.
    """
    image_title = img.css("::attr(alt)").get()
    if (not image_title
        or image_title.lower().startswith('_dsc')
        or image_title.lower().startswith('_mg')
        or image_title.lower().startswith('_xxx')
        or image_title.lower().startswith('dji_')
        or image_title.lower().startswith('dsc')
        or image_title.lower().startswith('dsc')
        or image_title.lower().startswith('img_')
        or image_title.lower().startswith('imgp')
        # regex match for P\d{7} or P\d{8} (Panasonic Lumix, Olympus Tough)
        or re.match(r'p\d{7,8}', image_title.lower())
        or image_title.lower().startswith('screenshot')
        or image_title.lower().startswith('fullsizeoutput')
        and default is not None
    ):
        image_title = default
    return image_title


def construct_image_title_from_url(url):
    return construct_title_from_url(url)


def construct_gallery_title_from_url(url):
    return construct_title_from_url(url)


def construct_title_from_url(url):
    """
    Constructs a gallery or image title from a URL. The title is the last
    component of the URL path, with any trailing slashes removed and query
    parameters removed. URL-encoded characters are decoded to their
    corresponding characters. Underscores and hyphens are replaced with
    spaces. Words are capitalised.

    Parameters:
        url (str): The URL to construct the title from.

    Returns:
        title (str): The title.
    """
    # Strip query params and fragments.
    url_without_params_or_fragments = urlparse(url)._replace(query='', fragment='').geturl()
    # Strip trailing slashes.
    url_without_params_or_fragments = url_without_params_or_fragments.rstrip('/')
    # Get the last component of the URL path.
    title = os.path.basename(url_without_params_or_fragments)
    # Replace underscores and hyphens with spaces.
    title = title.replace('_', ' ')
    title = title.replace('-', ' ')
    # Remove any leading or trailing whitespace.
    title = title.strip()
    # Remove any file extension.
    title = os.path.splitext(title)[0]
    # Capitalise the first letter of each word.
    title = title.title()
    return title