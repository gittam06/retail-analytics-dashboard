# 🛒 Retail Analytics & Recommendation Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458?style=flat-square&logo=pandas)](https://pandas.pydata.org/)

An interactive, end-to-end Exploratory Data Analysis (EDA) and Advanced Analytics dashboard built for e-commerce. This application transforms raw transactional data into actionable business intelligence, featuring automated customer segmentation and a market basket recommendation engine.

**🔴 Live Demo:** [View the Dashboard on Streamlit Cloud](https://retail-analytics-dashboard-wsjerjfp6hnkbsxcrjp2yu.streamlit.app)

---

## 🚀 Key Features

### 1. Macro Exploratory Data Analysis (EDA)
* **Real-time KPIs:** Instantly track total revenue, order volume, and unique customer count.
* **Time-Series Trending:** Interactive area charts visualizing month-over-month revenue growth.
* **Volume Drivers:** Horizontal bar charts identifying top-selling products.

### 2. RFM Customer Segmentation
* Calculates **Recency** (days since last purchase), **Frequency** (total purchases), and **Monetary** (total spend) value for every customer.
* Automatically scores and categorizes customers into actionable business segments (e.g., *Champions, Loyal Customers, At Risk, Lost*).
* Visualizes the customer base distribution using an interactive donut chart.

### 3. Market Basket Analysis (Recommendation Engine)
* Utilizes the **Apriori Algorithm** to discover hidden patterns in customer purchasing behavior.
* Generates association rules (If they buy *Product A*, recommend *Product B*).
* Filterable by country to analyze regional purchasing habits and optimized for local compute memory.

---

## 🛠️ Technology Stack

* **Front-End & App Framework:** [Streamlit](https://streamlit.io/) (with custom CSS injection)
* **Data Manipulation:** `pandas`, `openpyxl`
* **Data Visualization:** `plotly.express`
* **Machine Learning / Analytics:** `mlxtend` (Apriori & Association Rules)

---

## 💻 Run the Project Locally

To run this dashboard on your local machine, follow these steps:

**1. Clone the repository**
```bash
git clone https://github.com/gittam06/retail-analytics-dashboard.git
cd retail-analytics-dashboard
```

**2. Create and activate a virtual environment (Recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

**3. Install the dependencies**
```bash
pip install -r requirements.txt
```

**4. Add the Dataset**
Ensure the UK Online Retail dataset is named `online_retail.csv` and is placed in the root directory of the project. *(Note: The dataset is dynamically cleaned upon ingestion to handle hidden Byte Order Marks and inconsistent date formatting).*

**5. Launch the App**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
retail-analytics-dashboard/
│
├── .streamlit/
│   └── config.toml          # Global UI theme settings
├── app.py                   # Main Streamlit application and logic
├── requirements.txt         # Python dependencies
├── online_retail.csv        # The raw e-commerce dataset (Add locally)
└── README.md                # Project documentation
```

---

## 🧠 Business Value & Logic

This platform is designed to answer three critical business questions:
1. **How is the business performing overall?** (Macro EDA)
2. **Who are our most valuable customers, and who is churning?** (RFM Analysis)
3. **How can we increase the average order value?** (Market Basket Analysis)

By moving away from static spreadsheets and into an interactive web app, stakeholders can dynamically filter and explore data without needing to write a single line of code.
