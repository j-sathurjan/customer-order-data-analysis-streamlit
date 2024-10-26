import streamlit as st
from db.db_connector import get_db_connection
import pandas as pd
from filter import filter_data_by_sidebar, get_max_filter_amount, filter_customer_by_amount,top_customer_by_revenue,get_total_over_time,get_total_summery
import calendar

def data_filtering():
    
    sidebar_max_amount, sidebar_max_order = get_max_filter_amount()
    
    # Sidebar Filters
    st.sidebar.subheader("Data Filters")
    st.sidebar.write("let's apply some filters to play around the data.")
    date_range = st.sidebar.date_input('Order Date Range',[])
    min_amount = st.sidebar.slider('Filter By Total Spent', min_value=0, max_value=sidebar_max_amount)
    min_orders = st.sidebar.slider('Min Number Of Orders Placed By A Customer',min_value=0, max_value=sidebar_max_order)

    filter_orders = filter_data_by_sidebar(date_range, min_amount, min_orders)
    filter_customers = filter_customer_by_amount(min_amount, min_orders)

    st.header("Delivergate Data Engineering")
    st.write("Let's get some insights about the customer and order data through the streamlit application.")
    tab1, tab2 = st.tabs(['Orders Data With Customers','Customers Data'])
    with tab1:
        st.write("""### Orders Data """)
        st.write(f"""This is orders data joined with customer data filtered by date:{date_range},
                    and the total amount spent by the customer is above {min_amount}
                    and the total number of orders place by the perticular customer is above {min_orders}""")
        st.dataframe(filter_orders)
    with tab2:
        st.write("## Customers Data")
        st.write(f"""This is customer data filtered by 
                the total amount spent by the customer is above {min_amount}
                and the total number of orders place by the perticular customer is above {min_orders}""")
        st.dataframe(filter_customers)
        
def dashboard_data_visualization():
    st.subheader('Top 10 Customers by Revenue') 
    filter_top_customer = top_customer_by_revenue(10)
    st.bar_chart(filter_top_customer,y="spent_amount", x="customer_name",x_label='Customer',y_label='Total Spent')

    grouped_date = get_total_over_time()
    grouped_date.drop(['order_count'], axis=1, inplace=True)
    grouped_date['order_month'] = grouped_date['order_month'].apply(lambda x: calendar.month_abbr[x])
    grouped_date['month_with_year'] = grouped_date['order_year'].astype(str) +" - "+ grouped_date['order_month']
    st.subheader('Total Revenue Over Time')
    st.line_chart(grouped_date,y='spent_amount', x='month_with_year', color='#ffaa00', x_label='Month',y_label='total revenue')

def dashboard_key_metrics_display():
    st.subheader('Summary Metrics')
    total_revenue,total_customers,total_orders=get_total_summery()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"Total Revenue", value=f"{total_revenue}", delta="")
    with col2:
        st.metric(label=f"Number of unique customers", value=f"{total_customers}", delta="")
    with col3:
        st.metric(label=f"Number of orders", value=f"{total_orders}", delta="")