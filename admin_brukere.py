import sqlite3
import os
import shutil
import cv2

DB_FILE = "faceaccess.db"

def vis_alle_brukere():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, navn, bildemappe, opprettet_tid FROM users")
    rows = c.fetchall()
    conn.close()

    if rows:
        print(f"{'ID':<5}{'Navn':<20}{'Mappe':<30}{'Opprettet':<20}")
        print("-" * 75)
        for row in rows:
            print(f"{row[0]:<5}{row[1]:<20}{row[2]:<30}{row[3]:<20}")
    else:
        print("Ingen brukere funnet i databasen.")

def slett_bruker():
    id_to_delete = input("Skriv inn ID-en til brukeren du vil slette: ").strip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT navn, bildemappe FROM users WHERE id = ?", (id_to_delete,))
    result = c.fetchone()
    if result:
        navn, mappe = result
        bekreft = input(f"Vil du slette '{navn}' og mappen '{mappe}'? (j/n): ").strip().lower()
        if bekreft == 'j':
            c.execute("DELETE FROM users WHERE id = ?", (id_to_delete,))
            conn.commit()
            if os.path.exists(mappe):
                shutil.rmtree(mappe)
            print(f"[OK] Bruker '{navn}' slettet.")
        else:
            print("Avbrutt.")
    else:
        print("Ingen bruker funnet med den ID-en.")
    conn.close()

def endre_navn():
    id_to_update = input("Skriv inn ID-en til brukeren du vil endre navnet på: ").strip()
    nytt_navn = input("Skriv inn nytt navn: ").strip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET navn = ? WHERE id = ?", (nytt_navn, id_to_update))
    conn.commit()
    conn.close()
    print(f"[OK] Navn oppdatert til '{nytt_navn}'.")

def vis_bilder():
    id_to_view = input("Skriv inn ID-en til brukeren du vil se bilder fra: ").strip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT bildemappe FROM users WHERE id = ?", (id_to_view,))
    result = c.fetchone()
    conn.close()
    if result:
        bildemappe = result[0]
        bilder = [f for f in os.listdir(bildemappe) if f.endswith(".jpg")]
        for bilde in bilder:
            img_path = os.path.join(bildemappe, bilde)
            img = cv2.imread(img_path)
            cv2.imshow("Bilde", img)
            cv2.waitKey(300)
        cv2.destroyAllWindows()
    else:
        print("Fant ikke bruker eller mappe.")

def meny():
    while True:
        print("\nADMIN-MENY")
        print("[1] Vis alle brukere")
        print("[2] Slett en bruker")
        print("[3] Endre navn på bruker")
        print("[4] Vis bilder fra bruker")
        print("[0] Avslutt")

        valg = input("Ditt valg: ").strip()
        if valg == "1":
            vis_alle_brukere()
        elif valg == "2":
            slett_bruker()
        elif valg == "3":
            endre_navn()
        elif valg == "4":
            vis_bilder()
        elif valg == "0":
            print("Avslutter...")
            break
        else:
            print("Ugyldig valg.")

if __name__ == "__main__":
    meny()
