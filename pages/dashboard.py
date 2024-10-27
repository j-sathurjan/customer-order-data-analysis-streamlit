"""
Dashboard Module for Streamlit Application

This module provides functions for displaying data filtering options, visualizations,
and key metrics on the dashboard page of the Streamlit app. It includes:
1. Data filtering: Allows users to apply filters based on date range, total amount spent, 
   and minimum orders placed.
2. Data visualization: Displays bar and line charts for insights into customer spending.
3. Key metrics display: Shows summary statistics for total revenue, unique customers, 
   and number of orders.

Functions:
- data_filtering: Displays sidebar filters and filtered data tables for orders and customers.
- dashboard_data_visualization: Creates bar and line charts to visualize top customers by revenue
  and total revenue over time.
- dashboard_key_metrics_display: Displays summary metrics including total revenue, unique customers, 
  and order count.
"""
import streamlit as st # Main library for app interface
from db.db_connector import get_db_connection # Database connection function
import pandas as pd # Data manipulation library
from db.filter import ( # Import filter functions for data processing
    filter_data_by_sidebar,
    get_max_filter_amount,
    filter_customer_by_amount,
    top_customer_by_revenue,
    get_total_over_time,
    get_total_summery
)
import calendar # Standard library for working with dates

def data_filtering():
    """
    Display Data Filters and Filtered Data Tables.

    This function provides:
    - Sidebar filters for users to select a date range, minimum spend, and minimum orders.
    - Displays filtered data tables for "Orders Data with Customers" and "Customers Data" 
      based on selected filters.

    Raises:
        Exception: Catches errors related to data filtering and displays an error message.
    """
    try:
        # Get the maximum values for the sidebar sliders
        sidebar_max_amount, sidebar_max_order = get_max_filter_amount()
        
        # Sidebar Filter Configuration
        st.sidebar.subheader("Data Filters")
        st.sidebar.write("let's apply some filters to play around the data.")
        
        # Define sidebar filters for date range, minimum amount, and minimum orders
        date_range = st.sidebar.date_input('Order Date Range',[])
        min_amount = st.sidebar.slider('Filter By Total Spent', min_value=0, max_value=sidebar_max_amount)
        min_orders = st.sidebar.slider('Min Number Of Orders Placed By A Customer',min_value=0, max_value=sidebar_max_order)

        # Filter data based on sidebar input
        filter_orders = filter_data_by_sidebar(date_range, min_amount, min_orders)
        filter_customers = filter_customer_by_amount(min_amount, min_orders)

        # Page Header and Information
        st.header("Delivergate Data Engineering")
        st.write("Explore insights about customer and order data with interactive filters.")
        
        # Tabbed Display for Filtered Data
        tab1, tab2 = st.tabs(['Orders Data With Customers','Customers Data'])
        
        with tab1:
            st.write("""### Orders Data """)
            st.write(f"""
                This is orders data joined with customer data filtered by date:{date_range}, 
                and the total amount spent by the customer is above {min_amount}, 
                and the total number of orders place by the perticular customer is above {min_orders}
            """)
            st.dataframe(filter_orders) # Display the filtered customers data
            
        with tab2:
            st.write("## Customers Data")
            st.write(f"""
                This is customer data filtered by 
                the total amount spent by the customer is above {min_amount}
                and the total number of orders place by the perticular customer is above {min_orders}
            """)
            st.dataframe(filter_customers) # Display the filtered customers data
            
    except Exception:
        return st.error("Error in filtering the data!") # Display error if filtering fails
        
def dashboard_data_visualization():
    """
    Display Data Visualizations.

    This function creates:
    - A bar chart showing the top 10 customers by revenue.
    - A line chart displaying total revenue over time.
    
    Raises:
        Exception: Catches errors related to data visualization and displays an error message.
    """
    try:
        # Display top 10 customers by revenue
        st.subheader('Top 10 Customers by Revenue') 
        filter_top_customer = top_customer_by_revenue(10)
        st.bar_chart(filter_top_customer,y="spent_amount", x="customer_name",x_label='Customer',y_label='Total Spent')

        # Display total revenue over time with month and year
        grouped_date = get_total_over_time()
        grouped_date.drop(['order_count'], axis=1, inplace=True)
        
        # Convert month number to abbreviated month name for clarity
        grouped_date['order_month'] = grouped_date['order_month'].apply(lambda x: calendar.month_abbr[x])
        grouped_date['month_with_year'] = grouped_date['order_year'].astype(str) +" - "+ grouped_date['order_month']
        
        # display header and line chart of the Total Revenue Over Time
        st.subheader('Total Revenue Over Time')
        st.line_chart(grouped_date,y='spent_amount', x='month_with_year', color='#ffaa00', x_label='Month',y_label='total revenue')
    
    except Exception:
        return st.error("Error in visualizing data required to draw chart!") # Display error if visualization fails

def dashboard_key_metrics_display():
    """
    Display Key Metrics on Dashboard.

    This function shows:
    - Total revenue
    - Number of unique customers
    - Number of orders

    The metrics are displayed in three columns for a clean layout.
    
    Raises:
        Exception: Catches errors related to displaying metrics and shows an error message.
    """
    try:
        # Retrieve key metrics for display
        st.subheader('Summary Metrics')
        total_revenue,total_customers,total_orders=get_total_summery()
        
        # Display metrics in columns for better readability
        col1, col2, col3 = st.columns(3)
        with col1:
            #display total revenue in metric output
            st.metric(label=f"Total Revenue", value=f"{total_revenue}", delta="")
        with col2:
            #display Number of unique customers in metric output
            st.metric(label=f"Number of unique customers", value=f"{total_customers}", delta="")
        with col3:
            #display Number of orders in metric output
            st.metric(label=f"Number of orders", value=f"{total_orders}", delta="")

    except Exception:
        return st.error("Error in retrieving metrics data!")  # Display error if metrics retrieval fails
