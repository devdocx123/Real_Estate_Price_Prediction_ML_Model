# Bengaluru Real Estate Price Prediction

An end-to-end Machine Learning regression project that processes raw real estate data from Bengaluru, cleans and transforms complex features, and predicts housing prices using Scikit-Learn.

---

## 📌 Project Overview

Predicting real estate prices is challenging due to inconsistent data entries, high-cardinality categorical attributes, and severe outliers. This project demonstrates a complete data science workflow using the Bengaluru House Prices dataset (~13,320 initial records). It covers raw data extraction, custom preprocessing, statistical outlier filtering, one-hot encoding, and predictive modeling using Linear Regression.

---

## 🛠️ Key Technical Highlights

* Data Wrangling & Cleaning: Dropped uninformative features (area_type, availability, society, balcony), imputed missing bathroom values using statistical medians (2.0), and parsed non-standard inputs (e.g., converting range strings like '1133 - 1384' into arithmetic means).
* Feature Engineering: Extracted numerical values for bedrooms/BHK from textual descriptions and created a custom price_per_sqft metric to standardize property values uniformly across square footage sizes.
* Dimensionality Reduction: Cleaned leading/trailing whitespace and grouped infrequent locations (<= 10 occurrences) into a unified 'other' category, reducing categorical feature space by over 80% (cutting unique locations from 1,287 down to 241).
* Domain-Specific Outlier Removal: Applied real estate domain constraints to eliminate unrealistic entries where square footage per bedroom was less than 300 sqft.
* Statistical Filtering: Performed location-based standard deviation filtering (mean ± 1 std dev) on price_per_sqft to eliminate extreme pricing anomalies across distinct neighborhood clusters.
* Model Training & Evaluation: One-hot encoded categorical features and trained a Linear Regression model on unseen test data, achieving an R^2 accuracy score of ~83.9%.

---

## 📁 Project Structure

├── dataset/
│   └── Bengaluru_House_Data.csv
├── Bengaluru_House_Price_Prediction.ipynb
└── README.md

---

## 🚀 Technologies & Libraries Used

* Language: Python 3.x
* Data Processing: Pandas, NumPy
* Machine Learning: Scikit-Learn (LinearRegression, train_test_split)
* Environment: Jupyter Notebook / Google Colab

---

## 📊 Dataset & Model Performance

* Dataset Source: Bengaluru House Prices Dataset
* Initial Size: 13,320 rows × 9 columns
* Target Variable: price (in Lakhs INR)
* Final Model Metric: R^2 Score = 0.8388 (~83.9%)

---

## ⚡ Quickstart Guide

1. Clone the Repository:
   git clone https://github.com/your-username/bengaluru-real-estate-prediction.git
   cd bengaluru-real-estate-prediction

2. Install Dependencies:
   pip install numpy pandas scikit-learn jupyter

3. Run the Notebook:
   jupyter notebook Bengaluru_House_Price_Prediction.ipynb
