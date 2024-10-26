import streamlit as st
from db.db_connector import get_db_connection
import pandas as pd
from ml_model import StreamlitLogisticRegressionApp

ml_app = StreamlitLogisticRegressionApp()
def ml_prediction_display():
    try:
        st.subheader("Prediction")
        st.write("Lets predict a customer's behaviour, play some values and get the prediction.")
        total_revenue = st.number_input(
        "Insert a Revenue", placeholder="Type the total spent of the customer..."
        )
        total_orders = st.number_input(
            "Insert total orders", placeholder="Type the number of orders placed...", min_value=1
        )
        if st.button("predict"):
            data = pd.DataFrame(index=['0'])
            data['total_revenue'] = total_revenue
            data['total_orders'] = total_orders
            y = ml_app.predict_data_from_model(data)
            if y == 0:
                st.info("Customer is not a repeat purchaser")
            else:
                st.success("Great! This customer is repeat purchaser")
            st.write("see the predicted output below",y)
    except Exception:
        return st.error("something went wrong on prediction")
        
def ml_data_processing_display():
    try:
        st.header("Machine Learning Engineering")
        st.write("""Lets dive into the machine learning world!.
                here we used some machine learning libraries and techniques to build a 
                smooth streamlit application with machine learning capablities.""")
        st.write("here we use 3 tabs to seperate sections to make this visualy appealing")
        
        data_process_tab, validate_tab, model_tab = st.tabs(['Data Processing','Validations','Predictions'])
        with data_process_tab:
            try:
                X,y=ml_app.data_preprocessing_for_model_build()
            except Exception:
                return st.error("error loading processing data")
        with validate_tab:
            try:
                st.sidebar.subheader("Validation")
                st.sidebar.write("""Lets validate our ML model, play with the folds as you wish""")
                n_fold = st.sidebar.number_input("Enter the Fold Value",min_value=2, max_value=10, value=5)
                model = ml_app.validate_the_lr_model(X,y,n_fold)
            except Exception:
                return st.error("error on model validation.")
        with model_tab:
            try:
                ml_prediction_display()
            except Exception:
                return st.error("error on prediction")
    except Exception:
        return st.error("something went wrong!")
        