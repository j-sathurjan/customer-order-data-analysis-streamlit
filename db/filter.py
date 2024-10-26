from db.db_connector import get_db_connection
import pandas as pd
import streamlit as st
from datetime import date

# Get the database connection engine
engine = get_db_connection()

def get_max_filter_amount():
    try:
        if engine:
            query = """
                select max(spent_amount) max_amount, max(order_count) max_count
                from (select sum(total_amount) spent_amount, count(order_id) order_count
                from orders
                group by customer_id) sum_table;
            """
            max_df = pd.read_sql(query, con=engine)
            return int(max_df['max_amount']), int(max_df['max_count'])
        return st.error("Database connection error!")
    except Exception:
        return st.error("something went wrong on filtering!")

def filter_data_by_sidebar(date_range, min_amount=0, min_orders=0):
    try:
        if engine:
            start_date = '2024-01-01'
            end_date = date.today()
            if date_range:
                start_date, end_date = date_range
            filter_query = f""" SELECT o.order_id, o.total_amount, DATE(o.order_date) order_date, o.customer_id, c.customer_name
                                FROM orders o
                                LEFT JOIN customers c
                                ON o.customer_id=c.customer_id
                                WHERE   (o.order_date BETWEEN '{start_date}' AND '{end_date}') AND
                                        (c.customer_id IN ( SELECT customer_id
                                                            FROM orders
                                                            GROUP BY customer_id
                                                            HAVING SUM(total_amount) > {min_amount} AND COUNT(order_id) > {min_orders})); """
            
            orders_df = pd.read_sql(filter_query, con=engine)
            return orders_df
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")

def filter_customer_by_amount(min_amount= 0, min_orders = 0):
    try:
        if engine:
            filter_query = f"""
                    SELECT c.customer_id, c.customer_name, sum_tab.total_spent,sum_tab.number_of_orders, c.customer_email 
                    FROM customers c
                    JOIN (SELECT customer_id, sum(total_amount) total_spent, count(order_id) number_of_orders
                                        FROM orders
                                        GROUP BY customer_id
                                        HAVING sum(total_amount) > {min_amount} AND count(order_id) > {min_orders}) sum_tab
                    ON c.customer_id = sum_tab.customer_id
                """
            
            customers_df = pd.read_sql(filter_query, con=engine)
            return customers_df
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")

def top_customer_by_revenue(top_number=10):
    try:
        if engine:
            filter_query = f"""
                        SELECT c.customer_id, c.customer_name, sum_tab.spent_amount, sum_tab.order_count
                        FROM customers c
                        RIGHT JOIN (SELECT customer_id, sum(total_amount) spent_amount, count(order_id) order_count
                                FROM orders
                                GROUP BY customer_id
                                ORDER BY spent_amount DESC
                                LIMIT {int(top_number)}) sum_tab
                        ON c.customer_id=sum_tab.customer_id;
            
                        """
            customers_df = pd.read_sql(filter_query, con=engine)
            return customers_df
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")

def get_total_over_time():
    try:
        if engine:
            filter_query = f"""
                        SELECT year(order_date) order_year,month(order_date) order_month, sum(total_amount) spent_amount, count(order_id) order_count
                        FROM orders
                        GROUP BY year(order_date),month(order_date)
                        ORDER BY year(order_date),month(order_date)
                        """
            revenue_df = pd.read_sql(filter_query, con=engine)
            return revenue_df
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")

def get_total_summery():
    try:
        if engine:
            customer_query = "select count(distinct(customer_id)) customer_count from customers;"
            order_query = "select count(order_id) order_count, sum(total_amount) total_spent from orders;"
            customer_summery = pd.read_sql(customer_query, con=engine)
            order_summery = pd.read_sql(order_query, con=engine)
            
            total_customers = int(customer_summery['customer_count'])
            total_revenue = float(order_summery['total_spent'])
            total_orders = int(order_summery['order_count'])
            return total_revenue, total_customers, total_orders
        return st.error("Database connection error!")
    except Exception:
        return st.warning("something went wrong on filtering!")