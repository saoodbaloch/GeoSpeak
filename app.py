from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import deepl
import requests

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Database model to store translation history
class TranslationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.String(500), nullable=False)
    translated_text = db.Column(db.String(500), nullable=False)
    source_language = db.Column(db.String(5), nullable=False)
    target_language = db.Column(db.String(5), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Translation('{self.source_text}', '{self.translated_text}')"


# DeepL API setup
DEEPL_API_KEY = '95068060-c130-4753-8c4c-aeb5abc1f92f:fx'
translator = deepl.Translator(DEEPL_API_KEY)

# Route to render home page
@app.route('/')
def home():
    TranslationHistory.query.delete()
    db.session.commit()  
    return render_template('index.html')

# Route to handle translation requests
# Merriam-Webster API setup
MW_API_KEY = '516ab9de-bc71-4bea-a455-f39c2fc8aa25'

def fetch_definition(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MW_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        definitions = response.json()

        # Check if the response contains definitions
        if isinstance(definitions, list) and len(definitions) > 0:
            # The first entry usually has the best definition
            first_entry = definitions[0]
            if 'shortdef' in first_entry:
                return first_entry['shortdef']  # Return a list of short definitions
        return ["No definition found."]
    except requests.exceptions.RequestException as e:
        return ["Error fetching definition."]

# Modify the translate route to include definition fetching
@app.route('/translate', methods=['POST'])
def translate():
    source_text = request.form['textToTranslate']
    source_language = request.form['srcLanguage']
    target_language = request.form['destLanguage']

    try:
        # Perform translation using the DeepL API
        translated_text = translator.translate_text(source_text, source_lang=source_language, target_lang=target_language).text
        
        # Fetch the definition of the source word
        definition = fetch_definition(source_text)

        # Save the translation to the database
        translation = TranslationHistory(
            source_text=source_text, 
            translated_text=translated_text, 
            source_language=source_language, 
            target_language=target_language
        )
        db.session.add(translation)
        db.session.commit()

        return jsonify({'translated_text': translated_text, 'definition': definition})
    except deepl.DeepLException as e:
        return jsonify({'translated_text': 'Error occurred during translation.'})
    except Exception as e:
        return jsonify({'translated_text': 'An unexpected error occurred.'})

# Route to fetch translation history
@app.route('/history', methods=['GET'])
def history():
    translations = TranslationHistory.query.order_by(TranslationHistory.timestamp.desc()).all()
    return jsonify([{
        'source_text': t.source_text,
        'translated_text': t.translated_text,
        'source_language': t.source_language,
        'target_language': t.target_language,
        'timestamp': t.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for t in translations])

@app.route('/debug_db', methods=['GET'])
def debug_db():
    translations = TranslationHistory.query.all()
    return jsonify([{
        'id': t.id,
        'source_text': t.source_text,
        'translated_text': t.translated_text,
        'source_language': t.source_language,
        'target_language': t.target_language,
        'timestamp': t.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for t in translations])

# Route to fetch supported languages from DeepL API
@app.route('/languages', methods=['GET'])
def languages():
    try:
        response = requests.get('https://api.deepl.com/v2/languages', headers={'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}'})
        languages = response.json()
        return jsonify(languages)
    except Exception as e:
        print(f"Error fetching languages: {e}")
        return jsonify({'error': 'Failed to fetch languages'})
    


# Run the app and initialize the database
if __name__ == '__main__':
    # Create an application context and initialize the database
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    
    app.run(debug=True)
