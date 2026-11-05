"""QR-Code für das Selbstlernpaket erzeugen und überall einsetzen.

Nur nötig, wenn sich der Name des Repositorys oder der Besitzer ändert.

    pip install reportlab pillow
    python werkzeuge/qr_erzeugen.py                 # Adresse aus dem Git-Remote
    python werkzeuge/qr_erzeugen.py https://…/      # oder Adresse direkt angeben

Das Skript
  * setzt den QR-Code und den Link in docs/index.html ein (Knopf „QR-Code für die Klasse anzeigen“),
  * schreibt qr/qr-herz-kreislauf.png (zum Einfügen in Folien und Arbeitsblätter),
  * schreibt qr/aushang-qr-herz-kreislauf.pdf (A4-Aushang zum Ausdrucken).
Fehlerkorrektur Q, Ruhezone 4 Module.
"""
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw
from reportlab.graphics.barcode import qrencoder
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITE = os.path.join(WURZEL, "docs", "index.html")
PNG = os.path.join(WURZEL, "qr", "qr-herz-kreislauf.png")
PDF = os.path.join(WURZEL, "qr", "aushang-qr-herz-kreislauf.pdf")
RUHEZONE = 4


def adresse_aus_git():
    remote = subprocess.check_output(["git", "-C", WURZEL, "remote", "get-url", "origin"], text=True).strip()
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", remote)
    if not m:
        sys.exit("Konnte Besitzer/Repository nicht aus dem Git-Remote lesen: " + remote)
    besitzer, repo = m.groups()
    return f"https://{besitzer.lower()}.github.io/{repo}/"


def matrix(url):
    q = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.Q)
    q.addData(url)
    q.make()
    n = q.getModuleCount()
    return n, [(r, c) for r in range(n) for c in range(n) if q.isDark(r, c)]


def seite_aktualisieren(url, n, dunkel):
    N = n + 2 * RUHEZONE
    pfad = "".join(f"M{c + RUHEZONE} {r + RUHEZONE}h1v1h-1z" for r, c in dunkel)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" shape-rendering="crispEdges" role="img" '
           f'aria-label="QR-Code zum Selbstlernpaket Herz-Kreislauf"><rect width="{N}" height="{N}" fill="var(--qr-bg)"/>'
           f'<path d="{pfad}" fill="var(--qr-ink)"/></svg>')
    html = open(SEITE, encoding="utf-8").read()
    html, a = re.subn(r"<!--QR-START-->.*?<!--QR-END-->", "<!--QR-START-->" + svg + "<!--QR-END-->", html, flags=re.S)
    html, b = re.subn(r'const QR_URL="[^"]*";', f'const QR_URL="{url}";', html)
    if a != 1 or b != 1:
        sys.exit("Markierungen in docs/index.html nicht gefunden (<!--QR-START-->…<!--QR-END--> und const QR_URL).")
    open(SEITE, "w", encoding="utf-8").write(html)


def png_schreiben(n, dunkel, px=24):
    N = n + 2 * RUHEZONE
    bild = Image.new("RGB", (N * px, N * px), "white")
    zeichnen = ImageDraw.Draw(bild)
    for r, c in dunkel:
        x, y = (c + RUHEZONE) * px, (r + RUHEZONE) * px
        zeichnen.rectangle([x, y, x + px - 1, y + px - 1], fill=(15, 26, 34))
    bild.save(PNG)


def schriften():
    kandidaten = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/consola.ttf"),
        ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf", "/Library/Fonts/Courier New.ttf"),
    ]
    for normal, fett, mono in kandidaten:
        if all(os.path.exists(p) for p in (normal, fett, mono)):
            pdfmetrics.registerFont(TTFont("Sans", normal))
            pdfmetrics.registerFont(TTFont("SansB", fett))
            pdfmetrics.registerFont(TTFont("Mono", mono))
            return "Sans", "SansB", "Mono"
    return "Helvetica", "Helvetica-Bold", "Courier"


