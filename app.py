from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__)

# Fetch MongoDB URI from environment variable
# Ensure the URI includes credentials if authentication is required
mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://username:password@mongodb:27017/flask_db")

# Set up the MongoDB client with authentication
client = MongoClient(mongodb_uri)

# Connect to the database named 'flask_db'
db = client.flask_db

# Connect to the collection named 'data' within the 'flask_db' database
collection = db.data

# Define the route for the root URL
@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

# Define the route for the '/data' endpoint
@app.route('/data', methods=['GET', 'POST'])
def data():
    try:
        if request.method == 'POST':
            # Get the JSON data from the request
            data = request.get_json()
            # Insert the data into the 'data' collection in MongoDB
            collection.insert_one(data)
            # Return a success message
            return jsonify({"status": "Data inserted"}), 201
        elif request.method == 'GET':
            # Retrieve all documents from the 'data' collection
            # Convert the documents to a list, excluding the '_id' field
            data = list(collection.find({}, {"_id": 0}))
            # Return the data as a JSON response
            return jsonify(data), 200
    except Exception as e:
        # Return detailed error information in case of failure
        return jsonify({"error": str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
