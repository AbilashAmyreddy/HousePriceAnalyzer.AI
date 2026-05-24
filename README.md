# 🏙️ HousePrice.AI

HousePrice.AI is an AI-powered real estate price prediction platform that estimates residential property prices using machine learning and real-time market data. The project combines structured housing datasets with live web-scraped property listings to provide smarter and more realistic property price analysis.

The system uses a Gradient Boosting Regression model trained on the Bengaluru House Price Dataset to predict property values based on important features such as:

* Location
* Total Area (sqft)
* BHK Configuration
* Number of Bathrooms

In addition to predictive analytics, the platform integrates web scraping to fetch current property listings from real estate websites, allowing users to compare predicted prices with live market trends.

---

# ✨ Features

* AI-powered house price prediction
* Real-time property listing integration
* Web scraping for live market data
* Interactive premium Streamlit dashboard
* Price range & confidence estimation
* Data visualization & market insights
* Responsive modern UI

---

# 📸 App Preview

The screenshots below show the main flow of the app, from the landing section to predictions, analytics, and live market listings.

## Home / Project Snapshot

![HousePrice.AI landing page](App_Previews/Screenshot%20%28227%29.png)

## Prediction Studio

![House price prediction form and result view](App_Previews/Screenshot%20%28228%29.png)

## Market Insights

![Top locations chart and analytics dashboard](App_Previews/Screenshot%20%28229%29.png)

## Live Listings

![Live market listings fetched from real estate sources](App_Previews/Screenshot%20%28230%29.png)

---

# 🧠 Machine Learning Model

* Algorithm: Gradient Boosting Regressor (GBR)
* Dataset: Bengaluru House Price Dataset (Kaggle)
* Features Used:

  * Location
  * Area
  * BHK
  * Bathrooms
* Encoding: One-Hot Encoding
* Price Transformation: Log1p → Expm1

---

# 🛠️ Tech Stack

## Frontend

* Streamlit

## Backend / ML

* Python
* Scikit-learn
* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn

## Web Scraping

* BeautifulSoup

---

# 📊 Data Insights

The project includes multiple visualizations such as:

* Price Distribution
* Area vs Price Analysis
* BHK vs Price Trends
* Correlation Heatmaps
* Top Expensive Locations

---

# 🌐 Live Market Integration

HousePrice.AI fetches current property listings using web scraping to compare:

* Predicted prices
* Live market prices
* Property trends

This helps improve the practical relevance of the system.

---

# 🚀 How to Run

## Install Dependencies


pip install -r requirements.txt


## Start the Application


streamlit run app.py


---

# 📁 Dataset

Bengaluru House Price Dataset from Kaggle.

---

# 👨‍💻 Author

Abilash Amyreddy

Minor Project — AI & Machine Learning
