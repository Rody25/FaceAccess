import sqlite3

DB_FILE = "faceaccess.db"

def vis_alle_brukere():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, navn, bildemappe, opprettet_tid FROM users")
        rows = c.fetchall()

        if rows:
            print(f"{'ID':<5}{'Navn':<20}{'Mappe':<30}{'Opprettet':<20}")
            print("-" * 75)
            for row in rows:
                print(f"{row[0]:<5}{row[1]:<20}{row[2]:<30}{row[3]:<20}")
        else:
            print("Ingen brukere funnet i databasen.")
        conn.close()
    except Exception as e:
        print(f"[Feil] Kunne ikke lese databasen: {e}")

if __name__ == "__main__":
    vis_alle_brukere()
