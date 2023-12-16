from urllib.parse import urlparse
import validators


def is_valid(url):
    """Valide url and return None or error message"""
    errors = []
    if url == '':
        errors.append('empty_url')
    if not len(url) < 255:
        errors.append('too_long')
    if not validators.url(url):
        errors.append('invalid_url')
    return errors


def normalize_url(url):
    parsed_url = urlparse(url)
    normal_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return normal_url
