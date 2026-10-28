# ContestPusher — Benutzerhandbuch (Deutsch)

> **⚠️ Prüfstatus:** Nach dem Test geprüft am [DATUM] von [RUFZEICHEN]  
> Mit `[TODO]` oder `[PRÜFEN]` markierte Stellen müssen nach dem Testen bestätigt werden.

---

## Inhalt

1. [Installation](#installation)
2. [App starten](#app-starten)
3. [Dienste konfigurieren](#dienste-konfigurieren)
   - [LoTW — Logbook of the World](#lotw--logbook-of-the-world)
   - [eQSL.cc](#eqslcc)
   - [QRZ Logbook](#qrz-logbook)
   - [Club Log](#club-log)
   - [HRDLog.net](#hrdlognet)
4. [Log hochladen](#log-hochladen)
5. [Verlauf anzeigen](#verlauf-anzeigen)
6. [Häufige Fragen](#häufige-fragen)

---

## Installation

### Voraussetzungen

| Software | Version | Herunterladen |
|---|---|---|
| Python | 3.9 oder höher | [python.org/downloads](https://www.python.org/downloads/) |
| TQSL | Neueste Version | [arrl.org/tqsl-download](https://www.arrl.org/tqsl-download) *(nur für LoTW)* |

> **Windows:** Aktiviere während der Python-Installation **„Add Python to PATH"**.

### Dateien entpacken

Entpacke das ContestPusher-Archiv in einen Ordner deiner Wahl, z. B. `C:\ContestPusher\`.

---

## App starten

**Windows:**
```
Doppelklick auf start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

Beim ersten Start werden Abhängigkeiten automatisch installiert. Öffne dann deinen Browser unter:

```
http://localhost:8090
```

> Der Port kann mit der Umgebungsvariable `CONTESTPUSHER_PORT` geändert werden.

---

## Dienste konfigurieren

Gehe in der App zu **Dienste** (⚙️ in der Seitenleiste).  
Klicke auf einen Dienst, um die Einstellungen aufzuklappen. Aktiviere ihn mit dem Umschalter, fülle die Zugangsdaten aus und klicke auf **Speichern**.

Passwörter und API-Schlüssel werden **verschlüsselt lokal** auf deinem Computer gespeichert (Fernet AES-128).

---

### LoTW — Logbook of the World

**Was ist das?**  
LoTW ist das offizielle digitale QSL-System der ARRL. Bestätigungen werden kryptografisch mit einem Zertifikat signiert, das mit deinem Rufzeichen verknüpft ist.

**Voraussetzungen:**
- TQSL installiert und mit deinem Rufzeichen-Zertifikat konfiguriert
- Aktives LoTW-Konto auf [lotw.arrl.org](https://lotw.arrl.org)

**Einstellungen in ContestPusher:**

| Feld | Beschreibung |
|---|---|
| **TQSL-Pfad** | Vollständiger Pfad zur TQSL-Programmdatei. Standard: `C:\Program Files\TQSL\tqsl.exe` (Windows) oder `/usr/bin/tqsl` (Linux). `[NACH TEST PRÜFEN]` |
| **Rufzeichen** | Dein Rufzeichen, z. B. `DL1ABC`. Muss mit dem in TQSL installierten Zertifikat übereinstimmen. |
| **Passwort** | Dein LoTW / TQSL-Passwort. Wird verschlüsselt gespeichert. |

**Wie erhält man ein LoTW-Zertifikat?**

1. Erstelle ein Konto auf [lotw.arrl.org](https://lotw.arrl.org)
2. Öffne TQSL und rufe den **Station Location Wizard** auf
3. Beantrage ein Zertifikat für dein Rufzeichen
4. Die ARRL sendet eine Bestätigungs-E-Mail mit einer `.tq6`-Datei
5. Öffne diese Datei in TQSL — das Zertifikat ist jetzt installiert

> LoTW-Uploads können **30 Sekunden oder länger** dauern, da TQSL das Log zuerst signiert und dann hochlädt.

---

### eQSL.cc

**Was ist das?**  
eQSL.cc ist ein kostenloses elektronisches QSL-System, das für schnelle Bestätigungen beliebt ist.

**Konto erstellen:**  
Kostenlos registrieren auf [eqsl.cc/Member.cfm](https://www.eqsl.cc/Member.cfm)

**Einstellungen in ContestPusher:**

| Feld | Beschreibung |
|---|---|
| **Benutzername** | Dein eQSL.cc-Benutzername (dein Rufzeichen) |
| **Passwort** | Dein eQSL.cc-Passwort |

> eQSL benötigt **keinen API-Schlüssel**. Benutzername und Passwort reichen aus.

---

### QRZ Logbook

**Was ist das?**  
Das Online-Logbuch von QRZ.com mit automatischer QSL-Bestätigung für andere QRZ-Nutzer.

**Voraussetzungen:**  
Ein bezahltes **QRZ XML Subscription**-Abonnement. Ohne Abonnement funktioniert der API-Schlüssel nicht.  
Abonnieren unter [qrz.com/shop](https://www.qrz.com/shop).

**Wo findet man den API-Schlüssel?**

1. Anmelden auf [qrz.com](https://www.qrz.com)
2. Gehe zu **Logbook** → **Settings** (Zahnrad-Symbol)
3. Kopiere den Wert neben **API Key**

**Einstellungen in ContestPusher:**

| Feld | Beschreibung |
|---|---|
| **API-Schlüssel** | Der Schlüssel aus den QRZ-Logbuch-Einstellungen (langer alphanumerischer Code) |

---

### Club Log

**Was ist das?**  
Club Log ist ein kostenloser Dienst für Statistiken, DXCC-Analyse und die Veröffentlichung von Expeditions-Logs.

**Konto erstellen:**  
Kostenlos registrieren auf [clublog.org](https://clublog.org)

**Einstellungen in ContestPusher:**

| Feld | Beschreibung |
|---|---|
| **E-Mail-Adresse** | Die E-Mail-Adresse deines Club-Log-Kontos |
| **Passwort** | Dein Club-Log-Passwort |
| **Rufzeichen** | Dein Rufzeichen wie bei Club Log registriert |
| **Application Key** | `[PRÜFEN]` Möglicherweise erforderlich — zu finden in deinem Club-Log-Profil unter Settings → API |

> Club Log akzeptiert ADIF-Dateien direkt per HTTP POST. Kein gesondertes API-Abonnement erforderlich.

---

### HRDLog.net

**Was ist das?**  
HRDLog.net ist ein Online-Logbuch und eine Community für Funkamateure.

**Konto erstellen:**  
Kostenlos registrieren auf [hrdlog.net](https://www.hrdlog.net)

**Wo findet man den API-Schlüssel (Upload Code)?**

1. Anmelden auf [hrdlog.net](https://www.hrdlog.net)
2. Gehe zu **My Account** → **Upload Code** (oder **API**)
3. Kopiere den Upload Code — ein kurzer alphanumerischer Code

**Einstellungen in ContestPusher:**

| Feld | Beschreibung |
|---|---|
| **Rufzeichen** | Dein Rufzeichen |
| **Upload Code** | Der Upload Code / API-Schlüssel aus deinem HRDLog.net-Konto |

---

## Log hochladen

1. Gehe zu **Hochladen** (📤 in der Seitenleiste)
2. Ziehe deine `.adi`- oder `.adif`-Datei auf den Bereich oder klicke zum Durchsuchen
3. Klicke auf **An alle Dienste senden**
4. ContestPusher lädt parallel bei allen aktivierten Diensten hoch
5. Jeder Dienst zeigt ✅ (erfolgreich) oder ❌ (fehlgeschlagen) mit einer Meldung

> Stelle sicher, dass alle gewünschten Dienste vor dem Hochladen aktiviert sind.

---

## Verlauf anzeigen

Gehe zum **Verlauf** (📋), um alle bisherigen Uploads mit Datum, Dateiname, QSO-Anzahl und dem Ergebnis je Dienst zu sehen.

---

## Häufige Fragen

**Der LoTW-Upload dauert sehr lange oder zeigt einen Fehler.**  
Prüfe, ob TQSL mit einem gültigen Rufzeichen-Zertifikat konfiguriert ist. Öffne TQSL manuell und teste einen Upload. Kontrolliere auch den TQSL-Pfad in den ContestPusher-Einstellungen.

**Mein Passwort fehlt nach einem Neustart.**  
`[NACH TEST PRÜFEN]` Passwörter werden verschlüsselt in `contestpusher.db` gespeichert und sollten erhalten bleiben. Falls sie fehlen, wurde möglicherweise die `.key`-Datei gelöscht.

**Kann ich ContestPusher offline nutzen?**  
Nein — jeder Dienst erfordert eine Internetverbindung für den Upload.

**Kann ich nur einen Teil der QSOs hochladen?**  
Lade einfach eine ADIF-Datei hoch, die nur die gewünschten QSOs enthält. ContestPusher lädt alles hoch, was in der Datei steht.

**Die App startet nicht.**  
- Prüfe, ob Python 3.9+ installiert ist und sich im PATH befindet  
- Prüfe, ob Port 8090 bereits von einer anderen Anwendung belegt ist  
- Sieh dir die Fehlermeldung im Terminalfenster an

---

*ContestPusher ist Open Source (MIT). Quellcode: [github.com/pe5jw/ContestPusher](https://github.com/pe5jw/ContestPusher)*  
*73*
