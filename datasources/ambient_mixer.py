import os
import re
import requests
import untangle
from abc import ABC
from bs4 import BeautifulSoup

from common import download_file, make_filesafe
from config import config
from datasources.datasource_interface import DatasourceInterface
from models.channel import Channel
from models.environment import Environment

_XML_TEMPLATE_URL_PREFIX = "http://xml.ambient-mixer.com/audio-template?player=html5&id_template="
_ENVIRONMENT_ID_REGEX = re.compile(r"AmbientMixer.setup\(([0-9]+)\);")
_RANDOM_INTERVAL_MAP = {
    '1m': 60,
    '10m': 600,
    '1h': 3600
}

class AmbientMixer(DatasourceInterface, ABC):

    @staticmethod
    def is_valid_url(url):
        return re.match(r'https?://[a-zA-Z0-9_-]+\.ambient-mixer\.com/[a-zA-Z0-9_-]+', url)

    def load_environment(self):
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, 'html.parser')

        environment_id = _ENVIRONMENT_ID_REGEX.search(page).group(1)
        environment_name = soup.select('div.mixer_h2 > h2')[0].text
        environment_author = soup.select('div#mixer_details > div > a')[0].text

        attribution = f'Audio template by {environment_author} from https://www.ambient-mixer.com (Creative Commons Sampling Plus 1.0 License)'
        attribution += '\n' + soup.select('div#cc_license')[0].parent.nextSibling.nextSibling.nextSibling.text
        attribution = attribution.replace('\t\t\t\t\t\t', '\n')
        attribution = attribution.replace('\n\n', '\n')

        xml_template_url = _XML_TEMPLATE_URL_PREFIX + environment_id
        xml = requests.get(xml_template_url).text
        obj = untangle.parse(xml)

        channels = []
        for chan_num in range(1, 9):
            xml_channel = getattr(obj.audio_template, f"channel{chan_num}")
            self._download_channel_audio(xml_channel.url_audio.cdata)

            balance = (((int(xml_channel.balance.cdata) + 50) * 2.0) / 100) - 1.0  # Convert range from -50 to 50 to -1.0 to 1.0
            balance = round(balance, 2)

            channel = Channel(
                id=f'ambient-mixer_audio_{xml_channel.id_audio.cdata}',
                name=xml_channel.name_audio.cdata,
                filepath=self._get_audio_filepath_relative_to_audio_dir(xml_channel.url_audio.cdata),
                mute=(xml_channel.mute.cdata == 'true'),
                crossfade=(xml_channel.crossfade.cdata == 'true'),
                volume=int(xml_channel.volume.cdata),
                balance=balance,
                random=(xml_channel.random.cdata == 'true'),
                random_interval_count=int(xml_channel.random_counter.cdata),  # Only used if random is True
                random_interval_duration=_RANDOM_INTERVAL_MAP[xml_channel.random_unit.cdata],  # Only used if random is True
            )
            channels.append(channel)

        self.environment = Environment(
            id=f'{make_filesafe(environment_name)}_{environment_id}',
            name=environment_name,
            src_url=self.url,
            channels=channels,
            attribution=attribution,
        )

    def _download_channel_audio(self, url):
        relative_filepath = self._get_audio_filepath_relative_to_audio_dir(url)
        filepath = os.path.join(config['paths']['audio'], relative_filepath)
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            download_file(url, filepath)

    def _get_audio_filepath_relative_to_audio_dir(self, url):
        relative_path = url.split("xml.ambient-mixer.com/")[-1].replace("/", os.sep)
        return os.path.join('ambient-mixer', relative_path)
