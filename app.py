import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Set page configuration FIRST
st.set_page_config(page_title="Retail Analytics Platform", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# UI & STYLING INJECTION
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Smooth scrolling for the whole page */
        html {
            scroll-behavior: smooth;
        }
        /* Make the top padding smaller so the app feels more compact */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Style the metric cards */
        div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 5% 10% 5% 10%;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        /* Hide the default Streamlit footer and hamburger menu for a clean look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# MODULE A: Data Ingestion & Cleaning
# ==========================================
@st.cache_data
def load_and_clean_data(filepath="online_retail.csv"):
    try:
        df = pd.read_csv(filepath, encoding="ISO-8859-1")
        
        # Remove hidden Byte Order Marks (BOM)
        df.columns = df.columns.str.replace('ï»¿', '').str.replace('\ufeff', '')
        
        df = df.dropna(subset=['CustomerID'])
        df = df[df['Quantity'] > 0]
        df['Total_Sales'] = df['Quantity'] * df['UnitPrice']
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed', dayfirst=True)
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
        
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'online_retail.csv' is in the same directory.")
        return pd.DataFrame()

# ==========================================
# MODULE B: Macro EDA (Dashboard)
# ==========================================
def render_macro_eda(df):
    st.markdown("## 📈 Macro Exploratory Data Analysis")
    st.markdown("---")
    
    # 1. KPI Metric Cards
    total_revenue = df['Total_Sales'].sum()
    total_orders = df['InvoiceNo'].nunique()
    total_customers = df['CustomerID'].nunique()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="💰 Total Revenue", value=f"£{total_revenue:,.2f}")
    kpi2.metric(label="📦 Total Orders", value=f"{total_orders:,}")
    kpi3.metric(label="👥 Unique Customers", value=f"{total_customers:,}")
    
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    
    # 2. Charts
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_revenue = df.groupby('YearMonth')['Total_Sales'].sum().reset_index()
        fig_revenue = px.area(monthly_revenue, x='YearMonth', y='Total_Sales', 
                              title="Total Revenue Trend", template="plotly_white")
        fig_revenue.update_traces(line_color='#2E86C1', fillcolor='rgba(46, 134, 193, 0.2)')
        st.plotly_chart(fig_revenue, use_container_width=True)
        
    with col2:
        top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_products = px.bar(top_products, x='Quantity', y='Description', 
                              orientation='h', title="Top Products by Volume", template="plotly_white",
                              color='Quantity', color_continuous_scale='Blues')
        fig_products.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False) 
        st.plotly_chart(fig_products, use_container_width=True)

# ==========================================
# MODULE C: RFM Customer Segmentation
# ==========================================
def render_rfm_segmentation(df):
    st.markdown("## 🎯 RFM Customer Segmentation")
    st.info("Recency (days since last purchase), Frequency (number of purchases), Monetary (total spend).")
    
    snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',                                  
        'Total_Sales': 'sum'                                     
    }).reset_index()
    
    rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Total_Sales': 'Monetary'}, inplace=True)
    quantiles = rfm.quantile(q=[0.25, 0.5, 0.75])
    
    def r_score(x):
        if x <= quantiles['Recency'][0.25]: return 4
        elif x <= quantiles['Recency'][0.50]: return 3
        elif x <= quantiles['Recency'][0.75]: return 2
        else: return 1
        
    def fm_score(x, c):
        if x <= quantiles[c][0.25]: return 1
        elif x <= quantiles[c][0.50]: return 2
        elif x <= quantiles[c][0.75]: return 3
        else: return 4
        
    rfm['R'] = rfm['Recency'].apply(r_score)
    rfm['F'] = rfm['Frequency'].apply(fm_score, args=('Frequency',))
    rfm['M'] = rfm['Monetary'].apply(fm_score, args=('Monetary',))
    rfm['RFM_Segment'] = rfm['R'].map(str) + rfm['F'].map(str) + rfm['M'].map(str)
    
    def segment_label(row):
        if row['RFM_Segment'] == '444': return 'Champions'
        elif row['R'] >= 3 and row['F'] >= 3: return 'Loyal Customers'
        elif row['R'] <= 2 and row['F'] == 1: return 'Lost'
        elif row['R'] == 2 and row['F'] >= 3: return 'At Risk'
        else: return 'Average'
        
    rfm['Segment_Label'] = rfm.apply(segment_label, axis=1)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(rfm.head(15), use_container_width=True)
    with col2:
        segment_counts = rfm['Segment_Label'].value_counts().reset_index()
        segment_counts.columns = ['Segment_Label', 'Count']
        fig_segments = px.pie(segment_counts, names='Segment_Label', values='Count', 
                              title="Customer Segments", hole=0.4, template="plotly_white")
        fig_segments.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_segments, use_container_width=True)

# ==========================================
# MODULE D: Market Basket Analysis
# ==========================================
def render_market_basket(df):
    st.markdown("## 🛒 Recommendation Engine")
    st.info("Using the Apriori algorithm to discover products frequently bought together.")
    
    country = st.selectbox("Select Country for Analysis:", df['Country'].unique(), index=0)
    basket_df = df[df['Country'] == country]
    
    if len(basket_df) < 100:
        st.warning("Not enough transaction data for this country to run meaningful analysis.")
        return
    
    with st.spinner('Building the Basket Matrix & Running Algorithm...'):
        basket = (basket_df.groupby(['InvoiceNo', 'Description'])['Quantity']
                  .sum().unstack().reset_index().fillna(0)
                  .set_index('InvoiceNo'))
        
        def encode_units(x):
            if x <= 0: return 0
            if x >= 1: return 1
        
        basket_sets = basket.applymap(encode_units)
        frequent_itemsets = apriori(basket_sets, min_support=0.03, use_colnames=True)
        
        if frequent_itemsets.empty:
            st.warning("No frequent itemsets found with current support threshold. Try a country with more data.")
            return
            
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        rules = rules.sort_values('lift', ascending=False)
        
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        st.markdown("### Top Product Recommendations")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(15), use_container_width=True)

# ==========================================
# MAIN APP
# ==========================================
def main():
    inject_custom_css()
    
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    menu = ["Basic EDA", "Customer Segmentation", "Recommendation Engine"]
    choice = st.sidebar.radio("Go to:", menu)
    
    df = load_and_clean_data()
    
    if not df.empty:
        if choice == "Basic EDA":
            render_macro_eda(df)
        elif choice == "Customer Segmentation":
            render_rfm_segmentation(df)
        elif choice == "Recommendation Engine":
            render_market_basket(df)

if __name__ == '__main__':
    main()