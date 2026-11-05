# 3BFP2 · KB I · Selbstlernpaket Herz-Kreislauf

Selbstlernpaket zur Vorbereitung auf die Stunde „Schock“ (Themenblock 2, Woche 1).
Die Schülerinnen und Schüler scannen den QR-Code und arbeiten am Smartphone etwa 60 Minuten
fünf Module durch:

| Modul | Inhalt |
|---|---|
| Start | Leitfall Frau Maler, Überblick |
| 1 · Der Weg des Blutes | Kreislauf-Puzzle: 14 Stationen in die richtige Reihenfolge tippen |
| 2 · Herzzeitvolumen | Herz-Simulator mit zwei Missionen (HF, SV, Gefäßweite) |
| 3 · Puls & Blutdruck | Werte-Check „normal oder auffällig?“, MAD und Schockindex berechnen |
| 4 · Regulation | Blutverlust-Simulator, Klausurtraining (Aussagen beurteilen, Fall Herr Kraus) |
| 5 · Abschlusstest | 8 Fragen, ab 6 richtigen bestanden, Lernnachweis-Code für die Lehrkraft |

Inhalte: Material der Kollegin (ursprünglich als Claude-Artifact erstellt), für das Smartphone
überarbeitet. Am Text der Aufgaben wurde nichts geändert.

**Datenschutz:** keine Anmeldung, keine Cookies, keine Analyse, keine fremden Schriften oder
Skripte. Die Seite lädt nur Dateien aus diesem Repository. Der Lernfortschritt, die
Klausurantwort und die Initialen bleiben im Browser des jeweiligen Handys (localStorage) und
werden nirgends hingeschickt. Wer das Gerät wechselt, beginnt von vorn.

## Adresse und QR-Code

- Seite: https://klawittersven-arch.github.io/3BFP2_KB1_Herz-Kreislauf/
- `qr/aushang-qr-herz-kreislauf.pdf` – A4-Aushang mit QR-Code und Anleitung zum Ausdrucken
- `qr/qr-herz-kreislauf.png` – QR-Code als Bild für Folien oder Arbeitsblätter
- Auf der Seite selbst: ganz unten „QR-Code für die Klasse anzeigen“ – zeigt den Code groß
  für den Beamer.

## GitHub Pages einschalten (einmalig)

1. Auf GitHub im Repository oben **Settings** öffnen.
2. Links **Pages** wählen.
3. Bei „Build and deployment“ → Source: **Deploy from a branch**.
4. Branch: **main**, Ordner: **/docs** → **Save**.
5. Nach etwa 1–5 Minuten ist die Seite unter der Adresse oben erreichbar.

## Dateien

```
docs/                     ← alles, was GitHub Pages veröffentlicht
  index.html              ← die ganze Seite: Texte, Gestaltung und Programmlogik
  fonts/                  ← Schriften (Bricolage Grotesque, Source Sans 3, JetBrains Mono; SIL OFL)
qr/                       ← QR-Code als PNG und A4-Aushang als PDF
werkzeuge/qr_erzeugen.py  ← erzeugt den QR-Code neu und setzt ihn überall ein
```

## Texte ändern

Alle Texte stehen in `docs/index.html`. Auf GitHub die Datei öffnen, auf den Stift
(„Edit this file“) klicken und z. B. nach einem Satz suchen (Strg+F).

- Ändern Sie nur Text **zwischen den Anführungszeichen** `"…"`; Anführungszeichen, Kommas
  und Klammern bleiben stehen.
- Die Testfragen stehen unter `const QS=[`, die Werte-Karten unter `const VALS=[`, die
  Aussagen zum Klausurtraining unter `const CLAIMS=[`.
- Unten auf „Commit changes“ klicken. Nach 1–2 Minuten ist die Änderung online.

## QR-Code neu erzeugen

Nur nötig, wenn sich Name oder Besitzer des Repositorys ändern:

```
pip install reportlab pillow
python werkzeuge/qr_erzeugen.py
```

Das Skript liest die Adresse aus dem Git-Remote und erneuert den QR-Code in
`docs/index.html`, `qr/qr-herz-kreislauf.png` und `qr/aushang-qr-herz-kreislauf.pdf`.
