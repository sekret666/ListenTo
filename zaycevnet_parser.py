import urllib.request
from bs4 import BeautifulSoup
from song import Song

class Parser:

    def get_song_list(self, page):
        data = BeautifulSoup(page, 'html.parser')
        song_list = []
        count = 0
        for link in data.find_all('h3', {'class': 'result__title'}):
            link = link.find('a')
            song = self.get_song(link)
            skip = False
            for audio in song_list:
                if song_list == 0:
                    break
                if song.title in audio['title']:
                    skip = True
                if audio['title'] in song.title:
                    skip = True
            if skip:
                continue
            song_list.append({
                'type': 'audio',
                'id': str(count),
                'performer': song.performer,
                'title': song.title,
                'audio_url': song.audio_url
            })
            count += 1
            if count == 5:
                break
        return song_list

    def get_song(self, link):
        url = link['href']
        page = self.get_html_page(url)
        performer = self.get_tag(page, 'div', 'musicset-track__artist').get_text()
        title = self.get_tag(page, 'div', 'musicset-track__track-name').get_text()
        audio_url = self.get_tag(page, 'div', 'audiotrack-button audiotrack-button_download').find('a')['href']
        return Song(performer, title, audio_url)

    def get_tag(self, page, tag_name, class_name):
        data = BeautifulSoup(page, 'html.parser')
        tag = data.find(tag_name, {'class': class_name})
        return tag

    def get_html_page(self, url):
        with urllib.request.urlopen(url) as response:
            return response.read()
