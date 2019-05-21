# PIRATEFY-SERVER
rest api del progetto piratefy.
sono scritte in python e girano sul modulo flask, queste forniscono gli endpoint per la visualizzazione di canzoni, artisti, album e per lo streaming audio.
il progetto prevede la creazione di un database sqlite contenente le canzoni rilevate dallo scanner, che saranno poi fornite tramite gli endopoint del server.
lo scanner in questione è in grado di leggere ed interagire soltanto con i file audio .mp3

## Overview file di configurazione
Questo file gestisce i parametri dello scanner e delle api.
E' necessario impostarlo correttamente prima di avviare gli script
 **config.json**:
- **db_path:** percorso del database sqllite
- **api_key:** api key per last.fm
- **db_schema:** percorso del file contente lo schema logico del database
- **dirs:** elenco delle cartelle da scansionare
- **ignore:** elenco delle cartelle da ignorare durante la scansione (TODO)
- **fetch_metadata:** se true tenta il recupero dei metadati di artisti e canzoni
- **last_scan:** timestamp dell'ultima scansione effettuata (TODO)
- **service_port:** porta del servizio rest api

per la creazione di una api key nuova di last.fm seguire questo link https://www.last.fm/join?next=/api/account/create


## Configurazione ambiente di sviluppo
E' necessario installare Python 3 da qui https://www.python.org/downloads/
poi occorre installare le librerie **eyed3**,  **flask** e **flask_cors**
```sh
$ pip install eyed3
$ pip install python-magic-bin==0.4.14
$ pip install flask
$ pip install flask_cors
```
#### Note:
- lanciare il comando pip da console con i permessi di amministratore


## workflow
Seguire queste operazioni per la configurazione iniziale:
 - modificare il file **config.json** come oppurtuno (vedi la sezione dedicata al file sopra)
 - avviare il file **scanner.py**
 - al termine della scansione eseguire **api.py** (tramite console, non IDLE) per avviare le rest api


## Routing API
host/api/songs
host/api/songs/{id}
host/api/songs/play/{id}
host/api/artists
host/api/artists/{id}
host/api/albums
host/api/albums/{id}


## Documentazioni, troubleshooting e reference
- **sqlite3**
	- http://www.sqlitetutorial.net/sqlite-python/creating-database/
	- [sqlite3 python.org](https://docs.python.org/2/library/sqlite3.html)
	- [SQLite objects created in a thread can only be used in that same thread](https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa)
	- [get dict from sqlite query](https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query)

- **documentazione api last fm** 
	- [link api lastfm](https://www.last.fm/api)
	- [creazione account api key](https://www.last.fm/join?next=/api/account/create)
	- [endpoint info artista](http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=ARTIST_NAME&api_key=YOUR_API_KEY&format=json)
	- [endpoint info album](http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=YOUR_API_KEY&artist=ARTIST_NAME&album=ALBUM_NAME&format=json)

- **eyed3** 
	- [pip installing eyed3 module failed to find libmagic](https://stackoverflow.com/questions/46518690/pip-installing-eyed3-module-failed-to-find-libmagic)
	- [pagina ufficiale eyed3](https://eyed3.readthedocs.io/en/latest/index.html)
	- [librerie per la scansione dei metadati mp3](http://www.blog.pythonlibrary.org/2010/04/22/parsing-id3-tags-from-mp3s-using-python/)
	- [esempi utilizzo eyed3 - mutagen - id3](https://stackoverflow.com/questions/8948/accessing-mp3-meta-data-with-python)
	- [esempi utilizzo eyed3](https://stackoverflow.com/questions/8948/accessing-mp3-meta-data-with-python)
	- [github eyed3 sample to set mp3 tag](https://gist.github.com/sinewalker/c636025bfc4bf3cc3e9992f212a40afa)
	- [sample utilizzo mutagen](https://www.programcreek.com/python/example/63675/mutagen.File)

- **ricerca file directory / estensioni**
	- [list all files in a directory](https://www.mkyong.com/python/python-how-to-list-all-files-in-a-directory/)
	- [find all files in a directory with extension](https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python/3964690)
	- [check if string ends with one of the strings from a list](https://stackoverflow.com/questions/18351951/check-if-string-ends-with-one-of-the-strings-from-a-list)

- **operazioni sulle stringhe**
	- [remove spaces in string](http://www.datasciencemadesimple.com/remove-spaces-in-python/)
	- [how to capitalize the first letter of each word](https://stackoverflow.com/questions/1549641/how-to-capitalize-the-first-letter-of-each-word-in-a-string-python)
	- [how-to-substring-a-string](https://stackoverflow.com/questions/663171/how-to-substring-a-string-in-python)
	- [how-to-get-the-position-of-a-character](https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python)
	- [string encoding](https://www.programiz.com/python-programming/methods/built-in/str)

- **flask/media**
	- [the taste of media streaming with flask](https://codeburst.io/the-taste-of-media-streaming-with-flask-cdce35908a50)
	- [how do i set response headers in flask](https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask)
	- [video streaming with flask](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
	- [partials content request](https://stackoverflow.com/questions/8088364/html5-video-will-not-loop)
	- [flask stream file partial (snippet utilizzato)](https://gist.github.com/lizhiwei/7885684)
	


