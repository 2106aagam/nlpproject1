# NLP Sentiment Analyzer — Aagam

A beginner-friendly college project that demonstrates Natural Language Processing (NLP) through a web application.

## Features
- Enter a sentence/review and analyze sentiment.
- Positive / Neutral / Negative classification.
- Simple confidence indicator.
- Word count.
- Analysis history stored in SQLite.
- Clear history button.
- Responsive modern UI.
- About page explaining NLP.

## NLP concepts demonstrated
1. Tokenization — splitting text into words.
2. Normalization — converting text to lowercase.
3. Lexicon-based sentiment scoring.
4. Negation handling — e.g. "not good".
5. Basic intensity handling — e.g. "very good".
6. Classification into Positive, Neutral, or Negative.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Internet only for installing Flask

## Run on Windows

Open PowerShell in this project folder:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Project presentation points
Title: NLP Sentiment Analyzer

Problem:
Manually understanding the emotional tone of many reviews or comments takes time.

Solution:
The application uses NLP preprocessing and a sentiment lexicon to classify text.

Future scope:
- Train a machine-learning model using a real labeled dataset.
- Add multilingual sentiment analysis.
- Add charts and analytics.
- Use transformer models such as BERT.
- Add user authentication.

Note:
The displayed "confidence" is a normalized score from this educational rule-based model; it is not a calibrated probability.
