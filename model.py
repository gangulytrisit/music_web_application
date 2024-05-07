from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()



roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

#  User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    flag = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    playlists = db.relationship('Playlist', backref= 'user')
    songs = db.relationship('Song', backref= 'user')
    albums = db.relationship('Album', backref= 'user')




# Album model
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120), nullable=True)
    flag = db.Column(db.Boolean(), default=False)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    songs = db.relationship('Song', cascade='all, delete', backref='album')

#song model

class Song(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    genre = db.Column(db.String(64))
    flag = db.Column(db.Boolean(), default=False)
    lyrics = db.Column(db.Text(), nullable=False)
    singer = db.Column(db.String(128), nullable=False)
    date = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id'), nullable=False)
    rating = db.relationship('Rating', cascade='all, delete-orphan', backref='song')


# Playlist model


playlist_songs = db.Table('playlist_songs',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)


class Playlist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_songs, backref=db.backref('playlists', lazy='dynamic'))



#  Rating model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    rating = db.Column(db.Integer(), default=0, nullable=False)


