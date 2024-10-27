"""
Machine Learning Model Module for Streamlit Application

This module includes two classes for building, validating, and predicting using 
a logistic regression model:
1. StreamlitLogisticRegressionApp: Integrates Streamlit UI components for displaying 
   intermediate steps and data at each stage.
2. SimpleLogisticRegressionApp: Contains only the core machine learning code, 
   returning values directly without displaying in Streamlit.

Classes:
- StreamlitLogisticRegressionApp: Manages logistic regression with UI components for 
  interactive data processing and prediction.
- SimpleLogisticRegressionApp: Provides a streamlined logistic regression model for 
  background processing without Streamlit UI.
"""
#import necessory libraries
import streamlit as st
from db.db_connector import get_db_connection
from db.filter import filter_customer_by_amount
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time

# Initialize the database connection
engine = get_db_connection()

class StreamlitLogisticRegressionApp():
    """
    Streamlit-enabled Logistic Regression Model for interactive UI.

    This class handles data processing, validation, and prediction steps, 
    integrating Streamlit components to display intermediate results.
    """
    model = LogisticRegression() # Initialize Logistic Regression model
    standardizer = StandardScaler() # Initialize standard scaler for data normalization
    
    def data_preprocessing_for_model_build(self):
        """
        Preprocess Customer Data for Model Training.

        This function retrieves customer data from the database, preprocesses it, 
        and prepares input features (`X`) and target (`y`) for model training.
        
        Returns:
            tuple: Processed features (X) and target (y) data.
        """
        try:
            if engine:
                # Retrieve customer data and display initial dataset
                data_frame = filter_customer_by_amount(0,0)
                st.subheader("Data Preprocessing")
                st.write("This section involves in data processing before dive deeper into the machine learning field.")
                st.write("The original data filtered from the mysql to fit into our need is displayed below")
                st.dataframe(data_frame)
                
                # Add target column and rename columns
                st.write("lets add a new column repeat_purchaser which is used as target feature to train our model.")
                data_frame.rename(columns={"total_spent":"total_revenue","number_of_orders":"total_orders"}, inplace=True)
                data_frame['repeat_purchaser'] =  data_frame['total_orders']>1
            
                st.write("""the data after adding the repeat_purchaser column will be as below. 
                        if the total order is above 1 he is repeat puchaser else not.""")
                st.dataframe(data_frame.head(5))
                
                #extract usefull features only from the dataset
                st.write("""lets extract the usefull columns only from the dataframe""")
                processingData = data_frame[['total_revenue','total_orders','repeat_purchaser']]
                st.dataframe(processingData.head(5))
                
                # Count rows with null values
                st.write("""check for null values.
                        since the data is filtered by sql already i skiped other data processing techniques.""")
                null_rows_count = processingData.isnull().any(axis=1).sum()
                st.write(null_rows_count)
                
                #Frequency of repeat_purchaser
                st.write("lets display the frequency of the target column values")
                frequency = processingData['repeat_purchaser'].value_counts()
                st.write(frequency)
                
                
                # split the features and target variables
                st.write("split the dataset into input features(x) and target(y)")
                X = processingData[['total_revenue','total_orders']]  # Features (total_revenue, total_orders)
                y = processingData['repeat_purchaser']   # Target variable (repeat_purchaser)
                x_col,y_col = st.columns(2)
                with x_col:
                    st.write("x",X)
                with y_col:
                    st.write("y",y)
                self.X = X
                self.y = y
                return self.X , self.y
            return st.error("database connection failed!")
        except Exception:
            return st.error(f"something went wrong on data processing!")

    def validate_the_lr_model(self,X,y,k=5):
        """
        Validate Logistic Regression Model using k-Fold Cross-Validation.

        Parameters:
            X (DataFrame): Input features for model training.
            y (Series): Target variable for model training.
            k (int): Number of folds for cross-validation (default is 5).

        Returns:
            LogisticRegression: Trained logistic regression model.
        """
        try:
            st.subheader("Data Validation")
            st.write("""In this section i am going to validate my logistic regression model 
                    on our preprocessed data using the kfold cross validation.""")
            
            #define the folds to validate
            st.write(f"Lets define folds count as {k}")
            n_folds = k
            skf = StratifiedKFold(n_splits=n_folds)
            
            # prepare the features and target
            st.write("""Lets standardize our input data X and flatten the target data Y""")
            x_label = self.standardizer.fit_transform(X)
            y_label = np.ravel(y)
            x_col, y_col = st.columns(2)
            with x_col:
                st.write("X",x_label)
            with y_col:
                st.write("Y",y_label)
            
            #initialize the testing metric to update the test metrics 
            test_accuracy, test_precision, test_recall, test_f1, test_time = np.zeros((5,n_folds))
            
            #iterate nfolds to fit the model and find metrics of each folds
            for i, (train_index, test_index) in enumerate(skf.split(x_label, y_label)):
                
                # Measure execution time
                start_time = time.time()
            
                self.model.fit(x_label[train_index], y_label[train_index])
                y_pred = self.model.predict(x_label[test_index])
                
                # Calculate execution time
                end_time = time.time()
                
                # performance metrics
                test_accuracy[i] = accuracy_score(y_label[test_index], y_pred)
                test_precision[i] = precision_score(y_label[test_index], y_pred)
                test_recall[i] = recall_score(y_label[test_index], y_pred)
                test_f1[i] = f1_score(y_label[test_index], y_pred)
                test_time[i]= end_time - start_time
            
            #combine the matrics array to a dataframe
            st.write(f"""lets validate the model on {n_folds} folds and get the performance metrics on each folds.
                    This is called {n_folds}-Fold cross validation""")
            kfold_metric = pd.DataFrame(index=[f"fold-{x+1}" for x in range(n_folds)],
                                    columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])
            kfold_metric['Accuracy'] = test_accuracy
            kfold_metric['Precision'] = test_precision
            kfold_metric['Recall'] = test_recall
            kfold_metric['F1score'] = test_f1
            kfold_metric['Time'] = test_time
            st.write(kfold_metric)
            
            #find the mean and standar deviation of the validations metrics
            st.write(f"""lets find the mean and standard deviation the {n_folds}Fold evaluation metrics""")
            average_metric = pd.DataFrame(index=['Mean','Standard Deviation'],
                                    columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])
            average_metric['Accuracy'] = test_accuracy.mean(),test_accuracy.std()
            average_metric['Precision'] = test_precision.mean(),test_precision.std()
            average_metric['Recall'] = test_recall.mean(),test_recall.std()
            average_metric['F1score'] = test_f1.mean(),test_f1.std()
            average_metric['Time'] = test_time.mean(),test_time.std()
            
            st.write(average_metric)
            return self.model
        except Exception:
            return st.error("some thing went wrong on validation!")
        
    def predict_data_from_model(self,data):
        """
        Predict Customer Repeat Purchase Behavior.

        Parameters:
            data (DataFrame): Input data with `total_revenue` and `total_orders`.

        Returns:
            ndarray: Prediction result (1 for repeat purchaser, 0 for non-repeat).
        """
        try:
            predict_data = self.standardizer.fit_transform(data)
            y_predict = self.model.predict(predict_data)
            return y_predict
        except Exception:
            return st.error("An error occurred during prediction.")
        
    # def build_lr_model(self, X,y,k=5):
    #     # Logistic Regression
    #     model = LogisticRegression()        
    #     return model

