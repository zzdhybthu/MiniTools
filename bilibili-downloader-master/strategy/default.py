from bs4 import BeautifulSoup
import httpx

import config
from strategy.bilibili_strategy import BilibiliStrategy
from models.video import Video

import re
import json


class DefaultStrategy(BilibiliStrategy):

    def __init__(self) -> None:
        super().__init__()
        self.session = httpx.Client()
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            "Content-Type": "application/json; charset=utf-8",
            'cookie': config.COOKIE,
            'pragma': 'no-cache',
            'referer': 'https://space.bilibili.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
        }

    def get_video_page(self, url: str) -> BeautifulSoup:
        response = self.session.get(
            url=url,
            headers=self.session.headers
        )

        response.raise_for_status()
        bs = BeautifulSoup(response.text, 'html.parser')

        return bs

    def get_video_title(self, bs: BeautifulSoup) -> str:
        video_title = bs.find('h1').get_text()
        video_title = video_title.replace('/', '-')
        print(video_title)

        return video_title

    def get_video_json(self, bs: BeautifulSoup) -> str:
        # 取视频链接
        pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
        script = bs.find("script", text=pattern)
        result = pattern.search(script.next).group(1)
        video_json = json.loads(result)

        return video_json

    def get(self, video: Video) -> Video:
        bs = self.get_video_page(video.url)
        title = self.get_video_title(bs)
        json = self.get_video_json(bs)

        # 这里默认获取最高画质
        quality_id = json['data']['dash']['video'][0]['id']
        video_url = json['data']['dash']['video'][0]['baseUrl']
        audio_url = json['data']['dash']['audio'][0]['baseUrl']

        video.set_title(title)
        video.set_quality(quality_id)
        video.set_video_url(video_url)
        video.set_audio_url(audio_url)

        return video
