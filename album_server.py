from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

@route("/albums/<artist>")
def albums(artist):
    """
    Отправляем GET-запрос на сервер. Получаем данные из БД
    Пример Httpie: http http://localhost:8080/albums/Beatles
    """
    albums_list = album.find(artist)
    if not albums_list: # Если список альбомов исполнителя пуст
        message = "Ни одного альбома исполнителя {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        # Получаем названия альбомов в список
        album_names = [album.album for album in albums_list]
        # Получаем год выпуска альбомов в список
        album_years = [album.year for album in albums_list]
        # Создаем строку об исполнителе и количестве альбомов в списке
        result = album.make_russian(artist, len(album_names))
        # Объединяем списки в формате "название альбома (год выпуска)"
        years_albums = ["{} ({})".format(album_names[i], album_years[i]) for i, item in enumerate(album_names)]
        # Объединяем строки в результат
        result += "<br>".join(years_albums)
        print(result)
    return result

@route("/albums", method="POST")
def create_album():
    """
    Отправляем POST-запрос на сервер. Сохраняем данные в БД
    Пример Httpie: http -f POST localhost:8080/albums year=2000 artist="Madonna" genre="Pop" album="Music"
    """
    # Извлекаем данные POST-запроса
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year) # Если год в некоректном формате
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        # Сохраняем запись об альбоме в БД
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:       # Если ошибки формата данных
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:  # Если альбом существует
        result = HTTPError(409, str(err))
    else:
        # Выводим сообщение если все ОК
        print("Новый альбом под ID #{} успешно сохранен".format(new_album.id))
        result = "Новый альбом под ID #{} успешно сохранен".format(new_album.id)
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)