from model import db, User as user_m, Song as song_m, Playlist as playlist_m, Album as album_m, Rating as rating_m, Role
from flask_restful import Api, Resource, reqparse, fields, marshal_with , marshal
from flask_security import auth_required, hash_password, verify_password, login_user, current_user, logout_user
from flask_security.datastore import SQLAlchemyUserDatastore
from flask import jsonify, make_response
from cache import cache
from datetime import datetime
from task import csv_rep



datastore=SQLAlchemyUserDatastore(db,user_m,Role)

api=Api(prefix="/api")


#user
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='Username of the user', required=True)
user_parser.add_argument('email', type=str, help='Email of the user', required=True)
user_parser.add_argument('role', type=str, help='role of the register', required=True)
user_parser.add_argument('password', type=str, help='password of the user', required=True)
user_parser.add_argument('flag', type=str)
user_parser.add_argument('fs_uniquifier', type=str)
user_parser.add_argument('active', type=str)


#role
role_parser = reqparse.RequestParser()
role_parser.add_argument('name', type=str, required=True, help='role')
role_parser.add_argument('description', type=str, required=False)



#song
song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str, help='Title of the song', required=True)
song_parser.add_argument('genre', type=str, help='genere of the song', required=False)
song_parser.add_argument('flag', type=bool, required=False)
song_parser.add_argument('lyrics', type=str, help='lyrics of the song', required=True)
song_parser.add_argument('singer', type=str, help='singer of the song', required=True)
song_parser.add_argument('date', type=str, help='date of the song', required=False)
song_parser.add_argument('album_id', type=int, help='ID of the album the song belongs to', required=True)
song_parser.add_argument('user_id', type=int, help='ID of the user')


#album
album_parser = reqparse.RequestParser()
album_parser.add_argument('title', type=str, help='Title of the album', required=True)
album_parser.add_argument('flag', type=bool, required=False)
album_parser.add_argument('user_id', type=int, help='user of the album', required=False)
album_parser.add_argument('artist', type=str, help='artist of the album', required=False)



#rating
rating_parser = reqparse.RequestParser()
rating_parser.add_argument('rating', type=int, help='Rating of the song', required=True)
rating_parser.add_argument('user_id', type=int, help='ID of the user giving the rating', required=True)
rating_parser.add_argument('song_id', type=int, help='ID of the song being rated', required=True)



#playlist
playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('title', type=str, help='Title of the playlist', required=True)
playlist_parser.add_argument('user_id', type=int, help='ID of the user creating the playlist', required=True)
playlist_parser.add_argument('song_ids', type=list, location = 'json', help='list of IDs of the songs', required=True)


#parser login
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, help='email of the user', required=True)
login_parser.add_argument('password', type=str, help='password of the user', required=True)





#login api
class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        email=args.get("email")
        password=args.get("password")
       
        user = datastore.find_user(email = email)
        if user:
            if verify_password(password, user.password):
                login_user(user)
                auth_token = user.get_auth_token()
                # print(auth_token)
                login_details = {'message': "user was logged in successfully",
                                  'email': current_user.email,
                                  'user_id':current_user.id,
                                  'user_role':current_user.roles[0].name,
                                  'auth_token': auth_token}
                # print(login_details)
                return make_response(jsonify(login_details))



#Logout api

class LogoutResource(Resource):
    @auth_required('token')
    def post(self):
        logout_user()
        return {'message': 'User logged out successfully'}






# Resource fields
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'flag': fields.Boolean,
    'roles': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    })),
}


#  User Api

class UserResource(Resource):
    @auth_required('token')
    def get(self, email=None):
        if email: 
            user = user_m.query.filter_by(email = email).first()
            if user:
                role = user.roles[0].name if user.roles else None
                return {'user_id': user.id,'user_name': user.username,'flag': user.flag, 'role': role}
            else:
                return {'error': 'User not found'}, 404  
        else:
            users = user_m.query.all()
            full_users = [
                marshal(user, user_fields) for user in users
            ]
            if not users:
                return {'message': 'User not found'}, 404
            return full_users

   
    def post(self):
        args = user_parser.parse_args()
        email = args.get("email")
        username = args.get("username")
        password = args.get("password")
        flag= args.get("flag",False)
        role = args.get("role","user")
        check=user_m.query.filter_by(email=email).first()
        if check:
           return jsonify({'error':'email you entered already belongs to an account. Try another email.'})
        
        role = datastore.find_role(role)
        if role is None:
            role = datastore.create_role(name=role)
        
        datastore.create_user(email=email, 
                              username=username, 
                              password=hash_password(password), 
                              roles=[role],
                              flag=flag)
        db.session.commit()
        
    
        return {'message': 'Your account is created successfully.'}
       

    #@auth_required('token')
    def put(self, email_id):
        user = user_m.query.filter_by(email=email_id).first()
        if user:
            args = user_parser.parse_args()
            role = args.get("role")
            role = datastore.find_role(role)
            if role is None:
                role = datastore.create_role(name=role)

            user.roles = [role] 
            user.flag = args.get("flag", True)
            user.flag = True 
            db.session.commit()
            return {'message': f'Role updated successfully for {user.email}'}
        else:
            return {'error': 'User not found'}, 404



    # @auth_required('token')
    def delete(self, email_id , id):
        if email_id != "admin@admin.com":
            return {'error': 'Permission denied. Only admin can delete users.'}, 403

        user = user_m.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {user.id} deleted successfully'}
        else:
            return {'error': 'User not found'}, 404



