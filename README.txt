Author: Omar El Miloudi 02/21/2025

Wells Production Visualization & Prediction System

Welcome to the Wells Production Visualization & Prediction project! This repository contains a complete, end-to-end system for visualizing U.S. oil & gas well data, analyzing production trends, and predicting future production levels based on user-defined parameters. The solution consists of:

1. A front-end (HTML/CSS/JavaScript) for data visualization and user interaction.
2. A Flask-based backend (Python) exposing RESTful API endpoints.
3. A machine learning pipeline for predicting future oil and gas production (using Random Forest Regressors).
4. A PostgreSQL database (hosted on Google Cloud) that stores well data.

Below is a detailed overview of the system’s architecture, code structure, API endpoints, ML model pipeline, and usage instructions.


Table of Contents
-----------------
1. System Architecture
2. Technology Stack
3. File Structure
4. API Endpoints
5. Machine Learning Pipeline
6. Usage Instructions


1. System Architecture
----------------------
The system consists of three main layers:

1. Front-End (Client Layer)
   - Built with HTML, CSS, and JavaScript.
   - Utilizes Chart.js for data visualizations and Leaflet.js for an interactive map.
   - Fetches data from Flask API endpoints and displays charts (line charts, bar charts) and map markers for relevant well information.

2. Backend (Application Layer)
   - Flask (Python) server that serves as a RESTful API.
   - Handles requests for data (historical production, wells per state, most/least producing states, map markers) and orchestrates the machine learning predictions.
   - Connects to the PostgreSQL database for data retrieval and updates.

3. Database & ML Pipeline (Data Layer)
   - A PostgreSQL database stores all well production data (oil/gas/wells, by state and year).
   - The modeltrain.py script trains two Random Forest Regressors (for oil and gas predictions) and saves them as serialized pickle files.
   - The Flask application loads these trained models on startup and uses them for prediction whenever the user requests it.


2. Technology Stack
-------------------
- Python (Flask, psycopg2, scikit-learn, pickle)
- JavaScript (Chart.js, Leaflet.js, Fetch API)
- HTML5/CSS3 (Bootstrap for layout, custom styles)
- PostgreSQL (Data storage; can be hosted on Google Cloud SQL or locally)
- RandomForestRegressor (Scikit-learn for the ML model)


3. File Structure
-----------------
Below is an overview of the key files in this repository:

  .
  ├── app.py                   # Main Flask application & API endpoints
  ├── modeltrain.py            # Script for data fetching, preprocessing, and ML model training
  ├── random_forest_oil.pkl    # Trained RandomForest model for oil production (generated after training)
  ├── random_forest_gas.pkl    # Trained RandomForest model for gas production (generated after training)
  ├── index.html               # Main HTML front-end
  ├── style.css                # Custom CSS styles
  ├── script.js                # Front-end logic, fetches data from Flask API & renders charts/maps
  └── README.md                # This README


4. API Endpoints
-----------------
The Flask server (in app.py) exposes the following endpoints:

GET /api/trends:
   - Purpose: Returns historical oil production trends by year.
   - Response: An array of objects with the structure: [ { "year": 2000, "total_oil_production": 12345 }, { "year": 2001, "total_oil_production": 23456 }, ... ]

GET /api/wells-per-state:
   - Purpose: Retrieves the total number of wells per state.
   - Response: Array of objects listing each state and total_wells. [ { "state": "Texas", "total_wells": 100 }, { "state": "Colorado", "total_wells": 80 }, ... ]

GET /api/most-least-producing:
   - Purpose: Returns the top 5 most producing and bottom 5 least producing states (by total oil production).
   - Response: JSON object with two arrays, most_producing and least_producing, each containing [state, total_oil_production]. { "most_producing": [ ["Texas", 98765], ["Oklahoma", 87654], ... ], "least_producing": [ ["StateX", 123], ... ] }

GET /api/map-data:
   - Purpose: Provides geographic data (lat/lon) and well production for each state, for display on the interactive Leaflet map.
   - Response: An array of state objects: [ { "state": "Texas", "total_wells": 100, "avg_production": 12345.6, "lat": 31.0, "lon": -99.0 }, ... ]

POST /api/predict-well-performance:
   - Purpose: Predicts future oil and gas production based on user-provided year and expected total wells.
   - Request Body (JSON): { "year": 2025, "total_wells": 150 }
   - Response: { "year": 2025, "total_wells": 150, "predicted_oil_production": 12345.67, "predicted_gas_production": 2345.67 }


5. Machine Learning Pipeline
-----------------
The ML pipeline is implemented in modeltrain.py:

Data Fetching:
   - Connects to PostgreSQL (hosted on Google Cloud) (using psycopg2).
   - Runs a SQL query to retrieve well data (year, total wells, annual oil production, annual gas production) for 2000–2023.
   - Loads results into a Pandas DataFrame.

Data Preprocessing:
   - Removes rows with missing values.
   - Renames columns to standardized names.
   - Splits the DataFrame into features X = [Year, Total_Wells] and two target series y_oil / y_gas for production predictions.

Model Training:
   - Splits data into train/test sets (80/20).
   - Trains two RandomForestRegressor models:
      - oil_model for annual oil production.
      - gas_model for annual gas production.
   - Evaluates each using mean absolute error (MAE).

Model Serialization:
   - Saves both trained models (oil_model and gas_model) as random_forest_oil.pkl and random_forest_gas.pkl.

Inference:
   - During runtime (inside app.py), these pickle files are loaded, and the trained models make predictions via the /api/predict-well-performance endpoint.


6. Usage Instructions
-----------------
1. View Production Trends:
   - On page load, you’ll see a “Total Oil Production Over Time” line chart and a “Wells Per State” bar chart.

2. Most & Least Producing States:
   - Scroll down to see bar charts for the top 5 most producing states and bottom 5 least producing states.

3. Interactive Map:
   - Click “Toggle Interactive Map” to display a Leaflet map with markers for each state. Each marker shows the total wells and average production in the popup.

4. Predict Well Performance:
   - In the “Predict Well Performance” section, enter:
      - A future year (>= 2024).
      - An expected total wells count.
   - Click “Predict” to see the estimated annual oil & gas production.
