import requests
from bs4 import BeautifulSoup

# this function returns a soup page object
def getPage(url):

    # Webseite laden
    r = requests.get(url)
    data = r.text

    # parsen und zurück geben
    spobj = BeautifulSoup(data, "lxml")
    return spobj


def get_heise_headers(thema):

    # Heise-Webseite zum Thema "https" laden und mit BS4 parsen
    url = "https://www.heise.de/thema/" + thema
    page = getPage(url)

    # Liste der Anchors im <div class=keywordliste> Tag finden
    keywordliste = page.find("div", { "class": "keywordliste" })
    anchors = keywordliste.findAll("a")

    # Überschriften extrahieren
    headers = []
    for a in anchors:
        header = a.find("header")
        headers.append(str(header.string).strip())

    # Überschrifen zurück geben
    return headers


def analyze_top_3_words(headers):

    # Wortliste bauen
    words = []
    for header in headers:
        words += [word.rstrip(':') for word in header.split()]

    # Wörter zählen
    wordcounts = [words.count(word) for word in words]

    # Wort-Frequenzpaare bilden und deduplizieren
    wordfreq = dict(zip(words, wordcounts))

    # Frequenz-Wortpaare bilden und sortieren
    freqword = [(wordfreq[word], word) for word in wordfreq]
    freqword.sort()
    freqword.reverse()

    # Top-3 zurück geben
    return freqword[:3]


def main():
    # Überschriften zum Thema "https" von der Heise-Seite holen
    headers = get_heise_headers(thema = "https")

    print('Heise-Überschriften zum Thema "https":')
    for header in headers:
        print('\t' + header)

    # Wortliste bauen, Wörter zählen, sortieren, Top-3 zurück geben
    top_3 = analyze_top_3_words(headers)

    print('Top-3 Wörter in den Heise-Überschriften zum Thema "https":')
    for freq, word in top_3:
        print('\t{} ({}x)'.format(word, freq))


# Hauptroutine aufrufen
if __name__ == '__main__':
    main()
