Bengaluru Real Estate Price Prediction
An end-to-end Machine Learning regression project that processes raw real estate data from Bengaluru, cleans and transforms complex features, handles statistical and domain-specific outliers, and predicts property prices using Scikit-Learn.
📌 Project OverviewPredicting real estate prices is challenging due to inconsistent data entries, high-cardinality categorical attributes (e.g., hundreds of unique locations), and structural outliers.This project demonstrates a complete data science workflow using the Bengaluru House Prices dataset (~13,320 initial records). It covers raw data extraction, missing value imputation, text parsing, categorical aggregation, statistical outlier filtering, one-hot encoding, and predictive modeling using Linear Regression.
🛠️ Key Technical HighlightsData Wrangling & Cleaning: Dropped uninformative features, imputed missing values using statistical medians, and parsed inconsistent string formats (e.g., converting square footage ranges like '1133 - 1384' to arithmetic means).Feature Engineering: Extracted numerical values for bedrooms/bhk from textual descriptions and created a standardized price_per_sqft metric to evaluate property values uniformly.Dimensionality Reduction: Cleaned whitespace and grouped infrequent locations ($\le 10$ occurrences) into an 'other' category—reducing unique locations from 1,287 down to 241 (over 80% reduction in high-cardinality noise).Outlier Removal: Applied domain-specific rules (minimum 300 sqft per room) and statistical filtering ($\mu \pm 1\sigma$ on price_per_sqft) to eliminate anomalous pricing data.Model Training & Evaluation: Trained a Linear Regression model on unseen test data, achieving an $R^2$ score of ~83.9%.
📂 Project Structure.
├── dataset/
│   └── Bengaluru_House_Data.csv
├── Bengaluru_House_Price_Prediction.ipynb
└── README.md
🚀 Technologies & Libraries UsedLanguage: Python 3.xData Manipulation: Pandas, NumPyMachine Learning: Scikit-Learn (LinearRegression, train_test_split)
Environment: Jupyter Notebook / Google Colab📊 Dataset InformationDataset: Bengaluru House Prices DatasetInitial Size: 13,320 rows × 9 columnsTarget Variable: price (in Lakhs)
📈 Model PerformanceModelEvaluation MetricScoreLinear Regression$R^2$ Score (Test Set)0.8388 (83.9%)
⚙️ How to RunClone the Repository:git clone https://github.com/your-username/bengaluru-house-price-prediction.git
cd bengaluru-house-price-prediction
Install Dependencies:pip install numpy pandas scikit-learn jupyter
Launch Jupyter Notebook:jupyter notebook Bengaluru_House_Price_Prediction.ipynb
