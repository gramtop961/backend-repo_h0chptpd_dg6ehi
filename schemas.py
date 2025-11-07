from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Tournament organizing app schemas

class Game(BaseModel):
    name: str = Field(..., description="Game name")
    genre: Optional[str] = Field(None, description="Genre/category")
    rules_url: Optional[HttpUrl] = Field(None, description="Link to rules")

class Organizer(BaseModel):
    name: str = Field(..., description="Organizer name")
    email: str = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")

class Player(BaseModel):
    name: str = Field(..., description="Player full name")
    email: str = Field(..., description="Player contact email")
    handle: Optional[str] = Field(None, description="In-game name/handle")

class Tournament(BaseModel):
    title: str = Field(..., description="Tournament title")
    game_id: str = Field(..., description="Linked game id")
    organizer_id: str = Field(..., description="Linked organizer id")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")
    location: Optional[str] = Field(None, description="Location or venue name")
    max_players: Optional[int] = Field(None, ge=2, description="Maximum number of players")

class Participant(BaseModel):
    tournament_id: str = Field(..., description="Tournament id")
    player_id: str = Field(..., description="Player id")
    team_name: Optional[str] = Field(None, description="Team name if applicable")

class VenueImage(BaseModel):
    tournament_id: str = Field(..., description="Tournament id")
    image_url: HttpUrl = Field(..., description="Public URL of the venue image")
    caption: Optional[str] = Field(None, description="Image caption")

# Note: Collection names are the lowercase of class names above.
