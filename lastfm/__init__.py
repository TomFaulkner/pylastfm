from lastfm.lastfm import Album, Artist, Track


__all__ = ['Track', 'Album', 'Artist']
__author__ = 'Tom Faulkner'
__version__ = '0.0.0'
__github__ = 'https://github.com/TomFaulkner'


def _read_api_key_from_file():
    """ Called from __init__.py to get api key """
    try:
        with open('lastfm_api_key.txt') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't read lastfm_api_key.txt")


lastfm.api_key = _read_api_key_from_file()
