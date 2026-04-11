import sqlite3
import os
from contextlib import contextmanager

DATABASE_URL = os.getenv('DATABASE_URL', '/app/data/kna.db')

@contextmanager
def get_db_connection():
    """Context manager voor database verbindingen"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialiseer de database met tabellen"""
    os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Activiteiten tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activiteiten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                beschrijving TEXT,
                datum TEXT,
                tijd TEXT,
                locatie TEXT,
                type TEXT,
                afbeelding_url TEXT,
                is_published INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Nieuws tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nieuws (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                auteur TEXT,
                afbeelding_url TEXT,
                is_published INTEGER DEFAULT 1,
                published_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bestuur tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bestuur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                functie TEXT NOT NULL,
                email TEXT,
                telefoon TEXT,
                foto_url TEXT,
                bio TEXT,
                sort_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Insert sample data als tabellen leeg zijn
        cursor.execute("SELECT COUNT(*) FROM activiteiten")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO activiteiten (titel, beschrijving, datum, tijd, locatie, type, is_published)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', [
                ('Najaarsconcert 2025', 'Ons jaarlijkse hoogtepunt met een gevarieerd programma', '2025-11-30', '14:00', 'CIVON Innovatiecentrum, Ulft', 'concert', 1),
                ('Carnavalsoptocht', 'Meespelen in de Ulftse carnavalsoptocht', '2026-03-02', '13:00', 'Ulft centrum', 'straatoptreden', 1),
                ('Bevrijdingsconcert', 'Concert met Fanfare Gregorius', '2025-05-05', '19:30', 'Kerk Varsselder-Veldhunten', 'concert', 1),
                ('Ulftse Avondvierdaagse', 'Intocht met marsmuziek', '2025-06-07', '19:00', 'Zwarte Plein, Ulft', 'straatoptreden', 1)
            ])
            
            cursor.executemany('''
                INSERT INTO bestuur (naam, functie, email, sort_order)
                VALUES (?, ?, ?, ?)
            ''', [
                ('Ineke Aalders', 'Secretaris', 'secretaris@kna-ulft.nl', 1),
                ('Marco Geerts', 'Penningmeester', 'penningmeester@kna-ulft.nl', 2),
                ('Resie Kock', 'Algemene Zaken', 'info@kna-ulft.nl', 3),
                ('Bram Roes', 'Algemene Zaken', 'info@kna-ulft.nl', 4)
            ])
            
            cursor.executemany('''
                INSERT INTO nieuws (titel, content, auteur, is_published, published_at)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', [
                ('KNA Viert 106-jarig Bestaan!', 'Fanfare Kunst Na Arbeid bestaat dit jaar 106 jaar. Opgericht in 1919!', 'Ana', 1),
                ('Nieuw Jeugdproject Gestart', 'We zijn begonnen met Muzikidz! voor jonge muzikanten.', 'Henrite Jansma-Rusch', 1)
            ])
        
        conn.commit()
        print("✅ Database geïnitialiseerd!")

if __name__ == '__main__':
    init_db()
