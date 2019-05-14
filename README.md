# PIRATEFY-SERVER
rest api del progetto piratefy.
sono scritte in python e girano sul modulo flask, queste forniscono gli endpoint per la visualizzazione di canzoni, artisti, album e per lo streaming audio.
il progetto prevede la creazione di un database sqlite contenente le canzoni rilevate dallo scanner, che saranno poi fornite tramite gli endopoint del server

## Overview file di configurazione
Questo file gestisce i parametri dello scanner e delle api.
E' necessario impostarlo correttamente prima di avviare gli script
 **config.json**:
- **db_path:** percorso del database sqllite
- **api_key:** api key per last.fm
- **db_schema:** percorso del file contente lo schema logico del database
- **dirs:** elenco delle cartelle da scansionare
- **ignore:** elenco delle cartelle da ignorare durante la scansione
- **exts:** estensioni dei file musicali da cercare
- **last_scan:** timestamp dell'ultima scansione effettuata
- **service_port:** porta del servizio rest api

per la creazione di una api key nuova di last.fm seguire questo link https://www.last.fm/join?next=/api/account/create


## Configurazione ambiente di sviluppo
E' necessario installare Python 3 da qui https://www.python.org/downloads/
poi occorre installare le librerie **eyed3** e **flask**
```sh
$ pip install eyed3
$ pip install python-magic-bin==0.4.14
$ pip install flask
$ pip install flask_cors
```
#### Note:
- lanciare il comando pip da console con i permessi di amministratore
- python magic è richiesto per l'ultizzo di eyed3


## workflow
Seguire queste operazioni per la configurazione iniziale:
 - modificare il file **config.json** come oppurtuno (vedi la sezione dedicata al file sopra)
 - avviare il file **scanner.py**
 - al termine della scansione avviare **api.py** (tramite console, non IDLE)


## Routing API
TODO