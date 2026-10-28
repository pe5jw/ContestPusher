"""
eQSL.cc upload handler voor ContestPusher.
Gebruikt de eQSL HTTP import API.
"""
import httpx


EQSL_UPLOAD_URL = "https://www.eqsl.cc/qslnet/ImportADIF.cfm"


async def upload(adif_content: str, config: dict) -> dict:
    """
    Upload ADIF naar eQSL.cc.
    Config verwacht: username, password
    """
    username = config.get("username", "")
    password = config.get("password", "")

    if not username or not password:
        return {"ok": False, "message": "Gebruikersnaam en wachtwoord vereist voor eQSL"}

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                EQSL_UPLOAD_URL,
                data={
                    "EQSL_USER": username,
                    "EQSL_PSWD": password,
                    "ADIFData": adif_content,
                }
            )

        body = response.text
        # eQSL geeft tekstuele response terug
        if "Error" in body or "error" in body:
            # Extraheer foutmelding
            msg = body.strip()[:200]
            return {"ok": False, "message": f"eQSL fout: {msg}"}
        elif "accepted" in body.lower() or "imported" in body.lower():
            # Probeer aantal geaccepteerde QSO's te vinden
            import re
            match = re.search(r'(\d+)\s+(?:QSO|record)', body, re.IGNORECASE)
            count = match.group(1) if match else "?"
            return {"ok": True, "message": f"{count} QSO's geaccepteerd door eQSL"}
        else:
            return {"ok": True, "message": "Upload verzonden naar eQSL (status onbekend)"}

    except httpx.TimeoutException:
        return {"ok": False, "message": "Timeout: eQSL reageert niet"}
    except httpx.RequestError as e:
        return {"ok": False, "message": f"Netwerkfout: {str(e)}"}
    except Exception as e:
        return {"ok": False, "message": str(e)}
