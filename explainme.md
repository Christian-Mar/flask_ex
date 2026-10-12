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

## Dockerfile: niet nodig

Er is bewust geen Dockerfile. Een Dockerfile gebruik je om zelf een image te **bouwen**. Hier gebruiken we een kant-en-klare image (`mongo:latest`) van Docker Hub, dus er valt niets te bouwen.

Wel te bekijken:

| Wat | Commando |
|---|---|
| Details van de image | `docker image inspect mongo:latest` |
| Opbouw van de image per laag | `docker history mongo:latest` |
| Instellingen van de draaiende container | `docker inspect mongodb` |

Een Dockerfile is pas nodig als je de Flask-app zelf in een container wilt draaien.

## Alternatief: docker-compose.yml

In plaats van het lange `docker run`-commando kun je de configuratie in een bestand `docker-compose.yml` vastleggen. Dit bestand bestaat nu nog niet in het project.

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

| Actie | Commando |
|---|---|
| Starten | `docker compose up -d` |
| Stoppen en container verwijderen (data blijft) | `docker compose down` |
| Stoppen en ook het volume verwijderen (**data weg**) | `docker compose down -v` |

Let op: de container `mongodb` draait nu al via `docker run`. Verwijder die eerst (`docker stop mongodb && docker rm mongodb`) voordat je `docker compose up` gebruikt, anders botst de containernaam en de poort. Het volume `mongo_data` blijft bestaan, maar Compose geeft volumes standaard een voorvoegsel met de projectnaam (bijv. `flask_mongo_data`). Wil je het bestaande volume hergebruiken, voeg dan onder `volumes:` `external: true` toe bij `mongo_data`.

## Blog-applicatie (Flask)

De app staat in `src/blog/app.py`. Voorlopig geeft de route `/` alleen "hello world" terug. De app wordt gemaakt door de functie `create_app()`. `src/blog/__init__.py` is bewust leeg.

### Starten

```
uv run flask --app src/blog/app run --port 5001
```

Open daarna http://localhost:5001.

| Onderdeel | Uitleg |
|---|---|
| `uv run` | Draait het commando in de virtuele omgeving van het project (`.venv`). |
| `--app src/blog/app` | Wijst naar het bestand met de app. Flask vindt `create_app` daarin zelf. Dit werkt omdat `src/blog/__init__.py` bestaat, waardoor Flask er de module `blog.app` van maakt. |
| `run` | Start de ontwikkelserver. |
| `--port 5001` | Zie hieronder. |

Zonder `uv` kan het ook, met het volledige pad naar de Flask in de virtuele omgeving:

```
PYTHONPATH=src .venv/bin/flask --app blog.app run --port 5001
```

### Veelgemaakte fouten

- **`Could not locate a Flask application`:** je hebt waarschijnlijk `-- app` met een spatie getypt. Het moet `--app` zijn, aan elkaar. Flask leest `--` als "einde van de opties" en `app` als een los woord.
- **403 Forbidden of een vreemde serverheader (`AirTunes`) op poort 5000:** op macOS gebruikt AirPlay Receiver poort 5000, de standaardpoort van Flask. Gebruik daarom `--port 5001`, of zet AirPlay Receiver uit in Systeeminstellingen.

## Opmerkingen

- Als poort 27017 al in gebruik is, kies dan een andere hostpoort, bijv. `-p 27018:27017`, en verbind dan met `mongodb://localhost:27018`.
- Deze setup heeft geen authenticatie. Gebruik hem alleen voor lokale ontwikkeling. Voor authenticatie voeg je `-e MONGO_INITDB_ROOT_USERNAME=...` en `-e MONGO_INITDB_ROOT_PASSWORD=...` toe.
- `latest` kan na verloop van tijd naar een nieuwere versie wijzen. Pin een versie (bijv. `mongo:8`) voor reproduceerbaarheid.
