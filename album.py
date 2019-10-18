import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
    """
    Используется для идентификации ошибок
    """
    pass

class AlreadyExists(Error):
    """
    Используется для идентификации существующей записи
    """
    pass

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(year, artist, genre, album):
    """
    Сохраняем запись в базу данных
    """
    assert (year > 1900 and year < 2020), "Указано некорректное значение года"
    assert isinstance(artist, str), "Указано некорректное значение исполнителя"
    assert isinstance(genre, str), "Указано некорректное значение жанра"
    assert isinstance(album, str), "Указано некорректное значение альбома"

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None: # Если такой альбом существует
        raise AlreadyExists("Такой альбом уже сужествует и имеет следующий ID #{}".format(saved_album.id))

    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )    
    session.add(album)
    session.commit()
    return album

def make_russian(artist, albums):
    """
    Создаем строку об исполнителе и количестве альбомов
    в списке в соответствии с русским языком
    """
    if albums % 10 == 1 and albums % 100 != 11:
        album_str = "альбома"
    else:
        album_str = "альбомов"
    return "Список исполнителя " + artist + " состоит из " +\
    		 str(albums) + " " + album_str + ":<br>"