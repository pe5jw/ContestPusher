# ContestPusher — User Manual (English)

> **⚠️ Review status:** Reviewed after testing on [DATE] by [CALLSIGN]  
> Items marked `[TODO]` or `[VERIFY]` need confirmation after testing.

---

## Contents

1. [Installation](#installation)
2. [Starting the app](#starting-the-app)
3. [Configuring services](#configuring-services)
   - [LoTW — Logbook of the World](#lotw--logbook-of-the-world)
   - [eQSL.cc](#eqslcc)
   - [QRZ Logbook](#qrz-logbook)
   - [Club Log](#club-log)
   - [HRDLog.net](#hrdlognet)
4. [Uploading a log](#uploading-a-log)
5. [Viewing history](#viewing-history)
6. [Frequently asked questions](#frequently-asked-questions)

---

## Installation

### Requirements

| Software | Version | Download |
|---|---|---|
| Python | 3.9 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| TQSL | Latest | [arrl.org/tqsl-download](https://www.arrl.org/tqsl-download) *(for LoTW only)* |

> **Windows:** During Python installation, check **"Add Python to PATH"**.

### Extracting files

Extract the ContestPusher archive to a folder of your choice, e.g. `C:\ContestPusher\`.

---

## Starting the app

**Windows:**
```
Double-click start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

On first run, dependencies are installed automatically. Then open your browser at:

```
http://localhost:8090
```

> The port can be changed with the environment variable `CONTESTPUSHER_PORT`.

---

## Configuring services

Go to **Services** (⚙️ in the sidebar).  
Click a service to expand its settings. Enable it with the toggle, fill in the credentials, and click **Save**.

Passwords and API keys are **encrypted locally** on your computer (Fernet AES-128).

---

### LoTW — Logbook of the World

**What is it?**  
LoTW is the ARRL's official digital QSL system. Confirmations are cryptographically signed with a certificate tied to your callsign.

**Requirements:**
- TQSL installed and configured with your callsign certificate
- An active LoTW account at [lotw.arrl.org](https://lotw.arrl.org)

**Settings in ContestPusher:**

| Field | Description |
|---|---|
| **TQSL path** | Full path to the TQSL executable. Default: `C:\Program Files\TQSL\tqsl.exe` (Windows) or `/usr/bin/tqsl` (Linux). `[VERIFY AFTER TEST]` |
| **Callsign** | Your callsign, e.g. `W1AW`. Must match the certificate installed in TQSL. |
| **Password** | Your LoTW / TQSL password. Stored encrypted. |

**How to get a LoTW certificate:**

1. Create an account at [lotw.arrl.org](https://lotw.arrl.org)
2. Open TQSL and go to **Station Location Wizard**
3. Request a certificate for your callsign
4. The ARRL sends a confirmation email with a `.tq6` file
5. Open that file in TQSL — the certificate is now installed

> LoTW uploads may take **30 seconds or more** because TQSL first signs the log, then uploads it.

---

### eQSL.cc

**What is it?**  
eQSL.cc is a free electronic QSL system, popular for quick confirmations.

**Creating an account:**  
Register for free at [eqsl.cc/Member.cfm](https://www.eqsl.cc/Member.cfm)

**Settings in ContestPusher:**

| Field | Description |
|---|---|
| **Username** | Your eQSL.cc username (your callsign) |
| **Password** | Your eQSL.cc password |

> eQSL does **not** require an API key. Username and password are sufficient.

---

### QRZ Logbook

**What is it?**  
QRZ.com's online logbook, with automatic QSL confirmation for other QRZ users.

**Requirements:**  
A paid **QRZ XML Subscription**. Without a paid account the API key does not work.  
Subscribe at [qrz.com/shop](https://www.qrz.com/shop).

**Where to find the API key:**

1. Log in at [qrz.com](https://www.qrz.com)
2. Go to **Logbook** → **Settings** (gear icon)
3. Copy the value next to **API Key**

**Settings in ContestPusher:**

| Field | Description |
|---|---|
| **API key** | The key from your QRZ Logbook settings (long alphanumeric string) |

---

### Club Log

**What is it?**  
Club Log is a free service for statistics, DXCC analysis, and publishing expedition logs.

**Creating an account:**  
Register for free at [clublog.org](https://clublog.org)

**Settings in ContestPusher:**

| Field | Description |
|---|---|
| **Email address** | The email address of your Club Log account |
| **Password** | Your Club Log password |
| **Callsign** | Your callsign as registered with Club Log |
| **Application key** | `[VERIFY]` May be required — found in your Club Log profile under Settings → API |

> Club Log accepts ADIF files directly via HTTP POST. No separate API subscription is needed.

---

### HRDLog.net

**What is it?**  
HRDLog.net is an online logbook and community for amateur radio operators.

**Creating an account:**  
Register for free at [hrdlog.net](https://www.hrdlog.net)

**Where to find the API key (Upload Code):**

1. Log in at [hrdlog.net](https://www.hrdlog.net)
2. Go to **My Account** → **Upload Code** (or **API**)
3. Copy the Upload Code — it is a short alphanumeric string

**Settings in ContestPusher:**

| Field | Description |
|---|---|
| **Callsign** | Your callsign |
| **Upload Code** | The Upload Code / API key from your HRDLog.net account |

---

## Uploading a log

1. Go to **Upload** (📤 in the sidebar)
2. Drag your `.adi` or `.adif` file onto the drop zone, or click to browse
3. Click **Push to all services**
4. ContestPusher uploads to all enabled services in parallel
5. Each service shows ✅ (success) or ❌ (failed) with a message

> Make sure all desired services are enabled before uploading.

---

## Viewing history

Go to **History** (📋) to see all previous uploads, including date, filename, QSO count, and the result per service.

---

## Frequently asked questions

**The LoTW upload takes a very long time or shows an error.**  
Check that TQSL is correctly configured with a valid callsign certificate. Open TQSL manually and test an upload. Also verify the TQSL path in the ContestPusher settings.

**My password is gone after restarting.**  
`[VERIFY AFTER TEST]` Passwords are stored encrypted in `contestpusher.db` and should persist. If they disappear, the `.key` file may have been deleted.

**Can I use ContestPusher offline?**  
No — each service requires an internet connection to upload.

**Can I upload a subset of QSOs?**  
Simply upload an ADIF file containing only the QSOs you want. ContestPusher uploads everything in the file.

**The app won't start.**  
- Check that Python 3.9+ is installed and on PATH  
- Check that port 8090 is not already in use  
- Look at the error message in the terminal window

---

*ContestPusher is open source (MIT). Source code: [github.com/pe5jw/ContestPusher](https://github.com/pe5jw/ContestPusher)*  
*73*
