from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import os
import re
from collections import Counter
import math
import io
import csv
import json
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Stopwörter für Deutsch und Englisch
STOPWORDS_DE = set([
    'der', 'die', 'das', 'und', 'in', 'zu', 'den', 'mit', 'von', 'ist', 'auf', 
    'für', 'im', 'dem', 'des', 'eine', 'ein', 'als', 'sich', 'an', 'nicht', 
    'auch', 'werden', 'aus', 'er', 'sie', 'es', 'bei', 'oder', 'um', 'war',
    'werden', 'hat', 'sind', 'ich', 'du', 'wir', 'ihr', 'aber', 'so', 'wenn',
    'noch', 'nur', 'nach', 'bis', 'über', 'durch', 'kann', 'sein', 'diese',
    'zum', 'zur', 'am', 'vom', 'einen', 'einem', 'einer', 'eines', 'wurde',
    'mehr', 'wie', 'was', 'alle', 'sein', 'haben', 'hatte', 'wurden'
])

STOPWORDS_EN = set([
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it',
    'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but',
    'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will',
    'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
    'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can',
    'like', 'time', 'no', 'just', 'him', 'know', 'take', 'into', 'year', 'your',
    'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look',
    'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use',
    'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
    'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'was', 'are',
    'been', 'has', 'had', 'were', 'said', 'did', 'having', 'may', 'should'
])


def extract_text_from_pdf(pdf_path):
    """Extrahiert Text aus PDF"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        raise Exception(f"Fehler beim PDF-Lesen: {str(e)}")
    return text


def detect_language(text):
    """Einfache Spracherkennung basierend auf häufigen Wörtern"""
    words = text.lower().split()[:1000]  # Erste 1000 Wörter
    de_count = sum(1 for w in words if w in STOPWORDS_DE)
    en_count = sum(1 for w in words if w in STOPWORDS_EN)
    return 'de' if de_count > en_count else 'en'


def tokenize_and_clean(text, language):
    """Tokenisiert Text und entfernt Stopwörter"""
    # Nur Buchstaben und Apostrophe behalten
    text = text.lower()
    words = re.findall(r"[a-zäöüßàâçéèêëîïôûùüÿœæ]+(?:'[a-zäöüß]+)?", text, re.IGNORECASE)
    
    # Stopwörter entfernen
    stopwords = STOPWORDS_DE if language == 'de' else STOPWORDS_EN
    filtered_words = [w for w in words if w not in stopwords and len(w) > 1]
    
    return filtered_words


def calculate_zipf_analysis(word_counts, top_n=5000):
    """Berechnet Zipf-Gesetz Analyse"""
    sorted_words = word_counts.most_common(top_n)
    
    # Zipf-Gesetz: rank × frequency ≈ constant
    zipf_data = []
    for rank, (word, freq) in enumerate(sorted_words, 1):
        zipf_product = rank * freq
        expected_freq = sorted_words[0][1] / rank  # Ideales Zipf-Gesetz
        deviation = abs(freq - expected_freq) / expected_freq * 100
        
        zipf_data.append({
            'rank': rank,
            'word': word,
            'frequency': freq,
            'zipf_product': zipf_product,
            'expected_frequency': round(expected_freq, 2),
            'deviation_percent': round(deviation, 2)
        })
    
    return zipf_data


def calculate_statistics(words, word_counts, zipf_data):
    """Berechnet statistische Kennzahlen"""
    total_words = len(words)
    unique_words = len(word_counts)
    
    # Type-Token Ratio (lexikalische Vielfalt)
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Hapax Legomena (Wörter, die nur einmal vorkommen)
    hapax_legomena = sum(1 for count in word_counts.values() if count == 1)
    hapax_percentage = hapax_legomena / unique_words * 100 if unique_words > 0 else 0
    
    # Durchschnittliche Wortlänge
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
    
    # Zipf-Konstante (Durchschnitt der rank × frequency Produkte)
    zipf_constant = sum(item['zipf_product'] for item in zipf_data[:100]) / min(100, len(zipf_data))
    
    # Durchschnittliche Abweichung vom Zipf-Gesetz
    avg_zipf_deviation = sum(item['deviation_percent'] for item in zipf_data[:100]) / min(100, len(zipf_data))
    
    # Vokabulargröße für verschiedene Frequenzschwellen
    vocab_levels = {
        'top_10': len([w for w, c in word_counts.most_common() if c >= word_counts.most_common(10)[-1][1]]),
        'top_100': len([w for w, c in word_counts.most_common() if c >= word_counts.most_common(min(100, len(word_counts)))[-1][1]]),
        'top_1000': len([w for w, c in word_counts.most_common() if c >= word_counts.most_common(min(1000, len(word_counts)))[-1][1]]),
    }
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'type_token_ratio': round(ttr, 4),
        'hapax_legomena': hapax_legomena,
        'hapax_percentage': round(hapax_percentage, 2),
        'avg_word_length': round(avg_word_length, 2),
        'zipf_constant': round(zipf_constant, 2),
        'avg_zipf_deviation': round(avg_zipf_deviation, 2),
        'vocab_levels': vocab_levels
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'Keine PDF-Datei hochgeladen'}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Nur PDF-Dateien erlaubt'}), 400
    
    try:
        # Datei speichern
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Text extrahieren
        text = extract_text_from_pdf(filepath)
        
        # Sprache erkennen
        language = detect_language(text)
        
        # Tokenisierung und Bereinigung
        words = tokenize_and_clean(text, language)
        
        # Worthäufigkeiten zählen
        word_counts = Counter(words)
        
        # Zipf-Analyse (Top 5000)
        zipf_data = calculate_zipf_analysis(word_counts, top_n=min(5000, len(word_counts)))
        
        # Statistiken berechnen
        statistics = calculate_statistics(words, word_counts, zipf_data)
        statistics['detected_language'] = 'Deutsch' if language == 'de' else 'Englisch'
        
        # Aufräumen
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'statistics': statistics,
            'top_words': zipf_data[:50],  # Top 50 für Vorschau
            'zipf_plot_data': {
                'ranks': [item['rank'] for item in zipf_data[:500]],
                'frequencies': [item['frequency'] for item in zipf_data[:500]],
                'expected': [item['expected_frequency'] for item in zipf_data[:500]]
            },
            'all_words': zipf_data  # Alle Top 5000 für Export
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export/<format>', methods=['POST'])
def export_words(format):
    """Exportiert die Top 5000 Wörter als CSV oder JSON"""
    data = request.json.get('words', [])
    
    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Rang', 'Wort', 'Häufigkeit', 'Zipf-Produkt', 'Erwartete Häufigkeit', 'Abweichung %'])
        
        for item in data:
            writer.writerow([
                item['rank'],
                item['word'],
                item['frequency'],
                item['zipf_product'],
                item['expected_frequency'],
                item['deviation_percent']
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='word_frequency_top5000.csv'
        )
    
    elif format == 'json':
        output = json.dumps(data, ensure_ascii=False, indent=2)
        return send_file(
            io.BytesIO(output.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name='word_frequency_top5000.json'
        )
    
    return jsonify({'error': 'Ungültiges Format'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
