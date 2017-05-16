import json
from json import JSONDecodeError

import requests

uri = 'http://ws.audioscrobbler.com/2.0/'


def _build_url(method):
    api_key_and_format = f'&api_key={api_key}&format=json'
    return f'{uri}?method={method}{api_key_and_format}'


class Track:
    def __init__(self, mbid='c2786bd8-7dc7-4633-ab6c-70c70ebd432f',
                 artist=None, title=None, **kwargs):
        self._mbid = mbid
        self._artist = artist
        self._title = title

        self._data_dict = None

        self._load_from_file = kwargs.get('load_from_file', None)

        self._get_data()

    def __repr__(self):
        return f'{self.title}-{self.artist[0]}-{self.mbid}'

    def __str__(self):
        return f'{self.title} by {self.artist[0]}'

    @property
    def title(self):
        return self._data_dict['name']

    @property
    def mbid(self):
        return self._data_dict['mbid']

    @property
    def length(self):
        return int(self._data_dict['duration'])

    def __len__(self):
        return self.length

    @property
    def play_count(self):
        return self._data_dict['playcount']

    @property
    def listeners(self):
        return self._data_dict['listeners']

    @property
    def stats(self):
        return self.listeners, self.play_count

    @property
    def artist(self):
        return self._data_dict['artist']['name'],\
               self._data_dict['artist']['mbid'],\
               self._data_dict['artist']['url']

    @property
    def album(self):
        return self._data_dict['album']['artist'],\
               self._data_dict['album']['title'],\
               self._data_dict['album']['mbid'],\
               self._data_dict['album']['url']

    @property
    def summary(self):
        return self._data_dict['wiki']['summary']

    @property
    def content(self):
        return self._data_dict['wiki']['content']

    @property
    def genres(self):
        return [tag['name'] for tag in self._data_dict['toptags']['tag']]

    def _get_data(self):
        if not self._data_dict:
            if self._load_from_file:
                try:
                    with open(self._load_from_file) as f:
                        self._data_dict = json.load(f)['track']
                except FileNotFoundError:
                    raise FileNotFoundError("Track file does not exist")
                except JSONDecodeError:
                    raise JSONDecodeError("Invalid JSON data")
            else:
                r = requests.get(_build_url(f'track.getInfo&mbid={self._mbid}'))
                res = json.loads(r.text)
                self._data_dict = res['track']


class Artist:
    pass


class Album:
    pass
