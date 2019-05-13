# PIRATEFY-SERVER
rest api del progetto piratefy.
sono scritte in python e girano sul modulo flask, queste forniscono gli endpoint per la visualizzazione di canzoni, artisti, album e per lo streaming audio.
il progetto prevede la creazione di un database sqlite contenente le canzoni rilevate dallo scanner, che saranno poi fornite tramite gli endopoint del server

### Overview file di configurazione
Le configurazioni dei vari parametri dello scanner e delle api sono contenute nel file **config.json**.
- **db** percorso del database sqllite
- **api_key** api key per last.fm
- **ddl.sql** percorso del file contente lo schema logico del database
- **dirs** elenco delle cartelle da scansionare
- **ignore** elenco delle cartelle da ignorare durante la scansione
- **exts** estensioni dei file musicali da cercare
- **last_scan** timestamp dell'ultima scansione effettuata
- **service_port** porta del servizio rest

per la creazione di una api key nuova di last.fm seguire questo link https://www.last.fm/join?next=/api/account/create

### Configurazione ambiente di sviluppo
- Installare Python 3 da qui https://www.python.org/downloads/

- Tramite pip installare le librerie **pytaglib** e **flask**:
```sh
pip install pytaglib==1.4.1
pip install flask
pip install flask_cors
```
Nota: è necessario forzare pip ad installare la versione indicata di pytaglib

### workflow
Seguire queste operazioni per costruire il database dei media ed avviare il server delle api
 - modificare il file **config.json** come oppurtuno (vedi la sezione dedicata al file sopra)
 - avviare il file **scanner.py**
 - avviare il file **api.py** (avviarlo tramite console, non utilizzare IDLE)
 
### Routing API
TODO