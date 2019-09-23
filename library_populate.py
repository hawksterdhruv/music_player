import os
import logging

from pprint import pprint
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from functools import reduce


class Library:
    def __init__(self):
        self.songs = []
        self.contents = []
    
    def get_list(self):
        return self.contents

    def add_new(self, path):
        # todo : what to do with --> album art
        # todo : what to do with --> Thumbs.db
        # todo : what to do with --> non mp3 files
        logging.debug(f"{path} : add_new() called")
        if not os.path.exists(path):
            print(f"{path} : does not exist")
            # logging.warning(f"{path} : does not exist")
            # return
        elif os.path.isfile(path):
            filename, file_extension = os.path.splitext(path)
            if file_extension == '.mp3':
                self.__newsong__(path)

        elif os.path.isdir(path):
            # print('came to isdir')
            for subpath in os.listdir(path):
                filepath = os.path.join(path, subpath)
                # print(filepath)
                if os.path.isfile(filepath):
                    filename, file_extension = os.path.splitext(filepath)
                    if file_extension in ['.mp3', '.m4a']:
                        self.__newsong__(filepath)
                elif os.path.isdir(filepath):
                    self.add_new(filepath)
        return

    def __newsong__(self, filepath):
        filename, file_extension = os.path.splitext(filepath)
        print(filepath)
        op = {}
        if file_extension == '.mp3':
            audio = MP3(filepath)
            k = dict(audio)
            # del k['data']
            # pprint(list(k.keys()))
            # pprint(k)
            pprint(audio.keys())
            pprint(audio.tags.getall('POPM'))
            op.update(Artists=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TPE1')]))
            op.update(Album=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TALB') +
                                                        audio.tags.getall('TOAL') +
                                                        audio.tags.getall('TPE1')])[0])
            pprint(audio.tags.getall('TPE2'))  # ALBUM ??
            pprint(audio.tags.getall('TPE3'))
            pprint(audio.tags.getall('TPE4'))
            print()
            pprint(audio.tags.getall('TIT1'))
            # pprint(audio.tags.getall('TIT2')) # NAME OF SONG
            op.update(Title=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TIT2')])[0])
            pprint(audio.tags.getall('TIT3'))
            print()
            pprint(audio.tags.getall('COMM'))
            print()
            pprint(audio.tags.getall('TALB'))  # ALBUM ??
            pprint(audio.tags.getall('TOAL'))  # ALBUM ??
            pprint(audio.tags.getall('TCON'))  # CONTENT TYPE
            pprint(audio.tags.getall('TCOM'))  # COMPOSER (seems to have music/lyrics)
            pprint(audio.tags.getall('TENC'))
            pprint(audio.tags.getall('TDRC'))
            # pprint()

            op.update(Duration=audio.info.length)
            # pprint(audio.info.bitrate)
            pprint(audio.info.__dict__)
            self.contents.append(op)
        elif file_extension == '.mp4':
            audio = MP4(filepath)
            k = dict(audio)
            # del k['data']
            # pprint(list(k.keys()))
            # pprint(k)
            pprint(audio.keys())
        print('-' * 100)


class Song:
    pass


class Playlist:
    pass


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    # logging.basicConfig(format=FORMAT,level=logging.DEBUG)
    l = Library()
    # l.add_new('/home/dhruv/Music/Music/new world order/Disturbed')
    # l.add_new('/home/dhruv/Music/Music/new world order/eminem/Eminem Collection/8 Mile Soundtrack')
    l.add_new('/home/dhruv/Music/Music/Aisha (2010) ~ 320 VBR')
