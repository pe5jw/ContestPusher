"""
ContestPusher — Desktop launcher
Klein Tkinter venster: start/stop de server, open browser.
Geen shell venster nodig.
"""
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import font as tkfont

# ── Zorg dat imports vanuit de ContestPusher map werken ──────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

PORT = int(os.environ.get("CONTESTPUSHER_PORT", 8090))
URL  = f"http://localhost:{PORT}"

# ── Kleuren ───────────────────────────────────────────────────────────────────
BG        = "#0f1117"
BG2       = "#181c27"
BORDER    = "#2a3045"
FG        = "#e2e8f0"
FG2       = "#94a3b8"
ACCENT    = "#3b82f6"
OK        = "#22c55e"
ERR       = "#ef4444"
WARN      = "#f59e0b"

# ── Server thread ─────────────────────────────────────────────────────────────
_server   = None
_thread   = None

def _run_server():
    import uvicorn
    from main import app
    from database import init_db
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=PORT,
                log_level="error", access_log=False)

def start_server():
    global _server, _thread
    _thread = threading.Thread(target=_run_server, daemon=True)
    _thread.start()

def server_running() -> bool:
    """Controleer of de server reageert."""
    try:
        import urllib.request
        urllib.request.urlopen(URL + "/api/version", timeout=1)
        return True
    except Exception:
        return False

# ── GUI ───────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ContestPusher")
        self.resizable(False, False)
        self.configure(bg=BG)
        # Probeer een app-icoontje in te stellen (optioneel)
        try:
            icon = Path(__file__).parent / "static" / "icon.png"
            if icon.exists():
                img = tk.PhotoImage(file=str(icon))
                self.iconphoto(True, img)
        except Exception:
            pass

        self._build_ui()
        self._state = "stopped"   # stopped | starting | running
        self._auto_started = False

        # Start de server meteen bij openen
        self.after(100, self._auto_start)
        # Poll status elke seconde
        self.after(1000, self._poll)

    # ── UI bouwen ──────────────────────────────────────────────────────────
    def _build_ui(self):
        pad = {"padx": 24, "pady": 0}

        # ── Header ──
        header = tk.Frame(self, bg=BG2, pady=18)
        header.pack(fill="x")

        title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        sub_font   = tkfont.Font(family="Segoe UI", size=10)

        tk.Label(header, text="Contest", font=title_font,
                 bg=BG2, fg=FG).pack(side="left", padx=(24,0))
        tk.Label(header, text="Pusher", font=title_font,
                 bg=BG2, fg=ACCENT).pack(side="left")
        self._ver_lbl = tk.Label(header, text="v0.1.0",
                                  font=sub_font, bg=BG2, fg=FG2)
        self._ver_lbl.pack(side="right", padx=24)

        # ── Statusbalk ──
        status_frame = tk.Frame(self, bg=BG, pady=20)
        status_frame.pack(fill="x", **pad)

        dot_font   = tkfont.Font(family="Segoe UI", size=14)
        label_font = tkfont.Font(family="Segoe UI", size=11)
        url_font   = tkfont.Font(family="Segoe UI", size=10)

        row = tk.Frame(status_frame, bg=BG)
        row.pack(anchor="w")
        self._dot = tk.Label(row, text="●", font=dot_font, bg=BG, fg=WARN)
        self._dot.pack(side="left")
        self._status_lbl = tk.Label(row, text="  Starten…", font=label_font,
                                     bg=BG, fg=FG2)
        self._status_lbl.pack(side="left")

        self._url_lbl = tk.Label(status_frame, text=URL, font=url_font,
                                  bg=BG, fg=FG2, cursor="hand2")
        self._url_lbl.pack(anchor="w", pady=(4,0))
        self._url_lbl.bind("<Button-1>", lambda e: self._open_browser())

        # ── Knoppen ──
        btn_frame = tk.Frame(self, bg=BG, pady=4)
        btn_frame.pack(fill="x", padx=24, pady=(0, 24))

        btn_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        self._open_btn = tk.Button(
            btn_frame, text="🌐  Open in browser",
            font=btn_font, bg=ACCENT, fg="#fff", relief="flat",
            activebackground="#1d4ed8", activeforeground="#fff",
            padx=16, pady=9, cursor="hand2",
            command=self._open_browser
        )
        self._open_btn.pack(fill="x", pady=(0, 8))

        self._stop_btn = tk.Button(
            btn_frame, text="⏹  Stoppen",
            font=btn_font, bg=BG2, fg=FG2, relief="flat",
            activebackground=BORDER, activeforeground=FG,
            padx=16, pady=9, cursor="hand2",
            command=self._stop
        )
        self._stop_btn.pack(fill="x")

        # ── Breedte fixeren ──
        self.geometry("320x220")
        self.update_idletasks()

    # ── Acties ────────────────────────────────────────────────────────────
    def _auto_start(self):
        if not self._auto_started:
            self._auto_started = True
            self._set_state("starting")
            start_server()

    def _open_browser(self):
        if self._state == "running":
            webbrowser.open(URL)

    def _stop(self):
        self._set_state("stopped")
        self.after(400, self.destroy)

    # ── State machine ──────────────────────────────────────────────────────
    def _set_state(self, state: str):
        self._state = state
        if state == "starting":
            self._dot.config(fg=WARN)
            self._status_lbl.config(text="  Starten…", fg=FG2)
            self._open_btn.config(state="disabled", bg=BORDER, fg=FG2, cursor="")
            self._stop_btn.config(state="normal")
        elif state == "running":
            self._dot.config(fg=OK)
            self._status_lbl.config(text="  Actief", fg=FG)
            self._open_btn.config(state="normal", bg=ACCENT, fg="#fff", cursor="hand2")
            self._stop_btn.config(state="normal")
            # Eenmalig browser openen
            if not getattr(self, "_browser_opened", False):
                self._browser_opened = True
                self.after(300, webbrowser.open, URL)
        elif state == "stopped":
            self._dot.config(fg=ERR)
            self._status_lbl.config(text="  Gestopt", fg=FG2)
            self._open_btn.config(state="disabled", bg=BORDER, fg=FG2, cursor="")
            self._stop_btn.config(state="disabled")

    def _poll(self):
        """Controleer elke seconde of de server actief is."""
        if self._state in ("starting", "running"):
            if server_running():
                if self._state != "running":
                    self._set_state("running")
            else:
                if self._state == "running":
                    self._set_state("starting")
        self.after(1000, self._poll)

    # ── Venster sluiten ───────────────────────────────────────────────────
    def on_close(self):
        self._stop()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
