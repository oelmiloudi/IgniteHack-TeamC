import pandas as pd
import psycopg2
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from dotenv import load_dotenv
import os

# Load environment variables from credentials.env
load_dotenv("credentials.env")

# Database connection details
DB_CONFIG = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT")
}

# Connect to PostgreSQL and fetch data
def fetch_well_data():
    conn = psycopg2.connect(**DB_CONFIG)
    query = """SELECT 
                   CAST(TRIM("Year") AS INTEGER) AS year, 
                   "Total_Wells", 
                   "Total_Wells_Annual_Oil_Production", 
                   "Total_Wells_Annual_Gas_Production"
               FROM public.well_data 
               WHERE "Year" ~ '^[0-9]+$' 
               AND CAST(TRIM("Year") AS INTEGER) BETWEEN 2000 AND 2023;"""
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Print column names to verify
    print("Columns in DataFrame:", df.columns)
    
    return df

# Load data
df = fetch_well_data()

# Data preprocessing
df.rename(columns={"year": "Year"}, inplace=True)
df = df.dropna()  # Remove rows with missing values

# Split into features (X) and targets (Y)
X = df[["Year", "Total_Wells"]]
y_oil = df["Total_Wells_Annual_Oil_Production"]
y_gas = df["Total_Wells_Annual_Gas_Production"]

# Train-test split
X_train, X_test, y_oil_train, y_oil_test = train_test_split(X, y_oil, test_size=0.2, random_state=42)
X_train, X_test, y_gas_train, y_gas_test = train_test_split(X, y_gas, test_size=0.2, random_state=42)

# Train Random Forest models
oil_model = RandomForestRegressor(n_estimators=100, random_state=42)
oil_model.fit(X_train, y_oil_train)

gas_model = RandomForestRegressor(n_estimators=100, random_state=42)
gas_model.fit(X_train, y_gas_train)

# Evaluate model performance
oil_mae = mean_absolute_error(y_oil_test, oil_model.predict(X_test))
gas_mae = mean_absolute_error(y_gas_test, gas_model.predict(X_test))

# Save models for later use in the Flask API
with open("random_forest_oil.pkl", "wb") as f:
    pickle.dump(oil_model, f)

with open("random_forest_gas.pkl", "wb") as f:
    pickle.dump(gas_model, f)

print(f"Oil Model MAE: {oil_mae}")
print(f"Gas Model MAE: {gas_mae}")
