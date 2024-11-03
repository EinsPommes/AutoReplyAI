# AutoReplyAI - Automatischer E-Mail-Assistent

AutoReplyAI ist ein KI-gestützter E-Mail-Assistent, der automatisch auf eingehende E-Mails antwortet. Mit Hilfe der KI "4o-mini" generiert AutoReplyAI höfliche und professionelle Antworten und spart damit Zeit und Mühe bei der Bearbeitung von E-Mails.

## Features
- **Automatische Antwort**: AutoReplyAI prüft ungelesene E-Mails und sendet automatisch eine Antwort basierend auf dem Inhalt der E-Mail.
- **KI-Unterstützung**: Die Antworten werden durch eine KI generiert, die als Assistent entwickelt wurde, um höfliche und professionelle Nachrichten zu verfassen.
- **Einfache Konfiguration**: Verwenden Sie Umgebungsvariablen für die Konfiguration von E-Mail-Konto und API-Schlüssel.

## Voraussetzungen
- Python 3.7+
- Abhängigkeiten:
  - `openai`
  - Zugang zu einem SMTP- und IMAP-Server (z.B. web.de)

## Installation
1. Klonen Sie das Repository:
   ```sh
   git clone https://github.com/EinsPommes/AutoReplyAI.git
   cd AutoReplyAI
   ```
2. Erstellen Sie eine virtuelle Umgebung und installieren Sie die erforderlichen Python-Bibliotheken:
   ```sh
   python3 -m venv venv
     source venv/bin/activate
    pip install openai imaplib2
   ```
3. Setzen Sie die erforderlichen Umgebungsvariablen:
   - `EMAIL_ACCOUNT`: Ihre E-Mail-Adresse (z.B. von web.de).
   - `EMAIL_PASSWORD`: Ihr E-Mail-Passwort.
   - `OPENAI_API_KEY`: Ihr API-Schlüssel für OpenAI.

## Verwendung
Führen Sie das Skript aus, um ungelesene E-Mails zu überprüfen und automatisch darauf zu antworten:
```sh
python autoreplyai.py
```
Das Skript überprüft die E-Mail-Inbox und sendet eine automatisch generierte Antwort an den Absender jeder ungelesenen Nachricht.

## Haftungsausschluss
Bitte achten Sie darauf, dass das Skript sensible Informationen wie E-Mail-Passwörter enthält. Verwenden Sie sichere Methoden, wie Umgebungsvariablen, um Ihre Anmeldedaten zu schützen. Überwachen Sie die Nutzung der API, da möglicherweise Kosten anfallen.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert.
