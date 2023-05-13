import re


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