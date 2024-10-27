"""This module all about to organize all the content related to machine learning page.
    there two function to make this happens in a moduler way.
    - ml_prediction_display
    - ml_data_processing_display
"""
import streamlit as st
from db.db_connector import get_db_connection
import pandas as pd
from ml_model import StreamlitLogisticRegressionApp

ml_app = StreamlitLogisticRegressionApp()

def ml_prediction_display():
    """this function displays all the data related to machine learning model prediction.
    this will dispay input elements to get the revenue and the amount to be predicted from the user.
    when the user click on the Predict button the function display the prediction out put as a dataframe 
    as well as status message. if the predicted output is 1 it will display success message as 
    "Great! This customer is repeat purchaser" if the predicted output is 0 it will display a info message
    "Customer is not a repeat purchaser".

    Returns:
        status message: if the predicted output is 1 and 0 success and info message
                        if the exception thrown error status message.
    """
    try:
        #prediction related contents
        st.subheader("Prediction") #sub heading
        st.write("Lets predict a customer's behaviour, play some values and get the prediction.") #paragraph
        #input elements to get user input for prediction
        total_revenue = st.number_input(
        "Insert a Revenue", placeholder="Type the total spent of the customer..."
        ) # get number input
        total_orders = st.number_input(
            "Insert total orders", placeholder="Type the number of orders placed...", min_value=1
        ) #get number input
        
        #conditionally display if the Predict button is clicked code below get executed.
        if st.button("predict"):
            data = pd.DataFrame(index=['0']) # create 1 record empty data frame
            data['total_revenue'] = total_revenue #assign data frame value
            data['total_orders'] = total_orders #assign data frame value
            y = ml_app.predict_data_from_model(data) #predict target from model
            if y == 0:
                st.info("Customer is not a repeat purchaser") #info status message display
            else:
                st.success("Great! This customer is repeat purchaser") #success status message display
            st.write("see the predicted output below",y) #display predicted value of the given user input
    except Exception:
        return st.error("something went wrong on prediction") #return error status message
        
def ml_data_processing_display():
    """This function is all about to organize and display the machine learning page contents.
    here page has been organized into three tabs. tabs display the content related
     - data processing
     - validations
     - predictions
    
    Return: it return none. since there is no need of return values from the try block
            if error thrown it will return a error status message.
    """
    
    try:
        st.header("Machine Learning Engineering") #heading of the page
        st.write("""Lets dive into the machine learning world!.
                here we used some machine learning libraries and techniques to build a 
                smooth streamlit application with machine learning capablities.""") #small discription
        st.write("here we use 3 tabs to seperate sections to make this visualy appealing") # paragraph
        
        #create 3 tabs to display the content in an organized way
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
        