def pdf_schreiben(url, n, dunkel):
    sans, fett, mono = schriften()
    N = n + 2 * RUHEZONE
    B, H = A4
    rot, tinte, grau = (0.70, 0.125, 0.184), (0.094, 0.137, 0.176), (0.357, 0.42, 0.47)
    cv = canvas.Canvas(PDF, pagesize=A4)
    cv.setTitle("Selbstlernpaket Herz-Kreislauf – QR-Code")
    cv.setFillColorRGB(*rot); cv.rect(0, H - 0.8 * cm, B, 0.8 * cm, stroke=0, fill=1)
    cv.setFillColorRGB(*grau); cv.setFont(sans, 10.5)
    cv.drawString(2 * cm, H - 2.2 * cm, "3BFP2 · KB I · THEMENBLOCK 2 · VORBEREITUNG AUF WOCHE 1")
    cv.setFillColorRGB(*tinte); cv.setFont(fett, 30)
    cv.drawString(2 * cm, H - 3.6 * cm, "Selbstlernpaket")
    cv.drawString(2 * cm, H - 4.9 * cm, "Herz-Kreislauf")
    cv.setFont(sans, 13); cv.setFillColorRGB(*grau)
    cv.drawString(2 * cm, H - 6.0 * cm, "Vorbereitung auf die Stunde „Schock“ · Dauer: etwa 60 Minuten")
    groesse = 13 * cm
    x0, y0 = (B - groesse) / 2, H - 6.8 * cm - groesse
    m = groesse / N
    cv.setFillColorRGB(1, 1, 1); cv.rect(x0, y0, groesse, groesse, stroke=0, fill=1)
    cv.setFillColorRGB(15 / 255, 26 / 255, 34 / 255)
    for r, c in dunkel:
        cv.rect(x0 + (c + RUHEZONE) * m, y0 + groesse - (r + RUHEZONE + 1) * m, m + 0.2, m + 0.2, stroke=0, fill=1)
    cv.setStrokeColorRGB(0.85, 0.88, 0.9); cv.setLineWidth(1)
    cv.roundRect(x0 - 0.3 * cm, y0 - 0.3 * cm, groesse + 0.6 * cm, groesse + 0.6 * cm, 12, stroke=1, fill=0)
    y = y0 - 1.6 * cm
    schritte = ["Handykamera öffnen und auf den Code richten.", "Den angezeigten Link antippen.",
                "Die Module der Reihe nach bearbeiten.", "Am Ende den Lernnachweis-Code notieren."]
    for i, text in enumerate(schritte, 1):
        cv.setFillColorRGB(*rot); cv.circle(2.45 * cm, y + 0.17 * cm, 0.38 * cm, stroke=0, fill=1)
        cv.setFillColorRGB(1, 1, 1); cv.setFont(fett, 12); cv.drawCentredString(2.45 * cm, y + 0.03 * cm, str(i))
        cv.setFillColorRGB(*tinte); cv.setFont(sans, 14); cv.drawString(3.3 * cm, y, text)
        y -= 1.05 * cm
    cv.setFillColorRGB(*grau); cv.setFont(sans, 9.5)
    cv.drawString(2 * cm, 1.8 * cm, "Kein Handy zur Hand? Link im Browser öffnen:")
    cv.setFont(mono, 10); cv.setFillColorRGB(*tinte)
    cv.drawString(2 * cm, 1.3 * cm, url)
    cv.showPage()
    cv.save()


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else adresse_aus_git()
    n, dunkel = matrix(url)
    os.makedirs(os.path.dirname(PNG), exist_ok=True)
    seite_aktualisieren(url, n, dunkel)
    png_schreiben(n, dunkel)
    pdf_schreiben(url, n, dunkel)
    print("QR-Code für", url, "eingesetzt:")
    for p in (SEITE, PNG, PDF):
        print("  ", os.path.relpath(p, WURZEL))


if __name__ == "__main__":
    main()
