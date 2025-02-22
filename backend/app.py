from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import pickle
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database connection details
DB_CONFIG = {
    "dbname": "WellsData",
    "user": "teamc-admin",
    "password": "123456",  
    "host": "127.0.0.1",   
    "port": "5432"
}

def get_db_connection():
    """Establish connection to PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


# **1️⃣ Total Oil Production Over Time**
@app.route('/api/trends', methods=['GET'])
def get_trends():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "Year", SUM("Total_Wells_Annual_Oil_Production") AS total_oil_production
                   FROM well_data GROUP BY "Year" ORDER BY "Year";"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"year": row[0], "total_oil_production": row[1]} for row in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# **2️⃣ Wells Per State**
@app.route('/api/wells-per-state', methods=['GET'])
def get_wells_per_state():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "State", SUM("Total_Wells") AS total_wells
                   FROM well_data GROUP BY "State" ORDER BY total_wells DESC;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"state": row[0], "total_wells": row[1]} for row in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# **3️⃣ Most & Least Producing States**
@app.route('/api/most-least-producing', methods=['GET'])
def get_most_least_producing():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "State", SUM("Total_Wells_Annual_Oil_Production") AS total_oil_production
                   FROM well_data GROUP BY "State" ORDER BY total_oil_production DESC;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        top_5 = data[:5]
        bottom_5 = data[-5:]
        return jsonify({"most_producing": top_5, "least_producing": bottom_5})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/map-data', methods=['GET'])
def get_map_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "State", SUM("Total_Wells") AS total_wells, 
                          AVG("Total_Wells_Annual_Oil_Production") AS avg_production, 
                          "Latitude", "Longitude"
                   FROM well_data 
                   WHERE "Latitude" IS NOT NULL AND "Longitude" IS NOT NULL 
                   GROUP BY "State", "Latitude", "Longitude";"""
        cursor.execute(query)
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "No data found in the database"}), 404  # If no data, return 404

        cursor.close()
        conn.close()
        
        # Convert data into JSON format
        response_data = []
        for row in data:
            response_data.append({
                "state": row[0],
                "total_wells": row[1],
                "avg_production": row[2],
                "lat": row[3],
                "lon": row[4]
            })

        return jsonify(response_data)  # Ensure valid JSON response

    except Exception as e:
        print("Error in /api/map-data:", str(e))  # Log error
        return jsonify({"error": str(e)}), 500

# Load trained Random Forest models
with open("random_forest_oil.pkl", "rb") as f:
    oil_model = pickle.load(f)

with open("random_forest_gas.pkl", "rb") as f:
    gas_model = pickle.load(f)

@app.route('/api/predict-well-performance', methods=['POST'])
def predict_well_performance():
    try:
        # Get JSON input
        data = request.json
        year = int(data.get("year"))  # Future year for prediction
        total_wells = int(data.get("total_wells"))  # Expected well count

        # Ensure valid inputs
        if year < 2024:
            return jsonify({"error": "Year must be 2024 or later"}), 400
        if total_wells <= 0:
            return jsonify({"error": "Total wells must be positive"}), 400

        # Prepare input for the model
        input_data = np.array([[year, total_wells]])

        # Make predictions
        oil_prediction = oil_model.predict(input_data)[0]
        gas_prediction = gas_model.predict(input_data)[0]

        # Return JSON response
        return jsonify({
            "year": year,
            "total_wells": total_wells,
            "predicted_oil_production": round(oil_prediction, 2),
            "predicted_gas_production": round(gas_prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
