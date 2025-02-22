Wells Production Visualization & Prediction System
=================================================

Welcome to the Wells Production Visualization & Prediction project! This repository contains a complete, end-to-end system for visualizing U.S. oil & gas well data, analyzing production trends, and predicting future production levels based on user-defined parameters. The solution consists of:

1. A front-end (HTML/CSS/JavaScript) for data visualization and user interaction.
2. A Flask-based backend (Python) exposing RESTful API endpoints.
3. A machine learning pipeline for predicting future oil and gas production (using Random Forest Regressors).
4. A PostgreSQL database (which can be hosted on Google Cloud or run locally) that stores well data.

Below is a detailed overview of the system’s architecture, code structure, API endpoints, ML model pipeline, and setup instructions (including how to host the database on Google Cloud).


Table of Contents
-----------------
1. System Architecture
2. Technology Stack
3. File Structure
4. API Endpoints
5. Machine Learning Pipeline
6. Database Hosting (Google Cloud)
7. Setup & Installation
8. Usage Instructions
9. Contributors


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

Visual Overview:

  +---------------------+            +------------------------+          +------------------------------+
  |  Front-End (Client) | <--------> |    Flask API (app.py)  | <------> |  PostgreSQL & ML Models      |
  |  (index.html, CSS,  | (HTTP/JSON)|                        | (SQL)    |  (Hosted on GCP or locally)  |
  |  script.js)         |            |                        |          |  (modeltrain.py, .pkl files) |
  +---------------------+            +------------------------+          +------------------------------+


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

...

9. Contributors
---------------
This project was built and maintained by the following team:

- Basil Agboola – ML Lead
- Tafari Dudlet – ML Engineer
- Ryan Linton – Front-End Engineer
- Wali Siddiqui – Front-End Engineer
- Omar El Miloudi – Backend Engineer and Product Lead

---

Enjoy exploring and predicting well production trends! If you have any questions or run into any issues, please open an issue or contact any of the contributors.
