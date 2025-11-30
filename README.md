# 📚 PDF Wortfrequenzanalyse - Zipf-Gesetz App

Eine Web-Anwendung zur Analyse von PDF-Büchern, die Wortfrequenzen berechnet, nach dem **Zipf-Gesetz** visualisiert und die Top 5000 Wörter ausgibt. Unterstützt **Deutsch** und **Englisch**.

## 🌟 Features

- **📄 PDF Upload**: Lade PDF-Bücher bis 50MB hoch
- **🌍 Automatische Spracherkennung**: Erkennt Deutsch und Englisch
- **🔤 Intelligente Textverarbeitung**: Tokenisierung mit Stopwort-Filterung
- **📊 Zipf-Gesetz Analyse**: Visualisierung der Wortfrequenz-Verteilung
- **📈 Interaktive Grafiken**: 
  - Zipf-Gesetz Log-Log Plot (tatsächliche vs. erwartete Frequenzen)
  - Top 20 häufigste Wörter (Balkendiagramm)
  - Zipf-Abweichungen der Top 50 Wörter
- **📉 Statistische Kennzahlen**:
  - Type-Token Ratio (lexikalische Vielfalt)
  - Hapax Legomena (einmalig vorkommende Wörter)
  - Durchschnittliche Wortlänge
  - Zipf-Konstante
  - Vokabularreichweite
- **💾 Export-Funktionen**: CSV und JSON Export der Top 5000 Wörter
- **🎨 Modernes UI**: Responsive Design mit animierten Charts

## 🔬 Zipf-Gesetz

Das **Zipf-Gesetz** besagt, dass in einem Text die Häufigkeit eines Wortes umgekehrt proportional zu seinem Rang ist:

```
Frequenz × Rang ≈ Konstante
```

Oder mathematisch: `f(r) ≈ C / r`

Die App visualisiert diese Verteilung und berechnet Abweichungen vom idealen Zipf-Gesetz.

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip

### Schritte

1. **Repository klonen oder Dateien herunterladen**

2. **Abhängigkeiten installieren**:
```powershell
pip install -r requirements.txt
```

3. **App starten**:
```powershell
python app.py
```

4. **Browser öffnen**:
Navigiere zu `http://localhost:5000`

## 📖 Verwendung

1. **PDF hochladen**: Klicke auf "PDF-Datei auswählen" und wähle ein PDF-Buch
2. **Analyse starten**: Klicke auf "Analyse starten"
3. **Ergebnisse ansehen**: Die App zeigt:
   - Statistische Kennzahlen (Gesamtwörter, einzigartige Wörter, etc.)
   - Zipf-Gesetz Visualisierung
   - Top 20 häufigste Wörter
   - Zipf-Abweichungen
   - Tabelle mit Top 50 Wörtern
4. **Export**: Exportiere die Top 5000 Wörter als CSV oder JSON

## 📊 Statistiken Erklärung

- **Gesamtwörter**: Anzahl aller Wörter im Text (nach Stopwort-Filterung)
- **Einzigartige Wörter**: Anzahl unterschiedlicher Wörter
- **Type-Token Ratio (TTR)**: Verhältnis einzigartiger Wörter zu Gesamtwörtern (Maß für lexikalische Vielfalt)
- **Hapax Legomena**: Wörter, die nur einmal vorkommen
- **Hapax %**: Prozentsatz der Hapax Legomena
- **Ø Wortlänge**: Durchschnittliche Länge der Wörter in Buchstaben
- **Zipf-Konstante**: Durchschnittliches Produkt aus Rang × Frequenz (erste 100 Wörter)
- **Zipf-Abweichung**: Durchschnittliche prozentuale Abweichung vom idealen Zipf-Gesetz

## 🗂️ Projektstruktur

```
sprachlernenapp/
│
├── app.py                 # Flask Backend mit Analyse-Logik
├── templates/
│   └── index.html         # Frontend mit Visualisierungen
├── requirements.txt       # Python-Abhängigkeiten
├── README.md             # Dokumentation
└── uploads/              # Temporärer Upload-Ordner (wird erstellt)
```

## 🛠️ Technologien

**Backend**:
- Flask (Web-Framework)
- PyPDF2 (PDF-Textextraktion)
- Python Collections (Counter für Frequenzen)

**Frontend**:
- HTML5/CSS3
- JavaScript (ES6+)
- Chart.js 4.4.0 (Interaktive Grafiken)

## 📝 Beispiel-Output

Die App generiert folgende Daten für jedes analysierte Wort:
- **Rang**: Position in der Häufigkeitsliste
- **Wort**: Das Wort selbst
- **Häufigkeit**: Wie oft das Wort vorkommt
- **Zipf-Produkt**: Rang × Häufigkeit
- **Erwartete Häufigkeit**: Nach idealem Zipf-Gesetz
- **Abweichung %**: Prozentuale Abweichung vom Ideal

## 🔒 Sicherheit

- Dateigröße auf 50MB begrenzt
- Nur PDF-Dateien erlaubt
- Hochgeladene Dateien werden nach der Verarbeitung gelöscht
- Sichere Dateinamen mit `secure_filename()`

## 🌐 Sprachunterstützung

Die App unterstützt umfassende Stopwörter-Listen für:
- **Deutsch**: der, die, das, und, in, zu, etc.
- **Englisch**: the, be, to, of, and, a, etc.

Unterstützt auch Umlaute und Sonderzeichen: ä, ö, ü, ß, à, é, etc.

## 🎯 Anwendungsfälle

- **Linguistische Forschung**: Analyse von Textstrukturen
- **Sprachlernen**: Identifizierung der wichtigsten Vokabeln
- **Literaturanalyse**: Stilistische Untersuchungen
- **SEO & Content**: Keyword-Frequenzanalyse
- **Bildung**: Verständnis des Zipf-Gesetzes

## 📄 Lizenz

Dieses Projekt ist für Bildungs- und Forschungszwecke frei verwendbar.

## 🤝 Beitragen

Verbesserungsvorschläge und Erweiterungen sind willkommen!

## 📧 Support

Bei Fragen oder Problemen erstelle ein Issue oder kontaktiere den Entwickler.

---

**Viel Spaß beim Analysieren! 📚📊**