# Song api


from sqlalchemy import func

class SongResource(Resource):
    def post(self):
        args = song_parser.parse_args()
        song = song_m(  title=args['title'],
                        genre=args['genre'],
                        lyrics=args['lyrics'], 
                        singer=args['singer'], 
                        date = args['date'],
                        user_id=args['user_id'], 
                        album_id=args['album_id'], 
                        flag=args['flag'])
        db.session.add(song)
        db.session.commit()
        return {'message': 'Song created successfully'}, 201

    def get(self, song_id=None):
        if song_id:
            song = song_m.query.get(song_id)
            song_rating = db.session.query(func.avg(rating_m.rating)).filter_by(song_id=song_id).scalar()
            if song:
                return {
                    'id': song.id,
                    'title': song.title,
                    'genre': song.genre,
                    'flag': song.flag,
                    'lyrics': song.lyrics,
                    'singer': song.singer,
                    'date': song.date,
                    'user_id': song.user_id,
                    'album_id': song.album_id,
                    'rating': song_rating
                }
            else:
                return {'error': 'Song not found'}, 404
        else:
            songs = song_m.query.all()
            song_list = []
            for song in songs:
                song_rating = db.session.query(func.avg(rating_m.rating)).filter_by(song_id=song.id).scalar()
                song_list.append({
                    'id': song.id,
                    'title': song.title,
                    'genre': song.genre,
                    'flag': song.flag,
                    'lyrics': song.lyrics,
                    'singer': song.singer,
                    'date': song.date,
                    'user_id': song.user_id,
                    'album_id': song.album_id,
                    'rating': song_rating
                })
            return jsonify(song_list)

    def put(self, song_id, user_id):
        args = song_parser.parse_args()
        song = song_m.query.get(song_id)
        user = user_m.query.get(user_id)
        print(song.id)
        print(user.id)
        if song and (song.user_id == user_id):
            song.title = args['title']
            song.genre = args['genre']
            song.lyrics = args['lyrics']
            song.singer = args['singer']
            song.album_id = args['album_id']
            db.session.commit()
            return {'message': 'Song updated successfully'}
        else:
            return {'error': 'Song not found'}, 404

    def delete(self, song_id):
        song = song_m.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return {'message': 'Song deleted successfully'}
        else:
            return {'error': 'Song not found'}, 404





#Album api

class AlbumResource(Resource):
    def post(self):
        args = album_parser.parse_args()
        title = args.get('title')
        user_id = args.get('user_id')
        flag = args.get('flag')
        artist = args.get('artist')
        print(title,user_id,flag,artist)
        db.session.add(album_m(title=title, user_id=user_id, flag=flag, artist=artist))
        db.session.commit()
        return {'message': 'Album created successfully'}


    @cache.cached(timeout=15)
    def get(self, album_id=None,user_id=None):
        if album_id:
            album = album_m.query.get(album_id)
            if album:
                album_details = {
                    'id': album.id,
                    'title': album.title,
                    'flag': album.flag,
                    'user_id': album.user_id,
                    'artist': album.artist,
                    'songs': [{'id': song.id, 'title': song.title} for song in album.songs]
                }
                return jsonify(album_details)
            else:
                return jsonify({'error': 'Album not found'}), 404
        else:
            albums = album_m.query.all()
            album_list = []
            for album in albums:
                album_details = {
                    'id': album.id,
                    'title': album.title,
                    'flag': album.flag,
                    'user_id': album.user_id,
                    'artist': album.artist,
                    'songs': [{'id': song.id, 'title': song.title} for song in album.songs]
                }
                album_list.append(album_details)
            return jsonify(album_list)

    def put(self, album_id):
        album = album_m.query.get(album_id)
        if album:
            args = album_parser.parse_args()
            album.title = args.get('title')
            album.artist = args.get('artist')
            db.session.commit()
            return {'message': 'Album updated successfully'}
        else:
            return {'error': 'Album not found'}, 404

    def delete(self, album_id):
        album = album_m.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()
            return {'message': 'Album deleted successfully'}
        else:
            return {'error': 'Album not found'}, 404






# rating api

