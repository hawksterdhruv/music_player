import threading

import audiotools.player
import audiotools
import os
import logging
import webview
from pprint import pprint
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from functools import reduce
import json
from pprint import pprint
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///music.db')
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


def get_or_create(sess, model, **kwargs):
    instance = sess.query(model).filter_by(**kwargs).first()

    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        sess.add(instance)
        return instance, True


class PlayerApi:
    def play(self):
        # audiotools.player.available_outputs()
        audio_file = audiotools.open('/home/dhruv/Music/Music/Aisha (2010) ~ 320 VBR/04 - Behke Behke [DoReGaMa].mp3')

        audio_output = audiotools.player.open_output('ALSA')
        replay_gain = audiotools.player.RG_NO_REPLAYGAIN

        player = audiotools.player.Player(audio_output, replay_gain)

        player.open(audio_file)
        player.play()


class LibraryApi:
    contents = []

    def __init__(self):
        self.songs = []
        # contents = []

    @classmethod
    def get_list(cls, params):
        session.query(models.Song)
        return json.dumps(cls.contents).replace("'", "`")
        # return cls.contents

    @classmethod
    def add_new_button(cls, params):
        window = webview.create_window('Open file dialog example')
        print(window.uid)
        path = window.create_file_dialog(webview.FOLDER_DIALOG)
        # window.destroy()

        if len(path) > 0:
            # cls.add_new(params, path=path[0])
            t = threading.Thread(target=cls.add_new, args=(params,), kwargs={'path': path[0]}, daemon=True)
            t.start()
        else:
            return

    @classmethod
    def add_new(cls, params, path=''):

        print(f"{path} : add_new() called")
        # todo : what to do with --> album art
        # todo : what to do with --> Thumbs.db
        # todo : what to do with --> non mp3 files
        logging.debug(f"{path} : add_new() called")
        if not path:
            return
        if not os.path.exists(path):
            print(f"{path} : does not exist")
            # logging.warning(f"{path} : does not exist")
            # return
        elif os.path.isfile(path):
            filename, file_extension = os.path.splitext(path)
            if file_extension == '.mp3':
                temp = cls.__newsong__(path)
                al = get_or_create(session, models.Album, name=temp['Album'])
                ar_list = [get_or_create(session, models.Artist, name=artist_name) for artist_name in
                           temp['Artists']]
                gen = get_or_create(session, models.Genre, name=temp['Genre'])
                song = get_or_create(session, models.Song,
                                     title=temp['Title'],
                                     filepath=temp['Filepath'],
                                     duration=temp['Duration'],
                                     album=al,
                                     genre=gen)
                song.artists = ar_list
                # session.add(song)
                session.commit()

        elif os.path.isdir(path):
            # print('came to isdir')
            for subpath in os.listdir(path):
                filepath = os.path.join(path, subpath)
                # print(filepath)
                if os.path.isfile(filepath):
                    filename, file_extension = os.path.splitext(filepath)
                    if file_extension in ['.mp3', '.m4a']:
                        temp = cls.__newsong__(filepath)
                        # pprint(temp)
                        al, _ = get_or_create(session, models.Album, name=temp['Album'])
                        # pprint(al)
                        ar_list = [artist_block[0] for artist_block in
                                   [get_or_create(session, models.Artist, name=artist_name) for artist_name in
                                    temp['Artists']]]
                        # pprint(ar_list)
                        gen, _ = get_or_create(session, models.Genre, name=temp['Genre'])
                        # pprint(gen)
                        song, new = get_or_create(session, models.Song,
                                                  title=temp['Title'],
                                                  filepath=temp['Filepath'],
                                                  duration=temp['Duration'],
                                                  album=al,
                                                  genre=gen)
                        # pprint(song)
                        song.artists = ar_list
                        # if not song:
                        if new:
                            # session.add(song)
                            session.commit()
                elif os.path.isdir(filepath):
                    cls.add_new(params, path=filepath)
        return

    @classmethod
    def __newsong__(cls, filepath):
        filename, file_extension = os.path.splitext(filepath)
        print(filepath)
        op = {}
        if file_extension == '.mp3':
            audio = MP3(filepath)
            k = dict(audio)
            op.update(Filepath=filepath)
            # del k['data']
            # pprint(list(k.keys()))
            # pprint(k)
            # pprint(audio.keys())
            # pprint(audio.tags.getall('POPM'))
            op.update(Artists=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TPE1')]))
            op.update(Album=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TALB')])[0])
            # pprint(audio.tags.getall('TPE2'))  # ALBUM ??
            # pprint(audio.tags.getall('TPE3'))
            # pprint(audio.tags.getall('TPE4'))
            # print()
            # pprint(audio.tags.getall('TIT1'))
            # pprint(audio.tags.getall('TIT2')) # NAME OF SONG
            op.update(Title=reduce(lambda x, y: x + y, [a.text for a in audio.tags.getall('TIT2')])[0])
            genre = [a.text for a in audio.tags.getall('TCON')]
            if genre:
                op.update(Genre=reduce(lambda x, y: x + y, genre)[0])
            else:
                op.update(Genre=None)
            # pprint(audio.tags.getall('TIT3'))
            # print()
            # pprint(audio.tags.getall('COMM'))
            # print()
            # pprint(audio.tags.getall('TALB'))  # ALBUM ??
            # pprint(audio.tags.getall('TOAL'))  # ALBUM ??
            # pprint(audio.tags.getall('TCON'))  # CONTENT TYPE
            # pprint(audio.tags.getall('TCOM'))  # COMPOSER (seems to have music/lyrics)
            # pprint(audio.tags.getall('TENC'))
            # pprint(audio.tags.getall('TDRC'))
            # pprint()

            op.update(Duration=audio.info.length)
            # pprint(audio.info.bitrate)
            # pprint(audio.info.__dict__)
            # self.contents.append(op)
        elif file_extension == '.mp4':
            audio = MP4(filepath)
            k = dict(audio)
            # del k['data']
            # pprint(list(k.keys()))
            # pprint(k)
            # pprint(audio.keys())
        # print('-' * 100)
        return op
