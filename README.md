# ContestPusher 📤

**Upload je contest log naar alle grote ham radio diensten in één klik.**

ContestPusher is een gratis, open source (MIT) self-hosted webapp die je lokaal draait op Windows of Linux. Je laadt een ADIF bestand in, en het wordt parallel gepushed naar alle ingeschakelde services: LoTW, eQSL, QRZ, Club Log en HRDLog.net.

---

## Ondersteunde diensten

| Service | Protocol | Vereisten |
|---|---|---|
| **Logbook of the World (LoTW)** | TQSL CLI | TQSL geïnstalleerd + geconfigureerd |
| **eQSL.cc** | HTTP POST | eQSL account |
| **QRZ Logbook** | REST API | Betaald QRZ abonnement |
| **Club Log** | HTTP POST | Club Log account |
| **HRDLog.net** | REST API | HRDLog account + API key |

---

## Vereisten

- **Python 3.9+** — [python.org/downloads](https://www.python.org/downloads/)
- **TQSL** (alleen voor LoTW) — [arrl.org/tqsl-download](https://www.arrl.org/tqsl-download)

---

## Installatie & starten

### Windows

```
dubbelklik start.bat
```

Of via de command prompt:
```bat
cd C:\pad\naar\contestpusher
start.bat
```

### Linux / macOS

```bash
cd /pad/naar/contestpusher
chmod +x start.sh
./start.sh
```

De eerste keer worden dependencies automatisch geïnstalleerd in een `.venv` map.

### Open in je browser

```
http://localhost:8090
```

---

## Gebruik

1. **Services configureren** — Ga naar "Services" en vul je credentials in per dienst. Sla op met de knop. Wachtwoorden worden versleuteld opgeslagen.

2. **Log uploaden** — Ga naar "Upload", sleep je `.adi` of `.adif` bestand in het vak, klik "Push naar alle services". Je ziet per service of het gelukt is.

3. **Geschiedenis** — Onder "Geschiedenis" vind je alle eerdere uploads met de resultaten per service.

---

## Poort wijzigen

Standaard draait ContestPusher op poort `8090`. Je kunt dit wijzigen met een omgevingsvariabele:

**Windows:**
```bat
set CONTESTPUSHER_PORT=9000
start.bat
```

**Linux/macOS:**
```bash
CONTESTPUSHER_PORT=9000 ./start.sh
```

---

## Beveiliging

- Alle wachtwoorden worden versleuteld opgeslagen (Fernet AES-128) in `contestpusher.db`
- De encryptiesleutel staat in `contestpusher.key` (chmod 600 op Linux)
- De app luistert alleen op `127.0.0.1` (localhost) — niet bereikbaar van buitenaf
- Deel **nooit** `contestpusher.key` of `contestpusher.db`

---

## Projectstructuur

```
contestpusher/
├── main.py              # FastAPI applicatie
├── database.py          # SQLite + credential encryptie
├── requirements.txt     # Python dependencies
├── start.sh             # Linux/macOS starter
├── start.bat            # Windows starter
├── templates/
│   └── index.html       # Single-page frontend (NL/EN/DE/ES)
├── docs/
│   ├── handleiding-nl.md  # Nederlandstalige handleiding
│   ├── manual-en.md       # English user manual
│   ├── handbuch-de.md     # Deutsches Benutzerhandbuch
│   └── manual-es.md       # Manual en español
└── services/
    ├── adif_parser.py   # ADIF parser
    ├── lotw.py          # LoTW (via TQSL)
    ├── eqsl.py          # eQSL.cc
    ├── qrz.py           # QRZ Logbook
    ├── clublog.py       # Club Log
    └── hrdlog.py        # HRDLog.net
```

---

## Open source & donaties

ContestPusher is MIT licentie. Broncode: [github.com/pe5jw/ContestPusher](https://github.com/pe5jw/ContestPusher)

Vind je het nuttig? Help de ontwikkeling met een kleine donatie — elke koffie telt! ☕

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Doneer-FF5E5B?logo=ko-fi)](https://ko-fi.com/contestpusher)

---

## Licentie

MIT © Joeri

73 de PE5JW 🎙️
