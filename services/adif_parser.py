"""
ADIF parser voor ContestPusher.
Ondersteunt .adi en .adif bestanden.
"""
import re
from dataclasses import dataclass, field


@dataclass
class QSO:
    call: str = ""
    band: str = ""
    mode: str = ""
    qso_date: str = ""
    time_on: str = ""
    rst_sent: str = ""
    rst_rcvd: str = ""
    freq: str = ""
    name: str = ""
    comment: str = ""
    raw: dict = field(default_factory=dict)


def parse_adif(content: str) -> tuple[list[QSO], int]:
    """
    Parseer ADIF inhoud. Geeft lijst van QSO's en totaal aantal terug.
    Werkt voor zowel .adi als .adif formaat.
    """
    # Verwijder header (alles voor <EOH>)
    eoh_match = re.search(r'<EOH>', content, re.IGNORECASE)
    if eoh_match:
        content = content[eoh_match.end():]

    qsos = []
    # Split op <EOR> records
    records = re.split(r'<EOR>', content, flags=re.IGNORECASE)

    for record in records:
        record = record.strip()
        if not record:
            continue

        # Parse alle velden uit het record
        fields = {}
        for match in re.finditer(r'<([^:>]+)(?::(\d+)(?::[A-Z])?)?>([^<]*)', record, re.IGNORECASE):
            field_name = match.group(1).upper()
            value = match.group(3).strip()
            if value:
                fields[field_name] = value

        if not fields:
            continue

        qso = QSO(
            call=fields.get("CALL", ""),
            band=fields.get("BAND", ""),
            mode=fields.get("MODE", ""),
            qso_date=fields.get("QSO_DATE", ""),
            time_on=fields.get("TIME_ON", ""),
            rst_sent=fields.get("RST_SENT", ""),
            rst_rcvd=fields.get("RST_RCVD", ""),
            freq=fields.get("FREQ", ""),
            name=fields.get("NAME", ""),
            comment=fields.get("COMMENT", ""),
            raw=fields,
        )

        if qso.call:  # Alleen geldige QSO's met een callsign
            qsos.append(qso)

    return qsos, len(qsos)


def adif_to_string(qsos: list[QSO]) -> str:
    """Converteer QSO lijst terug naar ADIF string."""
    lines = ["ContestPusher ADIF Export\n<ADIF_VER:5>3.1.4\n<EOH>\n"]
    for qso in qsos:
        record = ""
        for k, v in qso.raw.items():
            if v:
                record += f"<{k}:{len(v)}>{v} "
        record += "<EOR>\n"
        lines.append(record)
    return "\n".join(lines)
