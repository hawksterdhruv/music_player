import sys
import threading

import audiotools.player
import audiotools

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QModelIndex, QEventLoop, pyqtSlot, pyqtSignal, QThread, \
    QObject, QSortFilterProxyModel, QRegExp

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from application_api import LibraryApi
from library_ui import Ui_Dialog as Library_ui_dialog
from player_ui import Ui_MainWindow as Player_ui_mainwindow
from playlist_ui import Ui_Dialog as Playlist_ui_dialog
import time


class SongsAbstractModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent=None, *args)
        self.headers = []
        self.songdata = datain
        # if len(datain) == 0:
        #     self.emptyFlag = True
        # else:
        #     self.emptyFlag = False

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.songdata)

    def columnCount(self, parent=None, *args, **kwargs):
        if len(self.songdata) == 0:
            return 0
        return len(self.songdata[0])

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return list(self.songdata[QModelIndex.row()].values())[QModelIndex.column()]

    def headerData(self, p_int, Qt_Orientation, role=None):
        # todo: resize columns
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            # print(list(self.songdata[0].keys())[p_int])
            return list(self.songdata[0].keys())[p_int]

    def insertRows(self, index, count, parent=None, *args, **kwargs):
        self.beginInsertRows(parent, index, index + count - 1)
        # self.songdata.insert(index, kwargs['data'])
        self.endInsertRows()

        return True


class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}
        self.searchText = None
        self.col_indexes = None

    def setSearchText(self, arg=None):
        self.searchText = arg
        self.beginResetModel()
        self.endResetModel()

    def setColIndexes(self, col_indexes):
        self.col_indexes = col_indexes

    # def setFilterByColumn(self, regex, column):
    #     self.filters[column] = regex
    #     self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):

        indices = [self.sourceModel().index(source_row, index, source_parent) for index in self.col_indexes]

        if self.searchText:
            for index in indices:
                if index.data() and self.searchText.lower() in index.data().lower():
                    return True
            else:
                return False
        else:
            return True


# class Timer(QObject):
#     def __init__(self,timer_label,player,duration):
#         super(Timer,self).__init__()
#         self.timer_label = timer_label
#         self.player = player
#         self.duration = duration
# 
#         self.playing_signal.connect(self.update_timer)
# 
#     playing_signal = pyqtSignal(int,int)
# 
#     @pyqtSlot(int,int)
#     def update_timer(self,int1,int2):
#         # for i in range(10):
#         #     time.sleep(1)
#         while True:
#             # while self.player.status() == audiotools.player.PLAYER_PLAYING:
#             print(self.player.progress()[0])
#             t = self.duration*self.player.progress()[0]/self.player.progress()[0]
#             self.timer_label.setText(f'{t}:.2f')
#             time.sleep(0.5)

