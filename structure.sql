-- tabella delle canzoni grezze
-- qui vengono raccolti i metadati della traccia e le informazioni
-- ottenute tramite web service last.fm
CREATE TABLE `SONGS_RAW` (
    `TITLE` TEXT NULL,
    `ALBUM` TEXT NULL,
    `ARTIST` TEXT NULL,
    `DATE` TEXT NULL,
    `LENGTH` INTEGER NULL,
    `TRACK_NO` INTEGER NULL,
    `GENRE` TEXT NULL,
    `PATH` TEXT NULL
);

-- tabella delle canzoni finali
-- dopo aver subito la rielaborazione delle altre tabella
CREATE TABLE `SONGS` (
    `SONG_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `TITLE`	TEXT NULL,
    `ALBUM_ID` INTEGER NULL,
    `LENGTH` INTEGER NULL,
    `TRACK_NO` INTEGER NULL,
    `PATH` TEXT NULL
);

-- la tabella viene popolata dai dinstinct ottenuti dalle songs_raw
-- e successivamente i campi biography e image_url tramite webapi opzionalmente
CREATE TABLE `ARTISTS` (
    `ARTIST_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `NAME` TEXT NULL,
    `BIOGRAPHY` INTEGER NULL,
    `IMAGE_URL` TEXT NULL,
    'SPOTIFY_ID' TEXT NULL
);


CREATE TABLE `ALBUMS` (
    `ALBUM_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `TITLE`	TEXT NULL,
    `ARTIST_ID` INTEGER NULL,
    `DATE` TEXT NULL,
    `COVER_URL` TEXT NULL,
    `SPOTIFY_ID` TEXT NULL
);