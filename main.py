import sys
from collections import OrderedDict

from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application_api import PlayerApi, LibraryApi
import models
from application_api import LibraryApi
from library_ui import Ui_Dialog as Library_ui_dialog
from player_ui import Ui_MainWindow as Player_ui_mainwindow
from playlist_ui import Ui_Dialog as Playlist_ui_dialog
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QModelIndex


# QModelIndex.siblingAtC()
# QAbstractTableModel
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


class PlayerMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Player_ui_mainwindow()
        self.ui.setupUi(self)
        self.library_dialog = LibraryDialog()
        self.library_dialog.setFather(self)
        self.playlist_dialog = PlalistDialog()
        self.playlist_dialog.setFather(self)
        self.ui.medialibrary_button.clicked.connect(self.toggle_library)
        self.ui.playlist_button.clicked.connect(self.toggle_playlist)

    def toggle_playlist(self):
        if self.playlist_dialog.isHidden():
            self.playlist_dialog.show()
        else:
            self.playlist_dialog.hide()

    def toggle_library(self):
        # my_dialog = LibraryDialog()
        # my_dialog.show()
        if self.library_dialog.isHidden():
            self.library_dialog.show()
        else:
            self.library_dialog.hide()


class LibraryDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Library_ui_dialog()
        self.ui.setupUi(self)
        self.songs = None
        self.albums = None
        self.artists = None
        # self.ui.songs.verticalHeader().hide()
        # self.ui.artists.verticalHeader().hide()
        # self.ui.albums.verticalHeader().hide()

        self.ui.library_button.clicked.connect(self.add_new)
        self.ui.songs.doubleClicked.connect(self.enqueue_song)
        # self.ui.widget.isWindowModified(self.alert)

        self.engine = create_engine('sqlite:///music.db')
        models.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.populate_songs()
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
        # self.father.playlist_dialog.songs = SongsAbstractModel([song])
        # self.father.playlist_dialog.ui.songs.setModel(self.father.playlist_dialog.songs)
        # for a in range(QModelIndex.model().columnCount()):
        # print(mod.data(QModelIndex))
        # print(mod.itemData(QModelIndex))
        pass
        # print(a.internalId())

    # print(self.songs)
    # print(QModelIndex.siblingAtRow(QModelIndex.row()).data())

    def add_new(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory()
        LibraryApi.add_new(path=folder)

    def populate_songs(self):
        # self.ui.songs.
        # songs_cursor = self.session.query(models.Song).all()
        # albums = self.session.query(models.Album).all()
        # artists = self.session.query(models.Artist).all()
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

        self.songs = SongsAbstractModel(songs_data)
        self.artists = SongsAbstractModel(artists_data)
        self.albums = SongsAbstractModel(albums_data)
        self.ui.songs.setModel(self.songs)
        self.ui.songs.hideColumn(6)  # hide filepath
        self.ui.songs.hideColumn(7)  # hide id
        self.ui.artists.setModel(self.artists)
        self.ui.albums.setModel(self.albums)


class PlalistDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Playlist_ui_dialog()
        self.ui.setupUi(self)
        self.songs = None
        self.hello()
        # self.ui.pushButton.clicked.connect(self.pu)
        self.father = None

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
        self.ui.songs.hideColumn(1) # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(3) # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(4) # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(5) # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(6) # [1, 3, 4, 5, 6, 7]
        self.ui.songs.hideColumn(7) # [1, 3, 4, 5, 6, 7]

        # print('heljlo')

    # def pu(self):
    #     k = {'title': 'Justaju Jiski Thi',
    #          'album': 'Umrao Jaan',
    #          'duration': 277.70775510204084,
    #          'artists': 'Umrao Jaan (1981)',
    #          'playcount': 0,
    #          'genre': 'Umrao Jaan',
    #          'filepath': '/home/dhruv/Music/music part 2/Umrao Jaan (1981)/04 Justaju Jiski Thi - www.downloadming.com.mp3',
    #          'id': 1}
    #     self.songs.songdata.insert(0, k)
    #     self.songs.insertRows(0, 0, parent=QModelIndex())



    def setFather(self, father):
        self.father = father


if __name__ == '__main__':
    # Base = declarative_base()

    app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    # my_dialog = LibraryDialog()

    # my_dialog.show()
    my_mainwindow = PlayerMainWindow()
    my_mainwindow.show()

    sys.exit(app.exec_())