class SimpleLogisticRegressionApp():
    """
    Basic Logistic Regression Model for background processing.

    This class provides core functionality for logistic regression, without 
    Streamlit components, making it suitable for backend processing.
    """
    #Logistic Regression
    model = LogisticRegression()
    standardizer = StandardScaler()
    
    def data_preprocessing_for_model_build(self):
        """
        Preprocess Data for Logistic Regression Model.

        Retrieves customer data, adds target column, and prepares features (`X`) 
        and target (`y`).
        
        Returns:
            tuple: Processed features (X) and target (y) data.
        """
        try:
            if engine:
                #get the customer data with their total orders and total spent
                data_frame = filter_customer_by_amount(0,0)
                data_frame.rename(columns={"total_spent":"total_revenue","number_of_orders":"total_orders"}, inplace=True)
                data_frame['repeat_purchaser'] =  data_frame['total_orders']>1
                processingData = data_frame[['total_revenue','total_orders','repeat_purchaser']]
                
                # split the features and target variables
                X = processingData[['total_revenue','total_orders']]  # Features (total_revenue, total_orders)
                y = processingData['repeat_purchaser']   # Target variable (repeat_purchaser)
                x_col,y_col = st.columns(2)
                self.X, self.y  = X, y
                return X,y
            return None
        except Exception:
            return st.error("something went wrong!")

    def validate_the_lr_model(self,X,y,k=5):
        """
        Validate Logistic Regression Model with k-Fold Cross-Validation.

        Parameters:
            X (DataFrame): Input features for model training.
            y (Series): Target variable for model training.
            k (int): Number of folds for cross-validation.

        Returns:
            tuple: Trained model, average metrics, and fold-wise metrics.
        """
        try:
            n_folds = k
            skf = StratifiedKFold(n_splits=n_folds)
            x_label = self.standardizer.fit_transform(X)
            y_label = np.ravel(y)
            
            #initialize the testing metric to update the test metrics 
            test_accuracy, test_precision, test_recall, test_f1, test_time = np.zeros((5,n_folds))
            
            #iterate nfolds to fit the model and find metrics of each folds
            for i, (train_index, test_index) in enumerate(skf.split(x_label, y_label)):
                
                # Measure execution time
                start_time = time.time()
            
                self.model.fit(x_label[train_index], y_label[train_index])
                y_pred = self.model.predict(x_label[test_index])
                
                # Calculate execution time
                end_time = time.time()
                
                # performance metrics
                test_accuracy[i] = accuracy_score(y_label[test_index], y_pred)
                test_precision[i] = precision_score(y_label[test_index], y_pred)
                test_recall[i] = recall_score(y_label[test_index], y_pred)
                test_f1[i] = f1_score(y_label[test_index], y_pred)
                test_time[i]= end_time - start_time
            
            #combine the matrics array to a dataframe
            kfold_metric = pd.DataFrame(index=[f"fold-{x+1}" for x in range(n_folds)],
                                    columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])
            kfold_metric['Accuracy'] = test_accuracy
            kfold_metric['Precision'] = test_precision
            kfold_metric['Recall'] = test_recall
            kfold_metric['F1score'] = test_f1
            kfold_metric['Time'] = test_time
            
            #find the mean and standar deviation of the validations metrics
            average_metric = pd.DataFrame(index=['Mean','Standard Deviation'],
                                    columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])
            average_metric['Accuracy'] = test_accuracy.mean(),test_accuracy.std()
            average_metric['Precision'] = test_precision.mean(),test_precision.std()
            average_metric['Recall'] = test_recall.mean(),test_recall.std()
            average_metric['F1score'] = test_f1.mean(),test_f1.std()
            average_metric['Time'] = test_time.mean(),test_time.std()
            
            self.performance_metrics = average_metric
            self.validation_metrics = kfold_metric
            return self.model, average_metric, kfold_metric
        except Exception:
            return st.error("something went wrong!")
        
    def predict_data_from_model(self,data):
        """
        Predict Customer Repeat Purchase Behavior.

        Parameters:
            data (DataFrame): Input data with `total_revenue` and `total_orders`.

        Returns:
            ndarray: Prediction result (1 for repeat purchaser, 0 for non-repeat).
        """
        try:
            predict_data = self.standardizer.fit_transform(data)
            y_predict = self.model.predict(predict_data)
            return y_predict
        except Exception:
            return st.error("something went wrong on prediction!")