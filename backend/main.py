from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
import os

from app.database import init_db, get_db_connection
from app.models import Activiteit, NieuwsItem, Bestuurslid

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    print("🚀 Initializing database...")
    init_db()
    print("✅ Database ready!")
    yield
    print("👋 Shutting down...")

app = FastAPI(
    title="KNA Ulft API",
    description="Backend API voor Fanfare KNA Ulft website",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🎺 Welkom bij de KNA Ulft API!",
        "version": "1.0.0",
        "endpoints": {
            "activiteiten": "/api/activiteiten",
            "nieuws": "/api/nieuws",
            "bestuur": "/api/bestuur",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "KNA API"}

# ============ ACTIVITEITEN ============
@app.get("/api/activiteiten", response_model=List[Activiteit])
def get_activiteiten():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM activiteiten WHERE is_published = 1 ORDER BY datum ASC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/api/activiteiten/{activiteit_id}")
def get_activiteit(activiteit_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activiteiten WHERE id = ?", (activiteit_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Activiteit niet gevonden")
        return dict(row)

# ============ NIEUWS ============
@app.get("/api/nieuws", response_model=List[NieuwsItem])
def get_nieuws():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM nieuws WHERE is_published = 1 ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/api/nieuws/{nieuws_id}")
def get_nieuws_item(nieuws_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nieuws WHERE id = ?", (nieuws_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Nieuws niet gevonden")
        return dict(row)

# ============ BESTUUR ============
@app.get("/api/bestuur", response_model=List[Bestuurslid])
def get_bestuur():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM bestuur WHERE is_active = 1 ORDER BY sort_order ASC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# ============ STATS ============
@app.get("/api/stats")
def get_stats():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM activiteiten WHERE is_published = 1")
        activiteiten = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM nieuws WHERE is_published = 1")
        nieuws = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bestuur WHERE is_active = 1")
        bestuur = cursor.fetchone()[0]
        
        return {
            "activiteiten": activiteiten,
            "nieuws": nieuws,
            "bestuur": bestuur
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
