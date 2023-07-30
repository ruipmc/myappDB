import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db


APP = Flask(__name__)

@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS songs FROM SONG').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS artists FROM ARTIST').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS albums FROM ALBUM').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS playlists FROM PLAYLIST').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS users FROM USER').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS styles FROM STYLE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS has FROM HAS').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS releases FROM RELEASES').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS features FROM FEATURES').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS genres FROM GENRE').fetchone()
    stats.update(x)
    logging.info(stats)
    return render_template('index.html',stats=stats)

#SONGS
@APP.route('/songs/')
def list_songs():
    songs = db.execute(
      '''
      SELECT IdSong, Composer, Duration, Title
      FROM SONG
      ORDER BY IdSong
      ''').fetchall()
    return render_template('songs-list.html', songs = songs)


@APP.route('/songs/<int:id>/')
def get_songs(id):
    song = db.execute(
      '''
      SELECT IdSong, Composer, Duration, Title
      FROM SONG 
      WHERE IdSong = %s
      ''', id).fetchone()

    if song is None:
      abort(404, 'Song id {} does not exist.'.format(id))

    return render_template('songs.html', 
      song=song)
    
@APP.route('/songs/search/<expr>/')
def search_song(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  songs = db.execute(
      ''' 
      SELECT IdSong, Composer, Duration, Title
      FROM SONG 
      WHERE Title LIKE %s
      ''', expr).fetchall()
  return render_template('song-search.html',
           search=search,songs = songs)
    
    
    
    
#ALBUM
@APP.route('/album')
def list_albums():
    albums = db.execute(
      '''
      SELECT IdAlbum, Title, Year
      FROM ALBUM
      ORDER BY IdAlbum
      ''').fetchall()
    
    return render_template('albums-list.html', albums = albums)
  
@APP.route('/albums/<int:id>/')
def get_albums(id):
    album = db.execute(
      '''
      SELECT IdAlbum, Title, Year
      FROM ALBUM 
      WHERE IdAlbum = %s
      ''', id).fetchone()

    if album is None:
      abort(404, 'Album id {} does not exist.'.format(id))

    return render_template('albums.html', 
      album=album)
    
@APP.route('/albums/search/<expr>/')
def search_album(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  albums = db.execute(
      ''' 
      SELECT IdAlbum, Title, Year
      FROM ALBUM 
      WHERE Title LIKE %s
      ''', expr).fetchall()
  
  return render_template('album-search.html', search=search,albums = albums)

  
#ARTIST
@APP.route('/artists/<int:id>/')
def get_artist_info(id):
  artist = db.execute(
    '''
    SELECT IdArtist, ArtistName, ArtisticalName, Country
    FROM ARTIST
    WHERE IdArtist = %s
    ''', id).fetchone()

  if artist is None:
     abort(404, 'Artist id {} does not exist.'.format(id))

  styles = db.execute(
    '''
    SELECT IdArtist, Styles
    FROM STYLE NATURAL JOIN ARTIST
    WHERE IdArtist = %s
    ORDER BY Styles
    ''', id).fetchall()
  
  songs = db.execute(
    '''
    SELECT IdSong, Composer, Duration, Title
    FROM SONG
    WHERE IdArtist = %s
    ORDER BY Title
    ''', id).fetchall()
  
  albums = db.execute(
    '''
    SELECT IdAlbum, Title, Year
    FROM ALBUM NATURAL JOIN RELEASES NATURAL JOIN ARTIST
    WHERE IdArtist = %s
    ORDER BY Title
    ''', id).fetchall()
  
  return render_template('artists.html', artist=artist, styles=styles, songs=songs, albums=albums)

@APP.route('/artist')
def list_artist():
  artists = db.execute(
    '''
    SELECT IdArtist, ArtistName, ArtisticalName, Country
    FROM ARTIST
    ORDER BY IdArtist 
    ''').fetchall()
   
  return render_template('artists-list.html', artists = artists)

    
@APP.route('/artists/search/<expr>/')
def search_artist(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  artists = db.execute(
      ''' 
      SELECT IdArtist, ArtistName
      FROM ARTIST
      WHERE ArtisticalName LIKE %s
      ''', expr).fetchall()
  
  return render_template('artist-search.html',
           search=search,artists=artists)



#STYLE
@APP.route('/style')
def list_style():
  styles = db.execute(
    '''
    SELECT IdArtist, Styles
    FROM STYLE
    GROUP BY IdArtist
    ORDER BY IdArtist 
    ''').fetchall()
   
  return render_template('styles-list.html', styles = styles)



#USER
@APP.route('/user')
def list_user():
  users = db.execute(
    '''
    SELECT Username, Followers, Following
    FROM USER
    ORDER BY Username
    ''').fetchall()
   
  return render_template('users-list.html', users=users)
  

  
#PLAYLIST
@APP.route('/playlist')
def list_playlists():
    playlists = db.execute(
      '''
      SELECT IdPlaylist, Creator, Name, TotalDuration
      FROM PLAYLIST
      ORDER BY IdPlaylist
      ''').fetchall()
    
    return render_template('playlists-list.html', playlists = playlists)