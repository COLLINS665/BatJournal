from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
SECRET_PASSWORD = ""
MONGO_URI = ""
# Connect to MongoDB
client = MongoClient(MONGO_URI)  # Change for MongoDB Atlas if needed
db = client["journal"]
entries_collection = db["entries"]

# Save a journal entry
@app.route('/save', methods=['POST'])
def save_entry():
    data = request.json
    if data.get("password") != SECRET_PASSWORD:
        return jsonify({"error": "Incorrect password"}), 403
    entry = {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "content": data["content"]
    }
    entries_collection.insert_one(entry)
    return jsonify({"message": "Entry saved"}), 200

# Get all entries
@app.route('/entries', methods=['POST'])
def get_entries():
    data = request.json
    if data.get("password") != SECRET_PASSWORD:
        return jsonify({"error": "Incorrect password"}), 403

    entries = list(entries_collection.find({}, {"_id": 0}))
    return jsonify(entries), 200


if __name__ == '__main__':
    app.run(debug=True)
