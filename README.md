# FaceAccess

FaceAccess – AI-basert innlogging med ansiktsgjenkjenning og OpenAI

Dette prosjektet er et komplett system bygget for Raspberry Pi 4 som kombinerer:
-  Ansiktsgjenkjenning
-  LED-indikatorer (grønn/rød)
-  OpenAI-basert smart assistent
-  GUI med språkvalg, tema og kategorier
-  Lokal SQLite-database for brukerhåndtering

---
 Prosjektfiler og hva de gjør

 Hovedsystem
- `app.py` – Starter kamera, gjenkjenner ansikt, viser GUI og sender spørsmål til GPT.
- `openai_gui.py` – GUI med tema- og språkvalg, forklaringskategorier og søkefelt.

 Ansiktsgjenkjenning
- `register_faces.py` – Tar bilder av ny bruker med Picamera2 og lagrer i `dataset/`. Registrerer også i databasen.
- `train_model.py` – Trener modellen (LBPH) basert på registrerte bilder.
- `recognize.py` – Kjører kun gjenkjenning og LED-tilbakemelding (test/debug).

 LED-kontroll
- `led_control.py` – Styrer grønn (GPIO 17) og rød (GPIO 27) LED.

 OpenAI
- `openai_assistant.py` – Kaller GPT-modellen og henter svar.
- `config.py` – Inneholder din OpenAI API-nøkkel (du må legge inn selv).

 Database og admin
- `database.py` – Lager og oppdaterer SQLite-databasen `faceaccess.db`.
- `admin_brukere.py` – Menyverktøy for å vise, endre og slette brukere + bilder.
- `vis_brukere.py` – Viser alle registrerte brukere i databasen.
- `vis_schema.py` – Viser SQL-strukturen (CREATE TABLE) for databasen.

---

Krav og installasjon

 Raspberry Pi-oppsett
- Raspberry Pi OS (Bookworm anbefales)
- Kamera aktivert (bruker Picamera2)
- Python 3.9+
- Installer nødvendige pakker:

```bash
sudo apt update
sudo apt install python3-picamera2 libcamera-dev libsqlite3-dev
pip install openai opencv-python
```

---

Hvordan bruke systemet

1. Kjør `register_faces.py` for å legge til bruker
2. Kjør `train_model.py` for å trene modellen
3. Start `app.py`:
```bash
python3 app.py
```

 Maskinvare

- Raspberry Pi 4
- Kamera (IMX219 eller tilsvarende)
- LED (rød og grønn)
- Motstander (220–330Ω)
- Jumper wires og breadboard

---

 Ekstra funksjoner

- GUI med mørk/lys tema
- Norsk og engelsk språkvalg
- Kategoriknapper med forklaring
- Tøm chat-knapp
- Ryddig logging og terminalrespons

---

 Sikkerhet og utvidelser

- Database lagrer hvem som er registrert
- Kan utvides med innloggingslogg, bildeanalyse, stemmestyring og mer

---

© 2024 – FaceAccess 

