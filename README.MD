# 📖 book-match

Sagt voraus, ob mir ein Buch wahrscheinlich gefällt – basierend auf Genre, Seitenzahl, Erscheinungsjahr und ob ich die Autorin/den Autor schon kenne.

Die Gewichtung orientiert sich an meinem eigenen Lesegeschmack: viel Thriller und Romance, meist 300–450 Seiten, meist aktuelle Neuerscheinungen.

## Nutzung

**Eingabe** (`POST /buch-check`)

```json
{
  "genre": "Romance",
  "seitenzahl": 380,
  "erscheinungsjahr": 2023,
  "autor_bekannt": true
}
```

**Ausgabe**

```json
{
  "gefaellt_mir_wahrscheinlichkeit": 0.88,
  "einschaetzung": "gefällt mir wahrscheinlich",
  "begruendung": "Romance ist eines deiner Lieblingsgenres; Autor*in ist dir bereits bekannt; Seitenzahl liegt in deinem bevorzugten Bereich; aktuelle Neuerscheinung"
}
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Danach:
- Oberflaeche: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Swagger-Doku: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Tech

Python · FastAPI · uvicorn · pydantic · HTML/CSS/JS (eigene UI unter static/index.html)

## Ausblick

Die Gewichtung ist aktuell eine einfache Heuristik. In der Azure-ML-Aufgabe wird sie durch ein Modell ersetzt, das auf echten Bewertungen aus meiner eigenen Lesehistorie trainiert wird.
