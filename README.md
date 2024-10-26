
# Delivergate Data Engineer Internship Dashboard

## Overview

This project is a **Streamlit application** designed as part of the Delivergate Data Engineer Internship assessment.
The application connects to a **MySQL database** using **SQLAlchemy** and provides interactive data processing and visualization through an intuitive web interface.
Users can import data to SQL database, explore various metrics, and even apply machine learning to predict customer behaviors. 
The app is organized into three main pages:
1. **Dashboard Page** - for data visualization and analytics.
2. **Original Data Page** - for data import and management.
3. **Machine Learning Page** - for predictive modeling.

## Features

- **Import Data**: One-click button to load data from CSV files into the MySQL database.
- **Dashboard Visualizations**: Interactive filters, bar charts, line charts, and summary metrics.
- **Machine Learning**: Predictive modeling to assess customer purchasing behavior and.
- **Enhanced UI**: The app is visually organized with easy navigation and user-friendly design.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup and Installation](#setup-and-installation)
3. [Running the App](#running-the-app)
4. [App Pages](#app-pages)
5. [Deployment on Streamlit Cloud](#deployment-on-streamlit-cloud)
6. [Technical Details](#technical-details)
7. [Contributing](#contributing)
8. [Author](#author)
9. [License](#license)

---

## Project Structure

```plaintext
streamlit_app/
├── app.py                      # Main Streamlit application
├── .streamlit/                 # Configuration
│   └── secrets.toml            # Streamlit Cloud environment variables (for deployment)
├── data/                       # Directory for CSV data files
│   ├── customers.csv           # Customer data CSV file
│   └── order.csv               # Orders data CSV file
├── db/                         # Database management
│   ├── data_import.py          # functions for data create on SQL
│   ├── db_connector.py         # MySQL connection using SQLAlchemy
│   └── filter.py               # functions related to filter data from SQL
├── pages/                      # Streamlit multipage application setup
│   ├── dashboard.py            # Page for data visualization
│   ├── data.py                 # Page for data import and management
│   └── ml.py                   # Page for machine learning model
├── ml_model.py                 # Machine learning related implementaion
├── requirements.txt            # Python package requirements
└── README.md                   # Project documentation
```

---

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/j-sathurjan/customer-order-data-analysis-streamlit.git streamlit_app
   cd streamlit_app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Connection**:
   - Set up a MySQL database named delivergate_db:
     ```sql
     CREATE DATABASE delivergate_db;
     ```

4. **Set Up `secrets.toml`**:
   - Replace the following credentials in `secrets.toml` for Streamlit Cloud deployment:
     ```toml
     [delivergate_db]
     dialect = "mysql"
     DB_HOST = "your_db_host"
     DB_USER = "your_db_user"
     DB_PASSWORD = "your_db_password"
     DB_NAME = "delivergate_db"
     ```

---

## Running the App

1. **Run Streamlit**:
   ```bash
   streamlit run app.py
   ```

2. **Access the App**:
   - Go to `http://localhost:8501` to view the app.

---

## App Pages

### 1. **Dashboard**
   - **Purpose**: Provides visual analytics and insights into customer and order data.
   - **Features**:
     - **Filters**: Date range, minimum total amount, and minimum number of orders.
     - **Data Frame**: Data frame filtered by the side bar filters displayed in two tab, Orders Data With Customers and Customers Data
       - **Orders Data With Customers** orders data filtered by date range, total spent and total orders
       - **Customers Data** customers data filtered by total spent and total orders
     - **Visualizations**:
       - **Top 10 Customers by Revenue** (Bar Chart)
       - **Revenue Over Time** (Line Chart)
     - **Summary Metrics**:
       - Total revenue
       - Number of unique customers
       - Total orders
      
### 2. **Original Data**
   - **Purpose**: Allows users to import data from `customer.csv` and `orders.csv` files into the MySQL database.
   - **Features**:
     - Single-click data import button.
     - Status messages to confirm successful data import or error handling.
     - Automated replacement of the database table.


### 3. **Machine Learning**
   - **Purpose**: Predicts customer repeat purchasing behavior.
   - **Features**:
     - Logistic regression model to classify customers as repeat purchasers.
     - Model accuracy displayed for performance insight.
     - Option to change the validation fold and retrain the model with updated data.

---

## Deployment on Streamlit Cloud

1. **Push Code to GitHub**:
   - Ensure all necessary files are added, including `app.py`, `ml_model.py`, `db/`, `pages/`, `requirements.txt`, and `README.md`.

2. **Connect to Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud).
   - Sign in with GitHub, and select your repository for deployment.

3. **Set Environment Variables**:
   - On Streamlit Cloud, add database credentials in the **Secrets** section matching the `secrets.toml` format.

4. **Deploy**:
   - Streamlit Cloud will automatically detect `requirements.txt` and deploy the app.
   - The app URL will be provided after deployment is complete.

---

## Technical Details

### Data Import Functionality
- **MySQL Integration**: SQLAlchemy is used for all database connections and queries, ensuring secure, efficient data import and retrieval.
- **One-click Import**: The Import Data button on the Original Data Page uses pandas to read CSV files and store data in the MySQL database.

### Visualizations
- **Streamlit Widgets**: Sidebar filters enable users to interactively adjust parameters for data views.
- **Chart Elements**: Generates bar and line charts for visualizing revenue trends and top customers.

### Machine Learning Model
- **Model**: A logistic regression model is used to predict repeat purchasing behavior based on customer revenue and number of orders.
- **Training**: Data is preprocessed and split within the app, allowing for real-time retraining.

---

## Contributing

Contributions to this project are welcome! Feel free to fork this repository and submit a pull request.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## Author

**Sathurjan Jeyarupan**

- LinkedIn: [linkedin.com/in/sathurjan-jeyarupan](https://www.linkedin.com/in/sathurjan-jeyarupan/)
- GitHub: [github.com/j-sathurjan](https://github.com/j-sathurjan)
- Email: j.sathurjan@gmail.com

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
