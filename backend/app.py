from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.data_loader.loader import DatasetLoader

app = Flask(__name__, static_folder='../ui/ui/dist', static_url_path='/')
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.filename.endswith(".parquet"):
                df = pd.read_parquet(file)
            else:
                return jsonify({"error": "Unsupported file type"}), 400

            # Store the dataframe in a global variable for simplicity
            # In a real application, you would use a more robust solution
            global dataframe
            dataframe = df

            return jsonify({"message": "File uploaded successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/api/connect", methods=["POST"])
def connect_database():
    data = request.get_json()
    db_type = data.get("db_type")
    host = data.get("host")
    port = data.get("port")
    database = data.get("database")
    user = data.get("user")
    password = data.get("password")
    table = data.get("table")

    try:
        conn_str = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
        loader = DatasetLoader()
        df = loader.load_sql(conn_str, table)

        global dataframe
        dataframe = df

        return jsonify({"message": "Connected to the database and loaded the data!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")

    global dataframe
    if dataframe is None:
        return jsonify({"error": "No data loaded"}), 400

    try:
        llm = OpenAI()
        sdf = SmartDataframe(dataframe, config={"llm": llm})
        response = sdf.chat(query)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
