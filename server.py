from flask import Flask, render_template, request, jsonify
import json
import os
from models import db, Phrase, Example
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

with app.app_context():
     db.create_all()

DATA_FILE = "user_data.json"

def initialize_data_file():
     """Ensure the JSON file exists before running the server."""
     if not os.path.exists(DATA_FILE):
          with open(DATA_FILE, "w") as file:
               json.dump([], file, indent=4)

def load_existing_data():
     """Load existing data from JSON file."""
     if os.path.exists(DATA_FILE):
          with open(DATA_FILE, "r") as file:
               try:
                    return json.load(file)
               except json.JSONDecodeError:
                    return []
     return []

def initialize_json_data_to_database():
     with app.app_context():
          a = load_existing_data()
          for i in a:
               phrase = Phrase(phrase=i["phrase"], meaning=i["meaning"], phrase_type=i["phrase_type"], note=i["note"])
               db.session.add(phrase)
               db.session.commit()
               for example in i["example"]:
                    example_entry = Example(content=example, phrase_id=phrase.id)
                    db.session.add(example_entry)
                    db.session.commit()

def save_data(new_data):
     """Save only 'phrase' and 'example' if it's not a duplicate phrase."""
     data = load_existing_data()

     # Extract only required keys (without changing case)
     phrase = new_data.get("phrase", "").strip()
     example = new_data.get("example", "").strip()
     phrase_type = new_data.get("phrase_type", "").strip()
     meaning = new_data.get("meaning", "").strip()
     note = new_data.get("note", "").strip()

     if not phrase or not example:
          return {"error": "Invalid data! Both 'phrase' and 'example' are required."}, 400

     print("New Entry:", phrase, example)  

     for entry in data:
          if entry["phrase"].strip() == phrase:
               print("FOUND DUPLICATE")
               return False

     # Split example sentences into a list based on newline (\n)
     example_list = [sentence.strip() for sentence in example.split('\n') if sentence.strip()]
     
     data.append({"phrase": phrase, "meaning": meaning, "phrase_type": phrase_type, "example": example_list, "note": note})
     
     with open(DATA_FILE, "w") as file:
          json.dump(data, file, indent=4)
     
     return True

@app.route("/")
def index():
     return render_template("index.html")

@app.route('/submit', methods=['POST'])
def receive_data():
     data = request.get_json()
     if not data:
          return jsonify({"error": "Invalid JSON"}), 400

     # Try to save data
     if save_data(data):
          return jsonify({"message": "Data saved successfully!"})
     else:
          return jsonify({"error": "Duplicate entry: This data already exists!"}), 409  # 409 Conflict

if __name__=="__main__":
     initialize_data_file()
     initialize_json_data_to_database()
     app.run("0.0.0.0",debug=True)