def update_timer_seek(timer_label, seek, player, duration):
    # t = duration * player.progress()[0] / player.progress()[1]
    # timer_label.setText('{}:{}'.format(int(t // 60), int(t % 60)))
    # for i in range(10):
    #     time.sleep(1)
    # while True:
    while player.state() == audiotools.player.PLAYER_PLAYING:
        percentage = player.progress()[0] / player.progress()[1]
        seek.setValue(int(percentage * 100))
        t = duration * percentage
        # print(t)
        timer_label.setText('{:02}:{:02}'.format(int(t // 60), int(t % 60)))
        time.sleep(0.5)
    print('exited')


class PlayerMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Player_ui_mainwindow()
        self.ui.setupUi(self)

        self.library_dialog = LibraryDialog()
        self.playlist_dialog = PlalistDialog()

        with open('darktheme.css') as file_in:
            css = file_in.read()
            self.setStyleSheet(css)
            self.playlist_dialog.setStyleSheet(css)
            self.library_dialog.setStyleSheet(css)

        self.library_dialog.setFather(self)
        self.playlist_dialog.setFather(self)

        audio_output = audiotools.player.open_output('ALSA')
        replay_gain = audiotools.player.RG_NO_REPLAYGAIN
        self.player = audiotools.player.Player(audio_output, replay_gain)

        self.ui.medialibrary_button.clicked.connect(self.toggle_library)
        self.ui.playlist_button.clicked.connect(self.toggle_playlist)
        self.ui.play_button.clicked.connect(self.play_song)
        self.ui.pause_button.clicked.connect(self.pause_song)
        self.ui.stop_button.clicked.connect(self.stop_song)
        self.ui.volume.sliderReleased.connect(self.change_volume)
        # self.ui.volume.sliderPressed.connect(self.change_volume)
        # self.ui.volume.sliderMoved.connect(self.change_volume)
        # self.ui.volume.mouseReleaseEvent.connect(self.change_volume)
        self.ui.volume.valueChanged.connect(self.change_volume)
        self.ui.timer_label.setText('00:00')

    def toggle_playlist(self):
        if self.playlist_dialog.isHidden():
            self.playlist_dialog.show()
        else:
            self.playlist_dialog.hide()

    def toggle_library(self):
        if self.library_dialog.isHidden():
            self.library_dialog.show()
        else:
            self.library_dialog.hide()

    def play_song(self, song=None):
        if song:
            audio_file = audiotools.open(song['filepath'])
            self.player.open(audio_file)

        self.player.play()
        time.sleep(0.1)
        self.thread = threading.Thread(target=update_timer_seek,
                                       args=(self.ui.timer_label, self.ui.seek, self.player, song['duration']))
        self.thread.start()

        print(f'playing {song.get("filepath")}' if song else '')

    def pause_song(self):
        if self.player:
            self.player.pause()

    def stop_song(self):
        if self.player:
            self.player.stop()

    def change_volume(self):
        if not self.ui.volume.isSliderDown():
            # print(self.ui.volume.value())
            self.player.set_volume(self.ui.volume.value() / 100)


class LibraryDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Library_ui_dialog()
        self.ui.setupUi(self)
        self.songs = None
        self.albums = None
        self.artists = None

        self.ui.library_button.clicked.connect(self.add_new)
        self.ui.songs.doubleClicked.connect(self.enqueue_song)

        self.engine = create_engine('sqlite:///music.db')
        models.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        # self.populate_songs()
        songs_data = [{'title': a.title,
                       'album': a.album.name,
                       'duration': a.duration,
                       'artists': ','.join([b.name for b in a.artists]),
                       'playcount': a.playcount,
                       'genre': a.genre.name,
                       'filepath': a.filepath,
                       'id': a.id} for a in self.session.query(models.Song).all()]
        albums_data = [{'name': a.name,
                        'track_count': len(a.songs),
                        'year': ''} for a in self.session.query(models.Album).all()]
        artists_data = [{'name': a.name,
                         'track_count': len(a.songs),
                         'album_count': len([])} for a in self.session.query(models.Artist).all()]

        ################## SETUP ALBUMS TABLE ##################
        self.albums = SongsAbstractModel(albums_data)
        self.proxy_albums = SortFilterProxyModel(self)
        self.proxy_albums.setSourceModel(self.albums)
        self.proxy_albums.setColIndexes([0])

        self.ui.albums.setModel(self.proxy_albums)

        self.ui.search_input.textChanged.connect(self.proxy_albums.setSearchText)
        ################## END ##################

        ################## SETUP ARTISTS TABLE ##################
        self.artists = SongsAbstractModel(artists_data)
        self.proxy_artists = SortFilterProxyModel(self)
        self.proxy_artists.setSourceModel(self.artists)
        self.proxy_artists.setColIndexes([0])

        self.ui.artists.setModel(self.proxy_artists)

        self.ui.search_input.textChanged.connect(self.proxy_artists.setSearchText)
        ################## END ##################

        ################## SETUP SONGS TABLE ##################
        self.songs = SongsAbstractModel(songs_data)
        self.proxy_songs = SortFilterProxyModel(self)
        self.proxy_songs.setSourceModel(self.songs)
        self.proxy_songs.setColIndexes([0, 1, 3, 5])
        self.ui.search_input.textChanged.connect(self.proxy_songs.setSearchText)
        self.ui.songs.setModel(self.proxy_songs)
        self.ui.songs.hideColumn(6)  # hide filepath
        self.ui.songs.hideColumn(7)  # hide id

        ################## END ##################

        self.father = None

    def setFather(self, father):
        self.father = father

    def enqueue_song(self, index):
        # print(self)
        mod = index.model()
        # print(mod.)
        song = dict(
            [(mod.headerData(a, Qt.Horizontal, Qt.DisplayRole), mod.itemData(index.siblingAtColumn(a))[0]) for a in
             range(mod.columnCount())])
        # print(song)

        self.father.playlist_dialog.songs.songdata.insert(0, song)
        # print(self.father.playlist_dialog.songs.songdata)
        self.father.playlist_dialog.songs.insertRows(0, 1, parent=QModelIndex())

    def add_new(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory()
        LibraryApi.add_new(path=folder)

    # def populate_songs(self):


class PlalistDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Playlist_ui_dialog()
        self.ui.setupUi(self)
        self.songs = None
        self.hello()
        # self.ui.pushButton.clicked.connect(self.pu)
        self.father = None
        self.ui.songs.doubleClicked.connect(self.play_song)

    def play_song(self, index):
        mod = index.model()
        song = dict(
            [(mod.headerData(a, Qt.Horizontal, Qt.DisplayRole), mod.itemData(index.siblingAtColumn(a))[0]) for a in
             range(mod.columnCount())])
        self.father.play_song(song)
        # self.father.playlist_dialog.songs.songdata.insert(0, song)
        # self.father.playlist_dialog.songs.insertRows(0, 1, parent=QModelIndex())

    def hello(self):
        self.songs = SongsAbstractModel([{'title': 'Justaju Jiski Thi',
                                          'album': 'Umrao Jaan',
                                          'duration': 277.70775510204084,
                                          'artists': 'Umrao Jaan (1981)',
                                          'playcount': 0,
                                          'genre': 'Umrao Jaan',
                                          'filepath': '/home/dhruv/Music/music part 2/Umrao Jaan (1981)/04 Justaju Jiski Thi - www.downloadming.com.mp3',
                                          'id': 1}])
        self.ui.songs.setModel(self.songs)
        self.ui.songs.hideColumn(1)  # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(3)  # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(4)  # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(5)  # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(6)  # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(7)  # [1, 3, 4, 5, 6, 7]

    def setFather(self, father):
        self.father = father


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    my_mainwindow = PlayerMainWindow()
    my_mainwindow.show()

    sys.exit(app.exec_())
