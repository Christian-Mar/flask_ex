# MongoDB via Docker

## Image downloaden

```
docker pull mongo:latest
```

Dit haalt de officiële MongoDB-image van Docker Hub (`docker.io/library/mongo:latest`). De image is gedownload, maar er draait nog geen container.

## Container starten

```
docker run -d --name mongodb -p 27017:27017 -v mongo_data:/data/db mongo:latest
```

| Onderdeel | Uitleg |
|---|---|
| `-d` | Draait de container op de achtergrond (detached). |
| `--name mongodb` | Geeft de container de naam `mongodb`, zodat je die makkelijk kunt beheren. |
| `-p 27017:27017` | Koppelt poort 27017 van je computer (host) aan poort 27017 in de container. 27017 is de standaardpoort van MongoDB. Formaat: `host:container`. |
| `-v mongo_data:/data/db` | Bewaart de data in een benoemd volume `mongo_data`, zodat de data blijft bestaan als de container wordt verwijderd. `/data/db` is de map waar MongoDB zijn data opslaat. |
| `mongo:latest` | De image die gebruikt wordt. |

## Verbinden

Connection string vanaf je computer:

```
mongodb://localhost:27017
```

Vanuit Python (bijv. in Flask) met `pymongo`:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["mijn_database"]
```

Een shell openen in de container:

```
docker exec -it mongodb mongosh
```

## Beheer

| Actie | Commando |
|---|---|
| Draaiende containers tonen | `docker ps` |
| Stoppen | `docker stop mongodb` |
| Opnieuw starten | `docker start mongodb` |
| Logs bekijken | `docker logs mongodb` |
| Container verwijderen (data blijft in het volume) | `docker rm mongodb` |
| Volume verwijderen (**data weg**) | `docker volume rm mongo_data` |

## Opmerkingen

- Als poort 27017 al in gebruik is, kies dan een andere hostpoort, bijv. `-p 27018:27017`, en verbind dan met `mongodb://localhost:27018`.
- Deze setup heeft geen authenticatie. Gebruik hem alleen voor lokale ontwikkeling. Voor authenticatie voeg je `-e MONGO_INITDB_ROOT_USERNAME=...` en `-e MONGO_INITDB_ROOT_PASSWORD=...` toe.
- `latest` kan na verloop van tijd naar een nieuwere versie wijzen. Pin een versie (bijv. `mongo:8`) voor reproduceerbaarheid.
