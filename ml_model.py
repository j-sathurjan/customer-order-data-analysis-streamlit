"""
    This module has two classes one is StreamlitLogisticRegressionApp, SimpleLogisticRegressionApp.
    both are usefull for logistic regression machine learning model creation, data processing and prediction
    StreamlitLogisticRegressionApp is build with the streamlit app components in between to display every step
    involved in the process of function execution at the same time SimpleLogisticRegressionApp contains only
    the python code which are relevent to machine learning and do specific task only with the return values.
    - StreamlitLogisticRegressionApp:
        - 
"""
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

engine = get_db_connection()

class StreamlitLogisticRegressionApp():
    #Logistic Regression
    model = LogisticRegression()
    standardizer = StandardScaler()
    
    def data_preprocessing_for_model_build(self):
        try:
            if engine:
                #get the customer data with their total orders and total spent
                data_frame = filter_customer_by_amount(0,0)
                
                st.subheader("Data Preprocessing")
                st.write("This section involves in data processing before dive deeper into the machine learning field.")
                
                st.write("The original data filtered from the mysql to fit into our need is displayed below")
                st.dataframe(data_frame)
                
                #rename the columns and add the repeat puchaser column
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
        try:
            predict_data = self.standardizer.fit_transform(data)
            y_predict = self.model.predict(predict_data)
            return y_predict
        except Exception:
            return st.error("something went wrong on prediction!")
        
    # def build_lr_model(self, X,y,k=5):
    #     # Logistic Regression
    #     model = LogisticRegression()        
    #     return model

class SimpleLogisticRegressionApp():
    #Logistic Regression
    model = LogisticRegression()
    standardizer = StandardScaler()
    
    def data_preprocessing_for_model_build(self):
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
        try:
            predict_data = self.standardizer.fit_transform(data)
            y_predict = self.model.predict(predict_data)
            return y_predict
        except Exception:
            return st.error("something went wrong on prediction!")