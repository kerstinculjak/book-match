from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="LesegeschmackCheckerAPI")

@app.get("/", include_in_schema=False)
def ui():
    return FileResponse("static/index.html")

## DEIN CODE BEGINNT HIER ##

# Definiert das Eingabe-Schema der API
class BuchRequest(BaseModel):
    genre: Literal["Thriller", "Romance", "Fantasy", "Sachbuch", "Sonstiges"]
    seitenzahl: int = Field(..., gt=0, description="Seitenzahl des Buchs")
    erscheinungsjahr: int = Field(..., ge=1900, le=2030)
    autor_bekannt: bool = Field(..., description="Kennst du Autor*in bereits von anderen Büchern?")


# Definiert das Ausgabe-Schema der API
class BuchResponse(BaseModel):
    gefaellt_mir_wahrscheinlichkeit: float
    einschaetzung: str
    begruendung: str


# Genre-Gewichtung, abgeleitet aus dem eigenen Bücherregal:
# viel Thriller und Romance, etwas Fantasy/Dystopie.
# Diese Werte ersetzt du in der Azure-ML-Aufgabe durch ein Modell, das auf deiner
# echten Bewertungshistorie trainiert wurde.
GENRE_SCORE = {
    "Thriller": 0.40,
    "Romance": 0.30,
    "Fantasy": 0.15,
    "Sachbuch": -0.10,
    "Sonstiges": 0.0,
}

# Deine gelesenen Bücher liegen mehrheitlich zwischen 300 und 450 Seiten
# und sind fast alle aktuelle Neuerscheinungen (ab ca. 2018).
BEVORZUGTE_SEITENZAHL = (280, 460)
AB_ERSCHEINUNGSJAHR = 2018


def schaetze_gefallen(genre: str, seitenzahl: int, erscheinungsjahr: int, autor_bekannt: bool) -> tuple[float, str]:
    """Kernlogik: schätzt, wie wahrscheinlich dir das Buch gefällt."""
    basis = 0.30
    genre_bonus = GENRE_SCORE.get(genre, 0.0)
    laenge_bonus = 0.10 if BEVORZUGTE_SEITENZAHL[0] <= seitenzahl <= BEVORZUGTE_SEITENZAHL[1] else -0.05
    aktualitaet_bonus = 0.10 if erscheinungsjahr >= AB_ERSCHEINUNGSJAHR else -0.05
    autor_bonus = 0.20 if autor_bekannt else 0.0

    score = basis + genre_bonus + laenge_bonus + aktualitaet_bonus + autor_bonus
    score = max(0.0, min(score, 0.97))

    gruende = []
    if genre_bonus >= 0.25:
        gruende.append(f"{genre} ist eines deiner Lieblingsgenres")
    if autor_bonus > 0:
        gruende.append("Autor*in ist dir bereits bekannt")
    if laenge_bonus > 0:
        gruende.append("Seitenzahl liegt in deinem bevorzugten Bereich")
    if aktualitaet_bonus > 0:
        gruende.append("aktuelle Neuerscheinung")
    if not gruende:
        gruende.append("wenig Überschneidung mit deinem bisherigen Lesegeschmack")

    return round(score, 2), "; ".join(gruende)


# Erstellt eine FastAPI-Route mit dem Titel "Buch-Check"
@app.post("/buch-check", response_model=BuchResponse)
def buch_check(req: BuchRequest):
    # Ruft die Business-Logik auf, welche das Gefallen schätzt
    score, begruendung = schaetze_gefallen(
        req.genre, req.seitenzahl, req.erscheinungsjahr, req.autor_bekannt
    )
    # Gibt eine Instanz von BuchResponse zurück, die automatisch zu JSON serialisiert wird
    return BuchResponse(
        gefaellt_mir_wahrscheinlichkeit=score,
        einschaetzung="gefällt mir wahrscheinlich" if score >= 0.5 else "eher nicht mein Fall",
        begruendung=begruendung,
    )