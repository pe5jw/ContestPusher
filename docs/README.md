# ContestPusher — Documentation

This folder contains user manuals in all supported languages.

| File | Language | Review status |
|---|---|---|
| `handleiding-nl.md` | 🇳🇱 Nederlands | ⏳ Needs review after testing |
| `manual-en.md` | 🇬🇧 English | ⏳ Needs review after testing |
| `handbuch-de.md` | 🇩🇪 Deutsch | ⏳ Needs review after testing |
| `manual-es.md` | 🇪🇸 Español | ⏳ Needs review after testing |

## What to check per manual

After testing ContestPusher, go through each manual and confirm:

- [ ] TQSL path defaults are correct for the OS
- [ ] All service field names match what's shown in the UI
- [ ] LoTW upload timeout behaviour description is accurate
- [ ] Club Log — confirm whether Application Key is required or not
- [ ] All links still work (service websites, registration pages)
- [ ] Replace `[DATE]` and `[CALLSIGN]` in the review header

Items marked `[VERIFY]` / `[CONTROLEER]` / `[PRÜFEN]` / `[VERIFICAR]` are placeholders that need confirmation.

## Adding a new language

1. Copy an existing manual file as `manual-XX.md`
2. Translate all content
3. Add a row to the table above
4. Add the language to `LANGS` in `templates/index.html`
5. Add a flag button in the `#langPicker` div in `templates/index.html`