class RatingResource(Resource):
    def post(self, song_id):
        
        # rating_data = request.get_json()
        args = rating_parser.parse_args()
        rating_value = args['rating']
        user_id = args['user_id'] 
        song_id = args['song_id']  #added this
        print(rating_value)
        print(user_id)
        print(song_id)
        if rating_value < 1 or rating_value > 5:
            return jsonify({'error': 'Please rate the song between 1 and 5.'}), 400

        try:
            rating = rating_m(song_id=song_id, rating=rating_value,user_id=user_id)
            db.session.add(rating)
            db.session.commit()
            return {'message': 'Song rated successfully.'}
        except Exception as e:
            return jsonify({'error': 'Failed to rate the song. Please try again later.'}), 500



# playlist api

class PlaylistResource(Resource):
    def get(self, playlist_id=None, user_id=None):
        if playlist_id:
            playlist = playlist_m.query.get(playlist_id)
            if playlist:
                # Fetch associated songs for the playlist
                songs = []
                for song in playlist.songs:
                    song_data = {
                        "title": song.title,
                        "lyrics": song.lyrics,
                        "genre": song.genre
                    }
                    songs.append(song_data)
                    
                playlist_data = {
                    "id": playlist.id,
                    "title": playlist.title,
                    "user_id": playlist.user_id,
                    "songs": songs, 
                }
                return jsonify({"playlist": playlist_data})
            else:
                return jsonify({"error": "Playlist not found"})
        else:
            user_id = user_id
            if user_id:
                playlists = playlist_m.query.filter_by(user_id=user_id).all()
                playlist_details = []
                for playlist in playlists:
                    # Fetch associated songs for each playlist
                    songs = []
                    for song in playlist.songs:
                        song_data = {
                            "title": song.title,
                            "lyrics": song.lyrics,
                            "genre": song.genre
                        }
                        songs.append(song_data)
                    playlist_data = {
                        "id": playlist.id,
                        "title": playlist.title,
                        "user_id": playlist.user_id,
                        "songs": songs,
                    }
                    playlist_details.append(playlist_data)
                return jsonify({"playlists": playlist_details})
            else:
                playlists = playlist_m.query.all()
                playlist_details = []
                for playlist in playlists:
                    # Fetch associated songs for each playlist
                    songs = []
                    for song in playlist.songs:
                        song_data = {
                            "title": song.title,
                            "lyrics": song.lyrics,
                            "genre": song.genre
                        }
                        songs.append(song_data)
                    playlist_data = {
                        "id": playlist.id,
                        "title": playlist.title,
                        "user_id": playlist.user_id,
                        "songs": songs,
                    }
                    playlist_details.append(playlist_data)
                return jsonify({"playlists": playlist_details})

    def post(self,user_id=None):
        args = playlist_parser.parse_args()
        title = args['title']
        user_id = args['user_id'] or user_id
        song_ids = args.get('song_ids')  # List of song IDs associated with the playlist
        print(title,user_id,song_ids)
        if title and user_id:
            new_playlist = playlist_m(title=title, user_id=user_id)
            if song_ids:
                # Fetch songs from database based on song_ids
                songs = song_m.query.filter(song_m.id.in_(song_ids)).all()
                # Associate fetched songs with the playlist
                new_playlist.songs.extend(songs)
            db.session.add(new_playlist)
            db.session.commit()
            return jsonify({"message": "Playlist created successfully"})
        else:
            return jsonify({"error": "Name and user_id are required for creating a playlist"})



    def delete(self, playlist_id):
        playlist = playlist_m.query.get(playlist_id)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return jsonify({"message": "Playlist deleted successfully"})
        else:
            return jsonify({"error": "Playlist not found"})




#export api


class Exportcsv(Resource):
    def get(self, email = None):
        Albums= album_m.query.all()
        data = []
        admin_email = "admin@admin.com"
        for album in Albums:
            album_info = {"name" : album.title, "artist": album.artist , "user_id" : album.user_id , "songs" : [] }
            for song in album.songs:
              song_info = {"name" : song.title, "Genre": song.genre , "singer" : song.singer , "Lyrics" : song.lyrics , "published Date" : song.date}
              album_info["songs"].append(song_info)
            data.append(album_info)
        print(data)
        if admin_email == email:
            csv_rep.delay(data, email, user= "admin")
            return {'message': 'Monthly report will be sent to the creator.'}, 200
        else:
            return {'error': 'Creator email is required.'}, 400









api.add_resource(UserResource, '/user', '/user/<int:user_id>' , '/user/<string:email>' , '/user/<string:email>/<int:id>')
api.add_resource(AlbumResource, '/album', '/album/<int:album_id>' , '/album/<int:album_id>/<int:user_id>')
api.add_resource(RatingResource, '/rating', '/rating/<int:song_id>')
api.add_resource(PlaylistResource, '/playlist', '/playlist/<int:playlist_id>', '/playlist/user/<int:user_id>' ,'/playlist/<int:playlist_id>/<int:user_id>')
api.add_resource(SongResource, '/song', '/song/<int:song_id>', '/song/<int:song_id>/<int:user_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(Exportcsv, '/export/<string:email>')

