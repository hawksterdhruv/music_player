from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    albid = Column(Integer, ForeignKey('albums.id'))
    genid = Column(Integer, ForeignKey('genres.id'))
    filepath = Column(String)
    duration = Column(Float)
    playcount = Column(Integer, default=0)
    genre = relationship('Genre', back_populates='songs')
    artists = relationship('Artist', secondary='songArtist')
    album = relationship('Album', back_populates='songs')


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    songs = relationship('Song', back_populates='album')
    # artists = relationship('Artist', secondary='albumArtist')

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    songs = relationship('Song', secondary='songArtist')
    # albums = relationship('Album', secondary='albumArtist')


class SongArtist(Base):
    __tablename__ = 'songArtist'
    artist_id = Column(Integer, ForeignKey('artists.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)

# class AlbumArtist(Base):
#     __tablename__ = 'albumArtist'
#     artist_id = Column(Integer, ForeignKey('artists.id'), primary_key=True)
#     album_id = Column(Integer, ForeignKey('albums.id'), primary_key=True)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    songs = relationship('Song', back_populates='genre')
