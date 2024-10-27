"""
Machine Learning Module for Streamlit Application

This module manages the content on the machine learning page of the Streamlit app. 
It organizes the page into three main sections:
1. Data Processing: Prepares and displays data for model training.
2. Model Validation: Allows users to validate the model with custom fold values.
3. Predictions: Provides an interface for users to input values and make predictions.

Functions:
- ml_prediction_display: Displays prediction input fields and prediction results based on user input.
- ml_data_processing_display: Organizes and displays the machine learning page with tabs for data processing, 
  validation, and prediction.
"""

import streamlit as st # Streamlit for app interface
from db.db_connector import get_db_connection # Database connection function
import pandas as pd # Data manipulation library
from ml_model import StreamlitLogisticRegressionApp # Import custom logistic regression class

# Initialize the ML model app
ml_app = StreamlitLogisticRegressionApp()

def ml_prediction_display():
    """
    Display Prediction Interface for Machine Learning Model.

    This function displays input fields for users to enter `total_revenue` and `total_orders`.
    When the "Predict" button is clicked, it predicts the customer's repeat purchase behavior 
    and displays a status message based on the output:
    - Success message for repeat purchasers.
    - Info message for non-repeat purchasers.

    Returns:
        None if successful, or a Streamlit error message if an exception occurs.
    """
    try:
        # Subheader and description for prediction section
        st.subheader("Prediction")
        st.write("Lets predict a customer's behaviour, play some values and get the prediction.")
        
        # Input fields for user to enter revenue and total orders
        total_revenue = st.number_input(
        "Insert a Revenue", placeholder="Type the total spent of the customer..."
        ) # get number input
        total_orders = st.number_input(
            "Insert total orders", placeholder="Type the number of orders placed...", min_value=1
        ) #get number input
        
        # Predict button - performs prediction when clicked
        if st.button("predict"):
            # Prepare input data for the model
            data = pd.DataFrame(index=['0']) # create 1 record empty data frame
            data['total_revenue'] = total_revenue #assign data frame value
            data['total_orders'] = total_orders #assign data frame value
            
            # Predict using the ML model
            y = ml_app.predict_data_from_model(data)
            
            # Display prediction result and status message
            if y == 0:
                st.info("Customer is not a repeat purchaser") #info status message display
            else:
                st.success("Great! This customer is repeat purchaser") #success status message display
            st.write("see the predicted output below",y) #display predicted value of the given user input
            
    except Exception:
        return st.error("something went wrong on prediction") # Error message if prediction fails
        
def ml_data_processing_display():
    """
    Display and Organize Machine Learning Page.

    This function organizes the machine learning page content into three tabs:
    - Data Processing: Prepares and displays data for model training.
    - Validations: Validates the model with customizable fold values.
    - Predictions: Allows users to enter input and receive predictions.

    Returns:
        None. Displays error message if an exception occurs.
    """
    try:
        # Page header and description
        st.header("Machine Learning Engineering") #heading of the page
        st.write("""
            Dive into the machine learning world! We used various ML techniques 
            to create a Streamlit application with predictive capabilities.
        """)
        st.write("here we use 3 tabs to seperate sections to make this visualy appealing") # paragraph
        
        # Create tabs for Data Processing, Validation, and Predictions
        data_process_tab, validate_tab, model_tab = st.tabs(['Data Processing','Validations','Predictions'])
        
        #data processing tab contents
        with data_process_tab:
            #get the preprocessed X,y and also calling the function diplay contents related to preprocessing step
            X,y=ml_app.data_preprocessing_for_model_build() #preprocessed X and y

        #Validations tab
        with validate_tab:
            st.sidebar.subheader("Validation") #sidebar sub heading
            st.sidebar.write("""Lets validate our ML model, play with the folds as you wish""") #sidebar paragraph
            #get the folds value from the sidebar number input and store it in n_folds
            n_fold = st.sidebar.number_input("Enter the Fold Value",min_value=2, max_value=10, value=5)
            #get the trained model as well as calling the validate function 
            # displays the content related to validation step
            model = ml_app.validate_the_lr_model(X,y,n_fold)
            
        #Predictions tab
        with model_tab:
            #call the ml_prediction_display function within this module to display all prediction related content
            # within the predictions tab
            ml_prediction_display()
        return None
    except Exception:
        return st.error("something went wrong!") #return error status message
        