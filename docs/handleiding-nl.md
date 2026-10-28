# ContestPusher — Handleiding (Nederlands)

> **⚠️ Reviewstatus:** Nagekeken na test op [DATUM] door [CALLSIGN]  
> Markeringen `[TODO]` of `[CONTROLEER]` wijzen op plekken die na testen bevestigd moeten worden.

---

## Inhoud

1. [Installatie](#installatie)
2. [De app starten](#de-app-starten)
3. [Services configureren](#services-configureren)
   - [LoTW — Logbook of the World](#lotw--logbook-of-the-world)
   - [eQSL.cc](#eqslcc)
   - [QRZ Logbook](#qrz-logbook)
   - [Club Log](#club-log)
   - [HRDLog.net](#hrdlognet)
4. [Een log uploaden](#een-log-uploaden)
5. [Geschiedenis bekijken](#geschiedenis-bekijken)
6. [Veelgestelde vragen](#veelgestelde-vragen)

---

## Installatie

### Vereisten

| Software | Versie | Downloaden |
|---|---|---|
| Python | 3.9 of hoger | [python.org/downloads](https://www.python.org/downloads/) |
| TQSL | Nieuwste versie | [arrl.org/tqsl-download](https://www.arrl.org/tqsl-download) *(alleen voor LoTW)* |

> **Windows:** Vink tijdens de Python installatie **"Add Python to PATH"** aan.

### Bestanden uitpakken

Pak het ContestPusher archief uit in een map naar keuze, bijvoorbeeld `C:\ContestPusher\`.

---

## De app starten

**Windows:**
```
Dubbelklik op start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

De eerste keer worden dependencies automatisch geïnstalleerd. Open daarna je browser op:

```
http://localhost:8090
```

> De poort kun je wijzigen met de omgevingsvariabele `CONTESTPUSHER_PORT`.

---

## Services configureren

Ga in de app naar **Services** (tandwiel ⚙️ in de zijbalk).  
Klik op een service om de instellingen uit te klappen. Schakel de service in met de toggle, vul de gegevens in en klik op **Opslaan**.

Wachtwoorden en API-sleutels worden **versleuteld opgeslagen** op je lokale computer (Fernet AES-128).

---

### LoTW — Logbook of the World

**Wat is het?**  
LoTW is het officiële QSL-systeem van de ARRL. Bevestigingen worden digitaal gesigneerd met een certificaat dat aan jouw callsign is gekoppeld.

**Vereisten:**
- TQSL geïnstalleerd én geconfigureerd met jouw callsign-certificaat
- Een actief LoTW-account op [lotw.arrl.org](https://lotw.arrl.org)

**Instellingen in ContestPusher:**

| Veld | Uitleg |
|---|---|
| **TQSL pad** | Volledig pad naar de TQSL executable. Standaard `C:\Program Files\TQSL\tqsl.exe` (Windows) of `/usr/bin/tqsl` (Linux). `[CONTROLEER NA TEST]` |
| **Callsign** | Jouw callsign, bijv. `PE5JW`. Moet overeenkomen met het certificaat in TQSL. |
| **Wachtwoord** | Je LoTW / TQSL wachtwoord. Wordt versleuteld opgeslagen. |

**Hoe krijg je een LoTW certificaat?**

1. Maak een account aan op [lotw.arrl.org](https://lotw.arrl.org)
2. Open TQSL en ga naar **Station Location Wizard**
3. Vraag een certificaat aan voor jouw callsign
4. De ARRL stuurt een bevestigingsmail met een `.tq6` bestand
5. Open dat bestand in TQSL — het certificaat is nu geïnstalleerd

> LoTW uploads kunnen **30 seconden of langer** duren omdat TQSL het bestand eerst signeert en dan uploadt.

---

### eQSL.cc

**Wat is het?**  
eQSL.cc is een gratis elektronisch QSL-systeem, populair voor snelle bevestigingen.

**Account aanmaken:**  
Registreer gratis op [eqsl.cc/Member.cfm](https://www.eqsl.cc/Member.cfm)

**Instellingen in ContestPusher:**

| Veld | Uitleg |
|---|---|
| **Gebruikersnaam** | Je eQSL.cc gebruikersnaam (jouw callsign) |
| **Wachtwoord** | Je eQSL.cc wachtwoord |

> eQSL heeft **geen API-sleutel** nodig. Gebruikersnaam + wachtwoord zijn voldoende.

---

### QRZ Logbook

**Wat is het?**  
Het online logboek van QRZ.com, met automatische QSL-bevestiging voor andere QRZ-gebruikers.

**Vereisten:**  
Een betaald **QRZ XML Subscription** abonnement. Zonder betaald account werkt de API-sleutel niet.  
Abonneren kan op [qrz.com/shop](https://www.qrz.com/shop).

**Waar vind je de API-sleutel?**

1. Log in op [qrz.com](https://www.qrz.com)
2. Ga naar **Logbook** → **Settings** (tandwiel)
3. Kopieer de waarde bij **API Key**

**Instellingen in ContestPusher:**

| Veld | Uitleg |
|---|---|
| **API-sleutel** | De sleutel uit je QRZ Logbook instellingen (lang alfanumerieke code) |

---

### Club Log

**Wat is het?**  
Club Log is een gratis dienst voor statistieken, DXCC-analyse en het publiceren van expeditie-logs.

**Account aanmaken:**  
Registreer gratis op [clublog.org](https://clublog.org)

**Instellingen in ContestPusher:**

| Veld | Uitleg |
|---|---|
| **E-mailadres** | Het e-mailadres van je Club Log account |
| **Wachtwoord** | Je Club Log wachtwoord |
| **Callsign** | Jouw callsign zoals geregistreerd bij Club Log |
| **Application key** | `[CONTROLEER]` Mogelijk vereist — te vinden in je Club Log profiel onder Settings → API |

> Club Log accepteert ADIF bestanden direct via HTTP POST. Er is geen apart API-abonnement nodig.

---

### HRDLog.net

**Wat is het?**  
HRDLog.net is een online logboek en community voor radioamateurs.

**Account aanmaken:**  
Registreer gratis op [hrdlog.net](https://www.hrdlog.net)

**Waar vind je de API-sleutel (Upload Code)?**

1. Log in op [hrdlog.net](https://www.hrdlog.net)
2. Ga naar **My Account** → **Upload Code** (of **API**)
3. Kopieer de Upload Code — dit is een korte alfanumerieke code

**Instellingen in ContestPusher:**

| Veld | Uitleg |
|---|---|
| **Callsign** | Jouw callsign |
| **Upload Code** | De Upload Code / API-sleutel uit je HRDLog.net account |

---

## Een log uploaden

1. Ga naar **Upload** (📤 in de zijbalk)
2. Sleep je `.adi` of `.adif` bestand naar het vak, of klik om te bladeren
3. Klik op **Push naar alle services**
4. ContestPusher uploadt parallel naar alle ingeschakelde services
5. Per service zie je ✅ (gelukt) of ❌ (mislukt) met een foutmelding

> Zorg dat alle gewenste services ingeschakeld zijn vóór je uploadt.

---

## Geschiedenis bekijken

Ga naar **Geschiedenis** (📋) om alle eerdere uploads te zien, met datum, bestandsnaam, aantal QSOs en het resultaat per service.

---

## Veelgestelde vragen

**Het LoTW upload duurt erg lang of geeft een fout.**  
Controleer of TQSL correct is geconfigureerd met een geldig callsign-certificaat. Open TQSL handmatig en test een upload. Controleer ook het TQSL-pad in de ContestPusher instellingen.

**Mijn wachtwoord is vergeten na een herstart.**  
`[CONTROLEER NA TEST]` Wachtwoorden worden versleuteld opgeslagen in `contestpusher.db`. Ze zouden bewaard moeten blijven. Als ze weg zijn, is mogelijk het `.key` bestand verwijderd.

**Kan ik ContestPusher gebruiken zonder internet?**  
Nee, elke service vereist een internetverbinding voor de upload.

**Kan ik een deelverzameling van QSOs uploaden?**  
Upload eenvoudig een ADIF bestand met alleen de gewenste QSOs. ContestPusher uploadt alles wat in het bestand staat.

**De app start niet op.**  
- Controleer of Python 3.9+ geïnstalleerd is en in PATH staat
- Kijk of poort 8090 niet al in gebruik is door een andere applicatie
- Bekijk de foutmelding in het terminalvenster

---

*ContestPusher is open source (MIT). Broncode: [github.com/pe5jw/ContestPusher](https://github.com/pe5jw/ContestPusher)*  
*73 de PE5JW*
