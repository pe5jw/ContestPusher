"""
LoTW upload handler voor ContestPusher.
Gebruikt TQSL command-line tool voor signing en upload.
"""
import asyncio
import subprocess
import tempfile
import os
from pathlib import Path


async def upload(adif_content: str, config: dict) -> dict:
    """
    Upload ADIF naar LoTW via TQSL.
    Config verwacht: tqsl_path, callsign, location (optioneel)
    """
    tqsl_path = config.get("tqsl_path", "tqsl")
    callsign = config.get("callsign", "")
    location = config.get("location", "")

    if not callsign:
        return {"ok": False, "message": "Geen callsign geconfigureerd voor LoTW"}

    # Controleer of TQSL beschikbaar is
    try:
        proc = await asyncio.create_subprocess_exec(
            tqsl_path, "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
    except FileNotFoundError:
        return {
            "ok": False,
            "message": f"TQSL niet gevonden op '{tqsl_path}'. Installeer TQSL of stel het juiste pad in."
        }

    # Schrijf ADIF naar tijdelijk bestand
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adi', delete=False, encoding='utf-8') as f:
        f.write(adif_content)
        tmp_path = f.name

    try:
        cmd = [
            tqsl_path,
            "-d",           # Geen GUI dialogen
            "-u",           # Upload naar LoTW
            "-c", callsign, # Callsign
            "-q",           # Quiet mode
        ]
        if location:
            cmd += ["-l", location]
        cmd.append(tmp_path)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)

        if proc.returncode == 0:
            return {"ok": True, "message": "Succesvol geüpload naar LoTW"}
        else:
            err = stderr.decode(errors="replace").strip()
            return {"ok": False, "message": f"TQSL fout: {err or 'Onbekende fout'}"}

    except asyncio.TimeoutError:
        return {"ok": False, "message": "Timeout: LoTW upload duurde te lang (>120s)"}
    except Exception as e:
        return {"ok": False, "message": str(e)}
    finally:
        os.unlink(tmp_path)
