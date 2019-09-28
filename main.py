import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application_api import PlayerApi, LibraryApi
import models
from application_api import LibraryApi
from library_ui import Ui_Dialog

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt


class SongsAbstractModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent=None, *args)
        self.headers = []
        self.songdata = datain

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.songdata)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.songdata[0])

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(list(self.songdata[QModelIndex.row()].values())[QModelIndex.column()])

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            # print(list(self.songdata[0].keys())[p_int])
            return list(self.songdata[0].keys())[p_int]


class Main(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.songs.verticalHeader().hide()
        self.ui.artists.verticalHeader().hide()
        self.ui.albums.verticalHeader().hide()

        self.ui.library_button.clicked.connect(self.add_new)

        self.engine = create_engine('sqlite:///music.db')
        models.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.populate_songs()

    def add_new(self):
        folder = QFileDialog.getExistingDirectory()
        LibraryApi.add_new(path=folder)

    def populate_songs(self):
        # self.ui.songs.
        # songs_cursor = self.session.query(models.Song).all()
        # albums = self.session.query(models.Album).all()
        # artists = self.session.query(models.Artist).all()
        songs_data = [{'title': a.title,
                       'album': a.album.name,
                       'duration': a.duration,
                       'artists': ','.join([b.name for b in a.artists])} for a in self.session.query(models.Song).all()]
        albums_data = [{'name': a.name,
                        'track_count': len(a.songs),
                        'year': ''} for a in self.session.query(models.Album).all()]
        artists_data = [{'name': a.name,
                         'track_count': len(a.songs),
                         'album_count': len([])} for a in self.session.query(models.Artist).all()]

        songs = SongsAbstractModel(songs_data)
        artists = SongsAbstractModel(artists_data)
        albums = SongsAbstractModel(albums_data)
        self.ui.songs.setModel(songs)
        self.ui.artists.setModel(artists)
        self.ui.albums.setModel(albums)



if __name__ == '__main__':
    # Base = declarative_base()

    app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    my_dialog = Main()

    my_dialog.show()
    sys.exit(app.exec_())
