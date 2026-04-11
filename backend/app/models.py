from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Activiteit(BaseModel):
    id: Optional[int] = None
    titel: str
    beschrijving: Optional[str] = None
    datum: Optional[str] = None
    tijd: Optional[str] = None
    locatie: Optional[str] = None
    type: Optional[str] = None
    afbeelding_url: Optional[str] = None
    is_published: bool = True

class NieuwsItem(BaseModel):
    id: Optional[int] = None
    titel: str
    content: str
    excerpt: Optional[str] = None
    auteur: Optional[str] = None
    afbeelding_url: Optional[str] = None
    is_published: bool = True

class Bestuurslid(BaseModel):
    id: Optional[int] = None
    naam: str
    functie: str
    email: Optional[str] = None
    telefoon: Optional[str] = None
    foto_url: Optional[str] = None
    bio: Optional[str] = None
    sort_order: int = 0
