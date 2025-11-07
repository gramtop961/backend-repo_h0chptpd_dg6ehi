import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Game, Organizer, Player, Tournament, Participant, VenueImage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility to validate ObjectId strings

def validate_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


@app.get("/")
def read_root():
    return {"message": "Tournament API running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            collections = db.list_collection_names()
            response["collections"] = collections[:10]
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


# Basic create/list endpoints for core entities

@app.post("/games", response_model=dict)
async def create_game(game: Game):
    new_id = create_document("game", game)
    return {"id": new_id}


@app.get("/games", response_model=List[dict])
async def list_games():
    docs = get_documents("game")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/organizers", response_model=dict)
async def create_organizer(organizer: Organizer):
    new_id = create_document("organizer", organizer)
    return {"id": new_id}


@app.get("/organizers", response_model=List[dict])
async def list_organizers():
    docs = get_documents("organizer")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/players", response_model=dict)
async def create_player(player: Player):
    new_id = create_document("player", player)
    return {"id": new_id}


@app.get("/players", response_model=List[dict])
async def list_players():
    docs = get_documents("player")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/tournaments", response_model=dict)
async def create_tournament(t: Tournament):
    # Basic referential checks (optional)
    validate_id(t.game_id)
    validate_id(t.organizer_id)
    new_id = create_document("tournament", t)
    return {"id": new_id}


@app.get("/tournaments", response_model=List[dict])
async def list_tournaments():
    docs = get_documents("tournament")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/participants", response_model=dict)
async def add_participant(p: Participant):
    validate_id(p.tournament_id)
    validate_id(p.player_id)
    new_id = create_document("participant", p)
    return {"id": new_id}


@app.get("/participants", response_model=List[dict])
async def list_participants(tournament_id: Optional[str] = None):
    filt = {}
    if tournament_id:
        validate_id(tournament_id)
        filt = {"tournament_id": tournament_id}
    docs = get_documents("participant", filt)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/venue-images", response_model=dict)
async def add_venue_image(v: VenueImage):
    validate_id(v.tournament_id)
    new_id = create_document("venueimage", v)
    return {"id": new_id}


@app.get("/venue-images", response_model=List[dict])
async def list_venue_images(tournament_id: Optional[str] = None):
    filt = {}
    if tournament_id:
        validate_id(tournament_id)
        filt = {"tournament_id": tournament_id}
    docs = get_documents("venueimage", filt)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
